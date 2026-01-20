# DIAGRAMAS TÉCNICOS Y FLUJOS DEL MVP

**Versión:** 1.0  
**Fecha:** 18 de enero de 2026

---

## 1. DIAGRAMA DE ARQUITECTURA GENERAL

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          CATALOGIA MVP ARCHITECTURE                       │
└──────────────────────────────────────────────────────────────────────────┘

┌─ DATA LAYER ───────────────────────────────────────────────────────────┐
│                                                                         │
│  Entrada 1: Imágenes                   Entrada 2: Catálogos            │
│  ├─ PNG/JPG de archivos                ├─ CSV (Symphony)               │
│  ├─ RGB en memoria                     ├─ TXT tabulado (Portfolio)     │
│  └─ Variable size                      └─ UTF-8 encoding               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                    ↓                                    ↓
┌─ PROCESSING LAYER ─────────────────────────────────────────────────────┐
│                                                                         │
│  ┌─ Módulo 1: Catalogación ──┐  ┌─ Módulo 2: Comparativa ─────┐      │
│  │                            │  │                              │      │
│  │  Processor: BLIP-2         │  │  Parser: pandas              │      │
│  │  ├─ Image → Tensores       │  │  ├─ Expand URLs             │      │
│  │  └─ Text tokenization      │  │  ├─ Normalize URLs          │      │
│  │                            │  │  └─ Merge datasets           │      │
│  │  Model: BLIP-2 1.5B params │  │                              │      │
│  │  ├─ Forward pass           │  │  Analysis: Outer join        │      │
│  │  ├─ Token generation       │  │  ├─ Identificar duplicados   │      │
│  │  └─ Beam/Sampling decode   │  │  ├─ Clasificar coincidencias │      │
│  │                            │  │  └─ Estadísticas             │      │
│  │  Post-processor:           │  │                              │      │
│  │  └─ Text deduplication     │  │  Export: Excel               │      │
│  │                            │  │  └─ Todas las columnas       │      │
│  └────────────────────────────┘  └──────────────────────────────┘      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                    ↓                                    ↓
┌─ OUTPUT LAYER ─────────────────────────────────────────────────────────┐
│                                                                         │
│  Output 1: Descripción de imagen       Output 2: Análisis comparativo  │
│  ├─ Formato: Texto (stdout)           ├─ Formato: .xlsx               │
│  ├─ Persistencia: ❌ No               ├─ Persistencia: ✅ Sí          │
│  └─ Ejemplo: "A group of people       └─ Contenido: merged dataframe  │
│     in a photography studio..."           con indicador de estado      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. FLUJO DE CATALOGACIÓN (MÓDULO 1)

```
                    CATALOGACIÓN DE IMÁGENES CON BLIP-2

START
  │
  ├─→ [1. INICIALIZACIÓN DE ENTORNO]
  │   ├─ Deshabilitar verificación SSL
  │   ├─ Configurar verbosity transformers
  │   ├─ Desactivar CUDA_VISIBLE_DEVICES (GPU solo si disponible)
  │   └─ Importar librerías
  │
  ├─→ [2. CARGAR IMAGEN]
  │   ├─ Leer imagen.png/jpg desde disco
  │   ├─ Validación: ❌ NO IMPLEMENTADA
  │   ├─ Convertir a RGB (RGBA, Palette → RGB)
  │   └─ Almacenar en RAM
  │
  ├─→ [3. DETECTAR DISPOSITIVO]
  │   ├─ ¿torch.cuda.is_available()?
  │   │  ├─ SÍ → device = "cuda"
  │   │  └─ NO → device = "cpu"
  │   │
  │   └─ Imprimir dispositivo seleccionado
  │
  ├─→ [4. DESCARGAR/CARGAR MODELO]
  │   │
  │   └─ Primera ejecución:
  │      ├─ Conectar a Hugging Face Hub
  │      ├─ Descargar modelo (~4-5 GB)
  │      │  ├─ blip2-flan-t5-xl (weights)
  │      │  └─ config.json, tokenizer files
  │      └─ Guardar en ~/.cache/huggingface/hub/
  │
  │   Ejecuciones posteriores:
  │      └─ Cargar desde caché local (< 1 segundo)
  │
  │   ├─ Blip2Processor.from_pretrained()
  │   ├─ Blip2ForConditionalGeneration.from_pretrained()
  │   └─ Configurar dtype:
  │      ├─ GPU → torch.float16 (FP16)
  │      └─ CPU → torch.float32 (FP32)
  │
  ├─→ [5. DEFINIR PROMPT]
  │   └─ prompt = "Question: Describe briefly this photograph for 
  │      bibliographic cataloging purposes. Mention people, objects, 
  │      context, and possible relevant topics."
  │
  ├─→ [6. PROCESAR INPUTS]
  │   ├─ processor(imagen, prompt, return_tensors="pt")
  │   │  └─ Salida: {input_ids, pixel_values, attention_mask}
  │   ├─ Mover tensores a dispositivo
  │   └─ .to(device)
  │
  ├─→ [7. GENERAR DESCRIPCIÓN]
  │   ├─ model.generate(
  │   │   **inputs,
  │   │   max_new_tokens=150,      # Limitar longitud
  │   │   temperature=0.7,          # Variabilidad controlada
  │   │   do_sample=True           # Muestreo (no determinístico)
  │   │ )
  │   │
  │   └─ Salida: tensor de token_ids
  │
  ├─→ [8. DECODIFICAR TOKENS]
  │   ├─ processor.decode(generated_ids[0], skip_special_tokens=True)
  │   └─ Salida: Texto en inglés (variable length)
  │
  ├─→ [9. LIMPIAR TEXTO]
  │   ├─ limpiar_texto(caption)
  │   │  ├─ Dividir por espacios
  │   │  ├─ Eliminar palabras consecutivas duplicadas
  │   │  └─ Reunir palabras
  │   └─ Salida: Texto sin duplicados
  │
  ├─→ [10. MOSTRAR RESULTADO]
  │   ├─ print("Resultado de la catalogación automática:")
  │   └─ print(caption_limpia)
  │
  └─→ END

Tiempo total esperado:
  • Primera ejecución: 5-15 min (descarga modelo) + 30-60 seg (procesamiento)
  • Ejecuciones posteriores: 30-90 seg (procesamiento)

En GPU NVIDIA (CUDA):
  • Carga de modelo: < 10 seg
  • Procesamiento imagen: 5-15 seg

En CPU:
  • Carga de modelo: 30-90 seg
  • Procesamiento imagen: 60-180 seg
```

---

## 3. FLUJO DE ANÁLISIS COMPARATIVO (MÓDULO 2)

```
                COMPARACIÓN DE CATÁLOGOS: SYMPHONY VS PORTFOLIO

START
  │
  ├─→ [1. LEER ARCHIVO SYMPHONY]
  │   ├─ Ruta: bnco/Symphony_30_07_2025.csv
  │   ├─ pd.read_csv(
  │   │   sep=";",
  │   │   encoding="utf-8",
  │   │   dtype=str          # Todo como strings
  │   │ )
  │   ├─ Estructura: [Columnas MARC: 001, 245, 856, ...]
  │   └─ Salida: df_symphony (N registros)
  │
  ├─→ [2. LEER ARCHIVO PORTFOLIO]
  │   ├─ Ruta: bnco/Portfolio_22_08_2025.txt
  │   ├─ pd.read_csv(
  │   │   sep="\t",          # Tabulado
  │   │   encoding="utf-8",
  │   │   dtype=str
  │   │ )
  │   ├─ Estructura: NODE_ID | FOLDER | NAME | URL
  │   └─ Salida: df_portfolio (191.716 registros observados)
  │
  ├─→ [3. EXPANDIR SYMPHONY - EXPLODE URLs MÚLTIPLES]
  │   ├─ Problema: Campo 856$u contiene URLs separadas por ";"
  │   │   Ejemplo: "url1.com;url2.com;url3.com"
  │   │
  │   ├─ df_symphony_expanded = df_symphony.assign(
  │   │   url = df_symphony["856$u"].str.split(";")
  │   │ ).explode("url")
  │   │
  │   ├─ Resultado: Una fila por cada URL
  │   │   De: 1 fila con 3 URLs → A: 3 filas con 1 URL cada una
  │   │
  │   └─ Salida: df_symphony_expanded (M registros, M ≥ N)
  │
  ├─→ [4. NORMALIZAR URLs]
  │   ├─ df_symphony_expanded["url"] = 
  │   │   df_symphony_expanded["url"].str.strip()
  │   │
  │   ├─ Eliminar espacios en blanco antes/después
  │   └─ Salida: URLs limpias
  │
  ├─→ [5. REALIZAR MERGE OUTER JOIN]
  │   ├─ merged = df_symphony_expanded.merge(
  │   │   df_portfolio,
  │   │   how="outer",           # Full outer join
  │   │   left_on="url",
  │   │   right_on="URL",
  │   │   indicator=True        # Agregar columna _merge
  │   │ )
  │   │
  │   ├─ Columna _merge contiene:
  │   │   ├─ "left_only" → En Symphony pero no en Portfolio
  │   │   ├─ "right_only" → En Portfolio pero no en Symphony
  │   │   └─ "both" → En ambos sistemas
  │   │
  │   └─ Salida: merged (todas las filas de ambos)
  │
  ├─→ [6. ANALIZAR RESULTADOS]
  │   ├─ print(merged["_merge"].value_counts())
  │   │  Salida ejemplo:
  │   │   both         1500
  │   │   left_only     250
  │   │   right_only    100
  │   │
  │   ├─ solo_symphony = merged[merged["_merge"] == "left_only"]["url"].dropna()
  │   ├─ solo_portfolio = merged[merged["_merge"] == "right_only"]["URL"].dropna()
  │   ├─ en_ambos = merged[merged["_merge"] == "both"]["url"].dropna()
  │   │
  │   └─ print(f"🔹 Solo Symphony: {len(solo_symphony)}")
  │      print(f"🔹 Solo Portfolio: {len(solo_portfolio)}")
  │      print(f"🔹 En ambos: {len(en_ambos)}")
  │
  ├─→ [7. EXPORTAR A EXCEL]
  │   ├─ merged.to_excel(
  │   │   "Comparativo_Symphony_Portfolio.xlsx",
  │   │   index=False
  │   │ )
  │   │
  │   ├─ Salida: Archivo .xlsx con:
  │   │   ├─ Todas las columnas de ambos DataFrames
  │   │   ├─ Columna _merge (indicador de estado)
  │   │   └─ Preservar NaN para datos faltantes
  │   │
  │   └─ Ubicación: Raíz del proyecto
  │
  └─→ END

Complejidad computacional:
  • Lectura Symphony: O(n)
  • Lectura Portfolio: O(m)
  • Explode URLs: O(n·k) donde k = URLs por registro
  • Merge: O((n·k + m) · log(n·k + m)) con índices
  • Exportación Excel: O(n·k + m)
  • Total: O((n·k + m) · log(n·k + m))

Con datos observados (191K Portfolio):
  • Tiempo esperado: 2-5 segundos en CPU
  • Memoria: ~200-300 MB
  • Archivo Excel generado: ~5-10 MB
```

---

## 4. CICLO DE VIDA DEL MODELO BLIP-2

```
                    BLIP-2 MODEL LIFECYCLE IN CATALOGIA

┌─ INSTALACIÓN (Primera ejecución) ──────────────────────────┐
│                                                            │
│  Transformers.from_pretrained()                           │
│         ↓                                                  │
│  ¿Modelo en ~/.cache/huggingface/hub/?                   │
│    │                                                      │
│    ├─ NO                                                  │
│    │  ├─ Conectar a Hugging Face Hub                      │
│    │  ├─ Descargar (~5 GB)                                │
│    │  ├─ Validar checksums                                │
│    │  └─ Guardar en caché                                 │
│    │                                                      │
│    └─ SÍ                                                  │
│       └─ Cargar desde caché (< 1 seg)                      │
│         ↓                                                  │
└─→ Modelo en memoria                                       │
                                                            │
┌─ EJECUCIÓN (Cada imagen) ─────────────────────────────────┐
│                                                            │
│  Para cada imagen:                                        │
│    ├─ Cargar en CPU/GPU                                   │
│    ├─ Procesar (embedding imagen)                         │
│    ├─ Cross-attention con prompt                          │
│    ├─ Generar tokens autoregrevisivos                      │
│    └─ Decodificar a texto                                 │
│                                                            │
└─ Salida: Descripción de imagen                            │
                                                            │
┌─ LIBERACIÓN (Final de programa) ───────────────────────────┐
│                                                            │
│  Al terminar:                                             │
│    ├─ Modelo sigue en RAM                                 │
│    ├─ Caché permanece en disco                            │
│    └─ Próxima ejecución reutiliza ambos                   │
│                                                            │
└─ Modelo persiste en ~/.cache/ entre ejecuciones           │
```

---

## 5. MANEJO DE DISPOSITIVOS (CPU vs GPU)

```
                      DEVICE SELECTION & EXECUTION

START
  │
  ├─→ torch.cuda.is_available()?
  │   │
  │   ├─ SÍ (GPU NVIDIA disponible)
  │   │  ├─ device = "cuda"
  │   │  ├─ torch_dtype = torch.float16 (FP16 - half precision)
  │   │  ├─ device_map = "auto"
  │   │  │
  │   │  ├─ Ventajas:
  │   │  │  ├─ 5-10x más rápido
  │   │  │  ├─ Menos memoria (FP16 vs FP32)
  │   │  │  └─ Ideal para producción
  │   │  │
  │   │  └─ Requisitos:
  │   │     ├─ NVIDIA GPU (RTX 30xx+, A100, etc.)
  │   │     ├─ CUDA Toolkit 11.8+
  │   │     └─ cuDNN 8.7+
  │   │
  │   └─ NO (GPU no disponible)
  │      ├─ device = "cpu"
  │      ├─ torch_dtype = torch.float32 (FP32 - full precision)
  │      │
  │      ├─ Ventajas:
  │      │  ├─ Funciona en cualquier máquina
  │      │  ├─ Compatible universal
  │      │  └─ No requiere drivers especiales
  │      │
  │      └─ Desventajas:
  │         ├─ 5-10x más lento
  │         ├─ Mayor consumo de memoria
  │         └─ Inadecuado para producción

Configuración recomendada:

┌─ CPU Configuration ────────────┐
│ device = "cpu"                 │
│ torch_dtype = torch.float32    │
│ batch_size = 1                 │
│ max_images/day = ~100          │
└────────────────────────────────┘

┌─ GPU Configuration ────────────┐
│ device = "cuda"                │
│ torch_dtype = torch.float16    │
│ batch_size = 4-8               │
│ max_images/day = ~1000         │
└────────────────────────────────┘

Tiempo de ejecución estimado (por imagen):
                CPU         GPU
Descarga modelo: 60-120s    10-20s
Procesamiento:   60-180s    5-15s
Total 1ª vez:    120-300s   15-35s
Total después:   60-180s    5-15s
```

---

## 6. ESTRUCTURA DE DATOS - BLIP-2 PROCESSING

```
                        BLIP-2 INPUT/OUTPUT FLOW

INPUT IMAGE:
  imagen.png (e.g., 1920x1080 pixels)
    ↓
  PIL.Image.convert("RGB")
    ├─ Pixel values: [0-255] per channel
    ├─ Shape: (H, W, 3)
    └─ Device: CPU

BLIP2PROCESSOR.process():
  ├─ Image processor:
  │  ├─ Resize → 224x224 (standard ViT input)
  │  ├─ Normalize:
  │  │  ├─ Mean = [0.48145466, 0.4578275, 0.40821073]
  │  │  └─ Std = [0.26862954, 0.26130258, 0.27577711]
  │  └─ Output: pixel_values (1, 3, 224, 224) FP32
  │
  └─ Text processor (prompt):
     ├─ Tokenize prompt string
     ├─ Special tokens: [CLS], [SEP], [PAD]
     └─ Output: input_ids (1, seq_len)

TENSORS TO DEVICE:
  ├─ pixel_values → device (GPU or CPU)
  ├─ input_ids → device
  └─ attention_mask → device

BLIP2MODEL.generate():
  ├─ Image encoder (ViT):
  │  ├─ Input: pixel_values (1, 3, 224, 224)
  │  └─ Output: image_embeddings (1, 257, 768)
  │
  ├─ Text prompt encoder:
  │  ├─ Input: input_ids (1, seq_len)
  │  └─ Output: text_embeddings (1, seq_len, 768)
  │
  ├─ Cross-attention fusion
  │
  ├─ Autoregressive decoding (max_new_tokens=150):
  │  ├─ Iteración 1: predict token 1
  │  ├─ Iteración 2: predict token 2 (dado token 1)
  │  ├─ ...
  │  └─ Iteración 150: predecir token 150 o [EOS]
  │
  └─ Output: generated_ids (1, total_length)

PROCESSOR.decode():
  ├─ generated_ids → tokens
  ├─ Skip special tokens: [CLS], [SEP], [PAD], [EOS]
  └─ Output: description_text (string)

OUTPUT TEXT:
  "A group of elderly men in formal attire standing in front of a
   historic building, likely from the mid-20th century. The photograph
   appears to be a formal portrait or documentation of a significant event.
   The black and white photograph shows architectural details..."

Tensor shapes throughout pipeline:
  └─ pixel_values:      (batch=1, channels=3, H=224, W=224)
  └─ image_embeddings:  (batch=1, seq=257, dim=768)
  └─ input_ids:         (batch=1, seq=variable)
  └─ generated_ids:     (batch=1, seq=variable)
```

---

## 7. ESTADÍSTICAS DE DATOS - PORTFOLIO CATALOGUING

```
                    PORTFOLIO DATASET STATISTICS

┌─ Portfolio_22_08_2025.txt ────────────────────────────────┐
│                                                           │
│ Total Registros: 191,716                                  │
│ Codificación: UTF-8                                       │
│ Delimitador: Tab (\t)                                     │
│ Tamaño archivo: ~15-20 MB                                 │
│                                                           │
│ Columnas:                                                 │
│  ├─ NODE_ID (Integer): Identificador único               │
│  ├─ FOLDER (String): Colección/Fondo                     │
│  ├─ NAME (String): Nombre del item                       │
│  └─ URL (String): Enlace al recurso digital              │
│                                                           │
│ Distribución por Colección:                              │
│  ├─ Fondo Fotográfico Nereo López: ~12,000 registros     │
│  ├─ Fondo Fotográfico Hermann F. Birkigt: ~8,000 registros│
│  ├─ Fondo Fotográfico Manuel H.: ~5,000 registros        │
│  └─ Otros fondos: ~166,716 registros                     │
│                                                           │
│ URLs:                                                     │
│  ├─ Formato: HTTPS                                       │
│  ├─ Dominio: bnco.ent.sirsi.net                          │
│  ├─ Patrón: /client/en_US/search/asset/{NODE_ID}/0      │
│  └─ Todas únicas: ✅ SÍ (asumido)                         │
│                                                           │
└───────────────────────────────────────────────────────────┘

Ejemplo de registro Portfolio:
┌────────────────────────────────────────────────────────┐
│ 243 | Fondo Fotográfico Nereo López | frojaspinilla_318│
│     | https://bnco.ent.sirsi.net/client/en_US/...      │
└────────────────────────────────────────────────────────┘

Analítica esperada (módulo 2):
├─ Registros solo en Symphony:  ~250-500 (1-3%)
├─ Registros solo en Portfolio: ~50-100 (0.05-0.1%)
├─ Registros en ambos:          ~1400-1500 (80-85%)
└─ Sin coincidir (NA values):   ~189k (98%)
   (El portfolio tiene muchos más registros que Symphony)
```

---

## 8. DIAGRAMA DE DEPENDENCIAS

```
                    DEPENDENCY GRAPH - CATALOGIA MVP

┌─────────────────────────────────────────────────────────┐
│                    prueba.py                            │
│              (Catalogación BLIP-2)                      │
│                                                         │
│  Importa:                                              │
│    ├─ ssl (stdlib)                                      │
│    ├─ urllib3 ← requests ← transformers               │
│    ├─ os (stdlib)                                       │
│    ├─ transformers ← tokenizers, datasets,             │
│    │                 huggingface-hub, tqdm              │
│    ├─ PIL ← pillow                                      │
│    └─ torch ← numpy                                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│          Comparativo_Portfolio_Symphony.py              │
│          (Análisis de Catálogos)                        │
│                                                         │
│  Importa:                                              │
│    └─ pandas ← numpy, openpyxl                         │
│                                                         │
└─────────────────────────────────────────────────────────┘

Árbol de dependencias (transitive):

core dependencies:
  ├─ transformers 4.35.0
  │  ├─ numpy >=1.19.0
  │  ├─ tokenizers >=0.11.0
  │  ├─ datasets >=2.0.0
  │  ├─ huggingface-hub >=0.10.0
  │  │  ├─ requests >=2.25.0
  │  │  ├─ filelock >=3.0.0
  │  │  └─ pyyaml >=5.1.0
  │  ├─ regex >=2021.0.0
  │  ├─ tqdm >=4.0.0
  │  └─ packaging >=20.0
  │
  ├─ torch 2.1.0
  │  ├─ numpy >=1.19.0
  │  ├─ typing-extensions >=4.0.0
  │  └─ sympy (optional)
  │
  ├─ pandas 2.1.1
  │  ├─ numpy >=1.23.2
  │  ├─ python-dateutil >=2.8.2
  │  ├─ pytz >=2020.1
  │  ├─ tzdata >=2022.1 (Windows)
  │  └─ openpyxl >=2.6.0 (para Excel)
  │
  ├─ Pillow 10.0.0
  │  └─ numpy >=1.23.5 (optional)
  │
  └─ urllib3 2.0.0
     ├─ certifi >=2017.4.17
     └─ pyOpenSSL (optional)

Total paquetes transitivos: ~25-30
Total tamaño instalación: ~2-4 GB (con modelos descargados)
```

---

## 9. MATRIZ DE COMPATIBILIDAD

```
                    COMPATIBILITY MATRIX

┌─ Software Support ────────────────────────────────────┐
│                                                      │
│  Python version:                                     │
│  ├─ 3.7: ✅ Soportado                               │
│  ├─ 3.8: ✅ Soportado                               │
│  ├─ 3.9: ✅ Soportado                               │
│  ├─ 3.10: ✅ Soportado (Recomendado)                │
│  ├─ 3.11: ✅ Soportado                              │
│  └─ 3.12: ⚠️ Parcial (transformers migración)       │
│                                                      │
│  OS support:                                         │
│  ├─ Windows 10/11: ✅ Soportado                      │
│  ├─ Linux (Ubuntu 18.04+): ✅ Soportado             │
│  ├─ macOS 10.14+: ✅ Soportado                       │
│  │  ├─ Intel: ✅ CPU/GPU                             │
│  │  ├─ Apple Silicon (M1/M2): ⚠️ CPU solo           │
│  │  └─ CUDA no disponible                           │
│  │                                                   │
│  GPU support:                                        │
│  ├─ NVIDIA (CUDA): ✅ Completo soporte              │
│  │  ├─ RTX 3090: ✅ Ideal                            │
│  │  ├─ RTX 3060: ✅ Bueno (~12 GB VRAM)             │
│  │  ├─ GTX 1080 Ti: ✅ Aceptable (11 GB VRAM)       │
│  │  └─ GTX 960: ❌ VRAM insuficiente (2 GB)         │
│  │                                                   │
│  ├─ AMD (HIP): ⚠️ Experimental (no testeado)        │
│  ├─ Intel Arc: ⚠️ Experimental                      │
│  ├─ Apple Metal: ⚠️ CPU fallback                    │
│  └─ Google TPU: ❌ No soportado                     │
│                                                      │
└──────────────────────────────────────────────────────┘

Matriz de Performance:

Device              | Memory | Speed | Cost | Recomendación
─────────────────────────────────────────────────────────
GPU RTX 3090        | 24 GB  | 10x  | $$$$ | ✅ Ideal
GPU RTX 3060        | 12 GB  | 8x   | $$   | ✅ Muy bueno
GPU RTX 2080        | 11 GB  | 7x   | $$   | ✅ Bueno
GPU V100            | 32 GB  | 12x  | $$$$ | ✅ Ideal (cloud)
CPU (i9-12900K)     | 64 GB  | 1x   | $$$  | ⚠️ Desarrollo
CPU (i5-10400)      | 16 GB  | 1x   | $    | ❌ Muy lento
CPU (Laptop)        | 8 GB   | 1x   | $    | ❌ No viable
```

---

## 10. CASOS DE USO Y FLUJOS

```
                    USE CASES & WORKFLOWS

CASO 1: Catalogación Individual
────────────────────────────────
Entrada: Una imagen PNG/JPG
Flujo:   Imagen → BLIP-2 → Descripción (texto)
Tiempo:  5-180 segundos (GPU/CPU)
Salida:  Impreso en consola
Usuario: Archivero, catalogador
Limitación: ❌ No persiste, no exporta

CASO 2: Catalogación Batch
────────────────────────────
Entrada: Carpeta con 100+ imágenes ❌ NO IMPLEMENTADO
Flujo:   Para cada imagen: Procesar → Guardar resultado
Tiempo:  ~1-3 horas (GPU)
Salida:  Base de datos o Excel
Usuario: Técnico de IA
Limitación: Requiere modificación de código

CASO 3: Análisis de Catálogos
──────────────────────────────
Entrada: Symphony_30_07_2025.csv + Portfolio_22_08_2025.txt
Flujo:   Leer → Expandir URLs → Merge → Exportar Excel
Tiempo:  2-5 segundos
Salida:  Comparativo_Symphony_Portfolio.xlsx
Usuario: Encargado de catálogos
Limitación: Merge simple (sin validación de duplicados)

CASO 4: Integración con Workflow
──────────────────────────────────
Entrada: API REST (por implementar)
Flujo:   HTTP POST /catalogar → Modelo → Respuesta JSON
Tiempo:  30-60 segundos
Salida:  JSON con metadatos catalogados
Usuario: Aplicación cliente
Limitación: ❌ No existe aún, requiere FastAPI + async

CASO 5: Validación de Calidad
──────────────────────────────────
Entrada: Descripción generada vs. Descripción manual
Validaciones: ❌ NO IMPLEMENTADAS
─ Largo mínimo de descripción
─ Detección de lenguaje (debe ser EN)
─ Extracción de entidades nombradas
─ Similitud con metadatos existentes
```

---

**Documento compilado:** 18 de enero de 2026  
**Scope:** Diagramas técnicos y arquitectura MVP
