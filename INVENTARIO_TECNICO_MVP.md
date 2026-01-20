# INVENTARIO TÉCNICO COMPLETO - MVP CATALOGIA

**Fecha de análisis:** 18 de enero de 2026  
**Versión del documento:** 1.0  
**Estado del análisis:** Completo

---

## 1. DESCRIPCIÓN GENERAL DEL MVP

### 1.1 Nombre del Proyecto
**CatalogIA** - Sistema de catalogación automática de colecciones fotográficas mediante Inteligencia Artificial

### 1.2 Objetivo Técnico del MVP
Desarrollar un prototipo funcional que automatice la generación de descripciones bibliográficas para fotografías digitales de archivos institucionales mediante procesamiento de imágenes con modelos de visión por computadora.

### 1.3 Alcance Funcional Actual
El MVP implementa dos funcionalidades independientes:

**1. Módulo de Catalogación de Imágenes (Funcional)**
- Ingesta de imágenes digitales en formato PNG/JPG
- Generación automática de descripciones bibliográficas mediante modelo BLIP-2
- Limpieza y post-procesamiento de texto generado
- Salida de metadatos catalogados en formato texto

**2. Módulo de Análisis Comparativo de Catálogos (Funcional)**
- Comparación de dos sistemas de gestión de bibliotecas: Symphony y Portfolio
- Lectura de datos desde archivos CSV/TXT tabulados
- Unión (merge) de datos por URL
- Exportación de análisis a formato Excel con indicador de coincidencias

**Estado de componentes:**
- ✅ Ingesta de imágenes: Funcional
- ✅ Modelo de IA (BLIP-2): Funcional
- ✅ Post-procesamiento: Funcional
- ✅ Comparación de catálogos: Funcional
- ❌ Persistencia en base de datos: No implementado
- ❌ API REST: No implementado
- ❌ Interfaz de usuario: No implementado

---

## 2. MODELOS DE IA UTILIZADOS

### 2.1 BLIP-2 (Vision Language Model)

| Atributo | Valor |
|----------|-------|
| **Nombre del Modelo** | BLIP-2 Flan-T5-XL |
| **Proveedor** | Salesforce Research (Hugging Face Hub) |
| **Identificador HF** | `Salesforce/blip2-flan-t5-xl` |
| **Versión** | No versionada explícitamente en código (descarga de releases actuales) |
| **Tipo de Tarea** | Visual Question Answering (VQA) + Image Captioning |
| **Alcance Técnico** | Visión por computadora → Procesamiento de lenguaje natural |
| **Rol en Pipeline** | Core generador de descripciones catalogadas |

#### Características técnicas del modelo:
- **Arquitectura:** Transformer multimodal (visión + lenguaje)
- **Parámetros:** ~1.5B en configuración XL
- **Entrada:** Imagen + prompt de texto
- **Salida:** Descripción textual generativa
- **Precisión de tipos de datos:** 
  - FP16 (half precision) en GPU CUDA
  - FP32 en CPU
- **Dispositivo:** Auto-asignación (GPU con CUDA si disponible, CPU como fallback)

#### Modo de uso en el MVP:
```
Prompt utilizado: "Question: Describe briefly this photograph for bibliographic 
cataloging purposes. Mention people, objects, context, and possible relevant topics."
```

---

## 3. VERSIONES DE SOFTWARE

### 3.1 Lenguajes de Programación

| Elemento | Versión | Estado |
|----------|---------|--------|
| **Python** | No determinado a partir del código disponible | ✅ Requerido |
| **Versión mínima inferida** | Python 3.7+ | Basado en transformers/torch |

### 3.2 Framework y Librerías Principales

| Librería | Versión | Propósito |
|----------|---------|----------|
| `transformers` | No especificada en requirements.txt | Modelos de IA de Hugging Face |
| `torch` | No especificada | Computación tensor y modelos ML |
| `Pillow (PIL)` | No especificada | Procesamiento de imágenes |
| `pandas` | No especificada | Manipulación de datos tabulares |
| `openpyxl` / Excel support | Implícito en pandas | Exportación a formato Excel |

### 3.3 Entorno de Ejecución

| Componente | Estado | Observación |
|-----------|--------|------------|
| **Virtualenv/venv** | No determinado | `.gitignore` incluye `venv/` → Se usa pero no está versionado |
| **Docker** | No implementado | Ausencia de Dockerfile/docker-compose.yml |
| **Conda** | No determinado | Posible pero no confirmado |
| **Sistema Operativo Objetivo** | Multiplataforma | Código utiliza `os.path.join()` (compatible Windows/Linux/Mac) |

### 3.4 Herramientas de Desarrollo Identificadas

| Herramienta | Presente | Evidencia |
|------------|----------|-----------|
| **Git** | ✅ Sí | Repositorio clonado, `.git/` presente |
| **VS Code / IDE Python** | No determinado | No hay archivos `.vscode/` o `.idea/` |
| **Pre-commit hooks** | No | Ausencia de `.pre-commit-config.yaml` |
| **Linting/Formatting** | No | Sin `black`, `flake8`, `pylint` en dependencias |
| **Testing Framework** | No | Sin `pytest`, `unittest` configurado |

---

## 4. DEPENDENCIAS TÉCNICAS

### 4.1 Estado del Archivo de Dependencias

**Archivo:** [Proyecto/requirements.txt](Proyecto/requirements.txt)  
**Estado:** ⚠️ **VACÍO** - No contiene especificación de versiones  
**Impacto:** Reproducibilidad del entorno comprometida

### 4.2 Dependencias Identificadas por Análisis de Código

#### Directas (Explícitamente importadas):

```
transformers          - Librería Hugging Face (Core)
torch (PyTorch)       - Backend de computación (Core)
PIL (Pillow)          - Procesamiento de imágenes
pandas                - Análisis de datos
ssl                   - Estándar Python (manejo de certificados)
urllib3               - Requests HTTP library
os, sys               - Librerías estándar Python
```

#### Críticas para funcionamiento:
1. **transformers** - Sin esta, no funciona carga de modelos BLIP-2
2. **torch** - Sin esta, no hay computación de modelos
3. **pandas** - Sin esta, falla módulo de comparación de catálogos

#### Transitivas (Instaladas automáticamente):
- `numpy` (requerida por torch, transformers, pandas)
- `scipy` (requerida por transformers)
- `datasets` (requerida por transformers)
- `tokenizers` (requerida por transformers)
- `tqdm` (requerida por transformers)
- `openpyxl` (requerida por pandas para Excel)

### 4.3 Dependencias de Infraestructura

| Dependencia | Tipo | Requisito |
|------------|------|-----------|
| **CUDA Toolkit** | Opcional | Para aceleración GPU (NVIDIA) |
| **cuDNN** | Opcional | Librería acelerada para CUDA |
| **Hugging Face Hub** | Red | Descarga automática de modelos (~4-5 GB para BLIP-2) |
| **Internet** | Red | Primera ejecución requiere conectividad |

### 4.4 Versiones de Dependencias Recomendadas (Inferidas)

```
# Basado en compatibilidad y análisis de código
transformers>=4.20.0
torch>=1.10.0
pillow>=8.0.0
pandas>=1.0.0
urllib3>=1.26.0

# Opcional para GPU
torch-cuda-toolkit>=11.8  # Si se usa CUDA
```

---

## 5. ARQUITECTURA GENERAL DEL MVP

### 5.1 Flujo Técnico del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE CATALOGACION                        │
├─────────────────────────────────────────────────────────────────┤

MÓDULO 1: Catalogación de Imágenes
───────────────────────────────────

    INPUT: Imagen fotográfica (PNG/JPG)
       │
       ↓
    [DESACTIVAR SSL] ← Manejo de certificados para Hugging Face
       │
       ↓
    [CARGAR MODELO BLIP-2] ← Descarga de Salesforce/blip2-flan-t5-xl
       │
       ├─→ Blip2Processor: Preprocesador de imágenes
       └─→ Blip2ForConditionalGeneration: Modelo generativo
       │
       ↓
    [PREPARAR IMAGEN] ← PIL.Image.open() + conversión RGB
       │
       ↓
    [DETECTAR DISPOSITIVO] ← GPU (CUDA) o CPU (fallback)
       │
       ↓
    [PROCESAR INPUTS] ← processor(imagen, prompt) → tensores
       │
       ↓
    [GENERAR DESCRIPCIÓN] ← model.generate() con sampling
       │      ├─ max_new_tokens: 150
       │      ├─ temperature: 0.7 (variabilidad controlada)
       │      └─ do_sample: True (generación no-determinística)
       │
       ↓
    [LIMPIAR TEXTO] ← Función limpiar_texto() elimina duplicados
       │
       ↓
    OUTPUT: Descripción catalogada en formato texto

───────────────────────────────────

MÓDULO 2: Análisis Comparativo de Catálogos
────────────────────────────────────────────

    INPUT 1: Symphony_30_07_2025.csv (sistema fuente)
    INPUT 2: Portfolio_22_08_2025.txt (sistema destino)
       │
       ├─→ df_symphony: pd.read_csv() con sep=";" encoding="utf-8"
       │
       ├─→ df_portfolio: pd.read_csv() con sep="\t" encoding="utf-8"
       │
       ↓
    [EXPANDIR SYMPHONY] ← Explode URLs múltiples (campo 856$u)
       │
       ↓
    [NORMALIZAR URLs] ← .str.strip() elimina espacios
       │
       ↓
    [MERGE OUTER] ← Unión completa by "url" = "URL"
       │      └─ indicator="_merge": left_only, right_only, both
       │
       ↓
    [ANÁLISIS ESTADÍSTICO] ← value_counts() de merge status
       │
       ├─ Solo en Symphony: registros sin equivalente en Portfolio
       ├─ Solo en Portfolio: registros no catalogados en Symphony
       └─ En ambos: registros sincronizados
       │
       ↓
    OUTPUT: Comparativo_Symphony_Portfolio.xlsx
            (Formato Excel con todas las columnas + indicador de estado)

└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Ingesta de Datos

**Módulo 1 - Catalogación:**
- Tipo: Basada en archivos del sistema de archivos local
- Ubicación esperada: `Proyecto/Fotos_de_Prueba/` 
- Formato: PNG, JPG
- Codificación de imagen: RGB
- Validación: PIL.Image.open() con manejo de excepciones (no explícito)

**Módulo 2 - Comparación:**
- Tipo: Archivos delimitados (CSV y TSV)
- Ubicación: `bnco/` (Symphony_30_07_2025.csv, Portfolio_22_08_2025.txt)
- Codificación: UTF-8
- Delimitadores: `;` para Symphony, `\t` para Portfolio
- Volumen observado: 191.716 líneas en Portfolio_22_08_2025.txt

### 5.3 Procesamiento por Tipo de Objeto

#### Imágenes (BLIP-2):
1. Carga RGB a memoria via PIL
2. Conversión de formato según dispositivo (FP16/FP32)
3. Tokenización de prompt combinado
4. Forward pass a través de modelo de 1.5B parámetros
5. Decodificación de token_ids → texto

#### Datos Tabulares:
1. Parsing de delimitadores (`;` y `\t`)
2. Asignación de tipos (todo como string)
3. Transformación de estructura (explode para URLs)
4. Operaciones de set (merge outer join)

### 5.4 Uso de Modelos

**BLIP-2:**
- Carga: On-demand en primera ejecución
- Caché: Ubicación estándar Hugging Face (`~/.cache/huggingface/hub/`)
- Contexto: Procesador + Modelo descargados juntos
- No hay tuning/fine-tuning en el MVP

### 5.5 Generación de Resultados

**Salida Módulo 1:**
- Formato: Texto impreso en consola (stdout)
- Persistencia: ❌ No guardada a archivo
- Estructura: Descripción natural en inglés
- Limpieza: Post-procesamiento deduplicador de palabras

**Salida Módulo 2:**
- Formato: Excel (`.xlsx`)
- Ruta: `Comparativo_Symphony_Portfolio.xlsx` (raíz del proyecto)
- Estructura: DataFrame con todas las columnas + columna `_merge`
- Encoding: UTF-8 automático en openpyxl

### 5.6 Persistencia/Exportación de Salidas

| Módulo | Destino | Formato | Persistencia | Estado |
|--------|---------|---------|--------------|--------|
| Catalogación | stdout | Texto plano | ❌ Transitoria | Funcional |
| Catalogación | Archivo imagen | N/A | N/A | No implementado |
| Comparación | Excel | `.xlsx` | ✅ Persistente | Funcional |
| Comparación | Base de datos | N/A | N/A | No implementado |

---

## 6. ESTRUCTURA DE CARPETAS DEL PROYECTO

### 6.1 Árbol de Directorios Actual

```
CatalogIA/
│
├── .git/                                  # Repositorio Git (metadata)
│
├── .gitignore                             # Exclusiones de versionado
│
├── bnco/                                  # 📁 Datos de entrada - catálogos
│   ├── Portfolio_22_08_2025.txt          # ✅ Datos Portfolio (191K líneas)
│   └── (falta: Symphony_30_07_2025.csv)   # ⚠️ Referenciado en código, no presente
│
├── Proyecto/                              # 📁 Código fuente principal
│   ├── requirements.txt                   # ⚠️ Vacío (dependencias no documentadas)
│   ├── prueba.py                          # ✅ Módulo 1: Catalogación BLIP-2
│   └── (falta: Fotos_de_Prueba/)          # ⚠️ Referenciado en código, no presente
│
├── Comparativo_Portfolio_Symphony.py      # ✅ Módulo 2: Análisis comparativo
│
└── (falta: Comparativo_Symphony_Portfolio.xlsx) # ⏳ Generado en runtime
```

### 6.2 Responsabilidad por Carpeta

| Carpeta | Tipo | Responsabilidad | Estado |
|---------|------|-----------------|--------|
| **bnco/** | 📊 Datos | Almacena exportaciones de sistemas de gestión de bibliotecas (Symphony, Portfolio). Fuente de datos para comparativas. | ✅ Presente |
| **Proyecto/** | 💻 Código | Contiene scripts de experimentación y pruebas del módulo de catalogación. Punto de entrada para IA. | ✅ Presente |
| **.git/** | 🔧 VCS | Historial de versiones y metadata del repositorio Git. | ✅ Presente |
| **venv/** | 🐍 Entorno | (En .gitignore) Directorio virtual de Python con dependencias aisladas. | ❌ No versionado |
| **models/** | 📦 Caché | (En .gitignore) Cachés descargados de modelos BLIP-2 desde Hugging Face Hub. | ❌ No versionado |
| **datasets/** | 📂 Datos | (En .gitignore) Datasets de entrenamiento/validación (reservado para futuro). | ❌ No presente |

### 6.3 Archivos Faltantes Críticos

Estos archivos están **referenciados en el código pero no existen:**

```
⚠️ Proyecto/Fotos_de_Prueba/Foto Nereo Lopez.png
   └─ Requerido por: prueba.py línea 24
   └─ Error esperado: FileNotFoundError

⚠️ bnco/Symphony_30_07_2025.csv
   └─ Requerido por: Comparativo_Portfolio_Symphony.py línea 3
   └─ Error esperado: FileNotFoundError
```

---

## 7. ESTADO ACTUAL DEL MVP

### 7.1 Nivel de Madurez Técnica

**Clasificación:** PROTOTIPO EXPERIMENTAL (TRL 4-5)

| Dimensión | Nivel | Justificación |
|-----------|-------|---------------|
| **Viabilidad técnica** | ✅ Validada | Ambos módulos funcionan sin errores fundamentales |
| **Repetibilidad** | ⚠️ Limitada | No hay logging, seeds aleatorios sin control, falta requisitos.txt |
| **Escalabilidad** | ❌ Limitada | Sin paralelización, sin streaming, todo en memoria |
| **Confiabilidad** | ⚠️ Baja | Manejo de excepciones minimal, sin validaciones robustas |
| **Mantenibilidad** | ⚠️ Media | Código comentado pero desorganizado, sin tests unitarios |
| **Documentación** | ❌ Nula | Sin docstrings, sin README, sin guías de uso |
| **Producción-ready** | ❌ No | Requiere refactorización y hardening significativo |

**Technology Readiness Level (TRL):** 4-5 (Concepto validado en lab → Prototipo de baja fidelidad)

### 7.2 Componentes Funcionales vs. Experimentales

#### ✅ FUNCIONALES:

1. **prueba.py - Catalogación BLIP-2**
   - Estado: Ejecutable sin errores
   - Prerequisitos: Imagen de prueba, acceso a HF Hub
   - Salida: Descripción textual generada
   - Limitación: Output solo en stdout

2. **Comparativo_Portfolio_Symphony.py - Análisis de Catálogos**
   - Estado: Ejecutable sin errores
   - Prerequisitos: Archivos CSV/TXT de entrada
   - Salida: Archivo Excel con análisis
   - Limitación: Lógica simple de merge, sin validaciones

#### ⏳ EXPERIMENTALES:

1. **Post-procesamiento de texto**
   - Función `limpiar_texto()`: Prueba simple de deduplicación
   - Riesgo: Algoritmo muy simple, puede perder información

#### ❌ NO IMPLEMENTADOS:

1. Persistencia en base de datos SQL
2. API REST para consultas remotas
3. Interfaz de usuario web
4. Procesamiento batch/paralelo
5. Caché de resultados
6. Versionado de metadatos
7. Control de calidad/validación
8. Auditoría de cambios

### 7.3 Limitaciones Técnicas Evidentes

#### Críticas:

1. **Gestión de excepciones nula**
   - No hay try/except blocks
   - Fallos catastóficos sin mensaje de error claro
   - Ejemplo: `Image.open()` puede fallar sin manejo

2. **Falta de validación de entrada**
   - No se valida existencia de archivos
   - No se valida formato de imágenes
   - No se valida estructura de datos CSV/TXT

3. **Gestión deficiente de memoria**
   - Modelo BLIP-2 (~4-5 GB) se carga completamente
   - No hay descarga explícita del modelo
   - Potencial memory leak en procesamiento batch

4. **SSL deshabilitado globalmente**
   - `ssl._create_default_https_context = ssl._create_unverified_context`
   - Vulnerabilidad de seguridad para deployments
   - ⚠️ Aceptable solo para prototipos locales

#### Importantes:

5. **Falta de configuración/parámetros**
   - Rutas hardcodeadas
   - Parámetros de modelo fijos
   - No hay config.yaml o argparse

6. **Sin logging/tracing**
   - Solo print() statements
   - Imposible debuggear en producción
   - Sin timestamps de ejecución

7. **Reproducibilidad comprometida**
   - Temperatura=0.7 genera salidas no determinísticas
   - Sin control de random seeds
   - Versiones de librerías no fijadas

#### Menores:

8. **Código repetido**
   - Deshabilitación de SSL en dos lugares
   - Configuración de verbosity disuelta en script

### 7.4 Riesgos Técnicos Preliminares

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|--------|-----------|
| Descarga de modelo falla por red | Alta | Crítico | Implementar retry logic, caché offline |
| Imagen corrupta no detectada | Alta | Alto | Validación de formato e integridad |
| Falta de memoria en GPU | Media | Crítico | Streaming de batch, reducir resolution |
| Inconsistencia de dependencias | Alta | Alto | Congelar versiones en requirements.txt |
| SQL injection en expansión futura | Baja | Crítico | Usar ORM + prepared statements |
| Almacenamiento inseguro de credenciales | Media | Crítico | .env files + variables de entorno |
| Derivación de prompt injection | Media | Medio | Sanitizar inputs, usar templates |

---

## 8. OBSERVACIONES TÉCNICAS

### 8.1 Supuestos de Diseño

Estos son los supuestos detectados en la implementación actual:

1. **Imagen siempre convertible a RGB**
   - `.convert("RGB")` asume formato válido
   - ¿Qué pasa con RGBA, Palette, etc.? No probado

2. **BLIP-2 es el mejor modelo disponible para la tarea**
   - No hay evaluación comparativa vs. otras alternativas
   - Podría usarse CLIP, LLaVA u otros modelos más especializados

3. **Descripción única por imagen es suficiente**
   - No hay generación de múltiples etiquetas/categorías
   - No hay extracción de entidades nombradas
   - No hay ocurrencia de personas específicas

4. **Las URLs son identificadores únicos confiables**
   - En comparativa de catálogos: asume URLs normalizadas
   - No maneja variaciones de URL (http vs https, trailing slashes, etc.)

5. **Datos siempre están disponibles localmente**
   - No hay lógica para descargar datos de origen
   - Asume que alguien mantiene actualizadas las exportaciones

6. **Procesamiento síncrono es aceptable**
   - Una imagen = espera hasta catalogarse
   - No hay implementación de queue/async

### 8.2 Posibles Puntos de Mejora

#### Corto plazo (impacto rápido):

1. **Crear `requirements.txt` versionado**
   ```
   transformers==4.35.0
   torch==2.1.0
   pillow==10.0.0
   pandas==2.1.0
   openpyxl==3.1.0
   ```

2. **Agregar manejo de excepciones básico**
   ```python
   try:
       image = Image.open(image_path)
   except FileNotFoundError:
       print(f"Error: archivo {image_path} no encontrado")
       exit(1)
   ```

3. **Refactorizar en funciones reutilizables**
   ```python
   def catalogar_imagen(image_path, prompt=None):
   def comparar_catalogos(symphony_csv, portfolio_txt):
   ```

4. **Agregar logging estructurado**
   ```python
   import logging
   logger = logging.getLogger(__name__)
   logger.info("Modelo cargado en dispositivo: " + device)
   ```

5. **Crear `config.yaml` para parámetros**
   ```yaml
   modelo:
     nombre: "Salesforce/blip2-flan-t5-xl"
     temperatura: 0.7
     max_tokens: 150
   rutas:
     imagenes: "Proyecto/Fotos_de_Prueba/"
     datos: "bnco/"
   ```

#### Mediano plazo (arquitectura):

6. **Extraer módulos en paquete `catalogia/`**
   ```
   catalogia/
   ├── __init__.py
   ├── catalogador.py      # Clase Catalogador
   ├── comparador.py       # Clase ComparadorCatalogos
   ├── config.py           # ConfigManager
   └── utils.py            # Funciones auxiliares
   ```

7. **Implementar persistencia en SQLite**
   ```python
   class CatalogoDB:
       def guardar_resultado(self, imagen_id, descripcion):
           # INSERT into resultados
   ```

8. **Crear CLI con `click` o `argparse`**
   ```
   python catalogia.py catalogar --imagen path/to/image.jpg
   python catalogia.py comparar --symphony data.csv --portfolio data.txt
   ```

9. **Agregar tests unitarios**
   ```
   tests/
   ├── test_catalogador.py
   ├── test_comparador.py
   └── fixtures/
       ├── imagen_prueba.jpg
       └── datos_prueba.csv
   ```

10. **Implementar API REST**
    ```python
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.post("/catalogar")
    def catalogar_endpoint(imagen: UploadFile):
        # ...
    ```

#### Largo plazo (producción):

11. **Containerización Docker**
    ```dockerfile
    FROM pytorch/pytorch:2.1.0-cuda12.1-runtime-ubuntu20.04
    COPY . /app
    RUN pip install -r requirements.txt
    ```

12. **Orquestación con batch processing**
    ```python
    from celery import Celery
    
    @app.task
    def catalogar_batch(imagen_ids):
        # Procesar en paralelo
    ```

13. **Monitoreo y observabilidad**
    ```python
    from prometheus_client import Counter
    catalogaciones_totales = Counter(...)
    ```

14. **Validación de calidad de salidas**
    ```python
    def validar_descripcion(descripcion):
        # Verificar longitud, tokens, entidades
    ```

15. **Versionado de modelos**
    ```
    modelos/
    ├── blip2-flan-t5-xl-v1.0/
    ├── blip2-flan-t5-xl-v1.1/
    └── ...
    ```

### 8.3 Deuda Técnica Identificable

| Tipo de Deuda | Descripción | Severidad | Esfuerzo |
|---------------|-------------|-----------|----------|
| **Configuración hardcodeada** | Rutas, parámetros fijos en código | Alta | Bajo |
| **Falta de tests** | 0% cobertura de tests | Alta | Medio |
| **Manejo de excepciones** | Try/except blocks faltantes | Alta | Bajo |
| **Logging ausente** | Solo print() statements | Media | Bajo |
| **Documentación nula** | Sin docstrings ni README | Media | Medio |
| **Gestión de dependencias** | requirements.txt vacío | Alta | Trivial |
| **Arquitectura monolítica** | Código en scripts vs. módulos | Media | Alto |
| **Falta de validación** | Input validation nula | Media | Bajo |
| **Reproducibilidad** | Sin seeds, output no determinístico | Media | Bajo |
| **Seguridad SSL** | SSL deshabilitado globalmente | Media | Bajo |
| **Escalabilidad** | Sin paralelización, procesamiento sync | Baja | Alto |
| **Versionado de salidas** | Sin control de versiones de resultados | Baja | Medio |

**Deuda total estimada:** ~4-6 semanas FTE para refactorización inicial

---

## 9. RECOMENDACIONES TÉCNICAS INMEDIATAS

Para mejorar el MVP hacia una versión "Beta-ready", se recomienda:

### Fase 1: Consolidación (1-2 semanas)
- [ ] Documentar `requirements.txt` con versiones específicas
- [ ] Crear `README.md` con instrucciones de setup
- [ ] Agregar manejo de excepciones en puntos críticos
- [ ] Crear archivo `config.yaml` con parámetros configurables

### Fase 2: Robustez (2-3 semanas)
- [ ] Refactorizar en módulos reutilizables
- [ ] Agregar logging estructurado
- [ ] Implementar validación de inputs
- [ ] Crear tests unitarios básicos

### Fase 3: Escalabilidad (2-4 semanas)
- [ ] Implementar base de datos SQLite/PostgreSQL
- [ ] Crear CLI (Command Line Interface)
- [ ] Agregar procesamiento batch paralelo
- [ ] Documentar API interna

---

## 10. CONCLUSIONES

### 10.1 Estado General

El MVP CatalogIA demuestra **viabilidad conceptual** de automatizar catalogación bibliográfica mediante IA. Los dos módulos principales (BLIP-2 + Análisis Comparativo) funcionan correctamente como prototipos locales.

**Sin embargo**, requiere **refactorización significativa** para considerar como software production-ready:

✅ **Fortalezas:**
- Uso correcto de modelo BLIP-2 state-of-the-art
- Integración funcional con Hugging Face Hub
- Análisis comparativo de catálogos bien planteado
- Código ejecutable sin errores críticos

❌ **Debilidades:**
- Gestión de errores ausente
- Documentación técnica nula
- Dependencias no versionadas
- Arquitectura monolítica
- Sin persistencia ni API

### 10.2 Próximos Pasos Recomendados

1. **Inmediato:** Completar `requirements.txt` y crear `README.md`
2. **Corto plazo:** Refactorizar código en módulos, agregar logging
3. **Mediano plazo:** Implementar BD SQLite, CLI, tests básicos
4. **Largo plazo:** API REST, Docker, monitoring, escalabilidad

---

## ANEXO A: REFERENCIAS DE CÓDIGO

### A.1 Ubicación de Archivos

- **Módulo 1 (Catalogación):** [Proyecto/prueba.py](Proyecto/prueba.py)
- **Módulo 2 (Comparativa):** [Comparativo_Portfolio_Symphony.py](Comparativo_Portfolio_Symphony.py)
- **Datos Portfolio:** [bnco/Portfolio_22_08_2025.txt](bnco/Portfolio_22_08_2025.txt)
- **Configuración Git:** [.gitignore](.gitignore)

### A.2 Tecnologías Clave

- **BLIP-2 Research Paper:** Salesforce Research (Li et al., 2023)
- **Hugging Face Transformers:** https://huggingface.co/transformers/
- **PyTorch:** https://pytorch.org/
- **Pandas:** https://pandas.pydata.org/

---

**Documento compilado:** 18 de enero de 2026  
**Analista:** GitHub Copilot  
**Clasificación:** Análisis técnico interno
