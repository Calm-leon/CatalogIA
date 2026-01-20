# 🔴 PLAN DE ACCIÓN INMEDIATA - CATALOGIA MVP

**Fecha:** 18 de enero de 2026  
**Urgencia:** CRÍTICA  
**Estimado:** 1-2 semanas (5-8 horas de trabajo)

---

## ⚠️ SITUACIÓN ACTUAL

El MVP está **técnicamente viable** pero **NO LISTO para usar institucionalemente** sin correcciones inmediatas:

✅ **Funciona:**
- Catalogación con BLIP-2: Genera descripciones correctamente
- Comparación de catálogos: Produce análisis válido

❌ **PROBLEMAS CRÍTICOS:**
1. **requirements.txt VACÍO** ← Sin documentación de dependencias
2. **Sin manejo de excepciones** ← Fallos catastóficos
3. **Sin persistencia** ← Resultados no se guardan
4. **SSL deshabilitado globalmente** ← Riesgo de seguridad
5. **Código desorganizado** ← Difícil de mantener

---

## 🎯 ACCIONES INMEDIATAS (PRIORIDAD CRÍTICA)

### ACCIÓN 1: Generar requirements.txt
**Tiempo:** 15 minutos  
**Responsable:** Desarrollador  
**Criticidad:** 🔴 CRÍTICA

**Problema:**
```
❌ Proyecto/requirements.txt está VACÍO
└─ Imposible reproducir entorno en otra máquina
```

**Solución:**

1. **Activar entorno virtual:**
```powershell
cd Proyecto
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. **Instalar dependencias actuales:**
```powershell
pip install --upgrade pip
pip install torch transformers pandas pillow huggingface-hub
```

3. **Generar requirements.txt:**
```powershell
pip freeze > requirements.txt
```

4. **Revisar y limpiar:**
Editar [Proyecto/requirements.txt](Proyecto/requirements.txt):
```txt
# Core ML
torch==2.1.0
transformers==4.35.0
huggingface-hub==0.19.0

# Data
pandas==2.1.1
openpyxl==3.1.0

# Images
Pillow==10.0.0

# Utils
tqdm==4.66.0
filelock==3.13.0
```

5. **Verificar:**
```powershell
pip install -r requirements.txt
python -c "import torch, transformers; print('✅ OK')"
```

**✅ Resultado esperado:** Archivo requirements.txt con versiones congeladas

---

### ACCIÓN 2: Crear README.md básico
**Tiempo:** 20 minutos  
**Responsable:** Desarrollador  
**Criticidad:** 🔴 CRÍTICA

**Problema:**
```
❌ No hay instrucciones de cómo ejecutar el proyecto
└─ Imposible onboarding de nuevos usuarios
```

**Solución:**

Crear [README.md](README.md):

```markdown
# CatalogIA MVP

Sistema de catalogación automática de imágenes con IA.

## Instalación Rápida

### Windows
\`\`\`powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r Proyecto/requirements.txt
\`\`\`

### Linux/macOS
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip install -r Proyecto/requirements.txt
\`\`\`

## Uso

### Catalogar imagen
\`\`\`bash
cd Proyecto
python prueba.py
\`\`\`

### Comparar catálogos
\`\`\`bash
python Comparativo_Portfolio_Symphony.py
\`\`\`

## Requisitos
- Python 3.7+
- 8 GB RAM (16 GB recomendado con GPU)
- Internet para descargar modelo BLIP-2 (~5 GB)

## Estructura
- \`Proyecto/\` - Módulo de catalogación
- \`bnco/\` - Datos de entrada
\`\`\`

**✅ Resultado esperado:** README.md funcional

---

### ACCIÓN 3: Agregar manejo básico de excepciones
**Tiempo:** 30 minutos  
**Responsable:** Desarrollador  
**Criticidad:** 🔴 CRÍTICA

**Problema:**
```
❌ prueba.py no maneja errores
└─ Crash sin mensajes útiles si imagen no existe
```

**Solución:**

Editar [Proyecto/prueba.py](Proyecto/prueba.py) - Envolver main en try/except:

```python
def main():
    try:
        # Cargar imagen
        image_path = os.path.join(os.path.dirname(__file__), r"Fotos_de_Prueba\Foto Nereo Lopez.png")
        
        if not os.path.exists(image_path):
            print(f"❌ Error: Archivo no encontrado: {image_path}")
            return False
            
        image = Image.open(image_path).convert("RGB")
        
        # ... resto del código ...
        
        return True
        
    except FileNotFoundError as e:
        print(f"❌ Error de archivo: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
```

Similarly para [Comparativo_Portfolio_Symphony.py](Comparativo_Portfolio_Symphony.py):

```python
def main():
    try:
        df_symphony = pd.read_csv("bnco/Symphony_30_07_2025.csv", ...)
        # ... resto ...
        return True
    except FileNotFoundError as e:
        print(f"❌ Error: Archivo no encontrado: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
```

**✅ Resultado esperado:** Mensajes de error claros en lugar de crashes

---

### ACCIÓN 4: Crear config.yaml centralizado
**Tiempo:** 25 minutos  
**Responsable:** Desarrollador  
**Criticidad:** 🟠 ALTA

**Problema:**
```
⚠️ Rutas y parámetros hardcodeados en scripts
└─ Difícil de cambiar, no escalable
```

**Solución:**

Crear [Proyecto/config.yaml](Proyecto/config.yaml):

```yaml
# CatalogIA Configuration

# Modelo BLIP-2
modelo:
  nombre: "Salesforce/blip2-flan-t5-xl"
  temperatura: 0.7
  max_tokens: 150
  do_sample: true

# Rutas
rutas:
  imagenes: "Fotos_de_Prueba"
  datos: "bnco"
  salida: "resultados"

# Sistema
sistema:
  usar_gpu: true
  verbosity: "error"
  timeout_segundos: 300

# Catálogos
catalogos:
  symphony:
    archivo: "Symphony_30_07_2025.csv"
    separador: ";"
    codificacion: "utf-8"
  portfolio:
    archivo: "Portfolio_22_08_2025.txt"
    separador: "\t"
    codificacion: "utf-8"
```

Crear [Proyecto/load_config.py](Proyecto/load_config.py):

```python
import yaml

def cargar_config(ruta="config.yaml"):
    with open(ruta, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# Uso en prueba.py:
# config = cargar_config()
# processor = Blip2Processor.from_pretrained(config['modelo']['nombre'])
```

**✅ Resultado esperado:** Archivo de configuración centralizado

---

## 🔧 ACCIONES SECUNDARIAS (SEMANA 1)

### ACCIÓN 5: Agregar logging estructurado
**Tiempo:** 45 minutos  
**Responsable:** Desarrollador  
**Criticidad:** 🟠 ALTA

**Cambio:**

Reemplazar `print()` con logging:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Uso:
logger.info("Modelo cargado en dispositivo: " + device)
logger.warning("Imagen no encontrada, usando fallback")
logger.error("Error al procesar imagen")
```

**✅ Beneficio:** Debugging más fácil, logs grabados

---

### ACCIÓN 6: Crear script de verificación del entorno
**Tiempo:** 30 minutos  
**Responsable:** Desarrollador  
**Criticidad:** 🟡 MEDIA

**Crear [verify_env.py](Proyecto/verify_env.py):**

```python
#!/usr/bin/env python
import sys
import torch
import transformers

print("=" * 60)
print("VERIFICACIÓN DE ENTORNO CATALOGIA")
print("=" * 60)

tests = [
    ("Python", f"{sys.version_info.major}.{sys.version_info.minor}+", 
     sys.version_info >= (3, 7)),
    ("PyTorch", torch.__version__, True),
    ("Transformers", transformers.__version__, True),
    ("GPU disponible", "✅ CUDA" if torch.cuda.is_available() else "❌ CPU", True),
]

for name, version, ok in tests:
    status = "✅ OK" if ok else "❌ FALLO"
    print(f"{name:20} {version:30} {status}")

print()
print("✅ Entorno listo" if all(ok for _, _, ok in tests) else "❌ Problemas encontrados")
```

**Uso:**
```bash
python verify_env.py
```

**✅ Beneficio:** Verificación rápida antes de ejecución

---

### ACCIÓN 7: Documentar el código existente
**Tiempo:** 60 minutos  
**Responsable:** Desarrollador  
**Criticidad:** 🟡 MEDIA

**Agregar docstrings a funciones:**

En [Proyecto/prueba.py](Proyecto/prueba.py):

```python
def catalogar_imagen(imagen_path, prompt=None, dispositivo=None):
    """
    Catalogar una imagen usando BLIP-2.
    
    Args:
        imagen_path (str): Ruta a la imagen (PNG/JPG)
        prompt (str, optional): Prompt personalizado. Default: prompt bibliográfico
        dispositivo (str, optional): 'cuda' o 'cpu'. Default: detectar automáticamente
        
    Returns:
        str: Descripción catalogada en inglés
        
    Raises:
        FileNotFoundError: Si la imagen no existe
        ValueError: Si el formato no es soportado
        RuntimeError: Si hay error en el modelo
        
    Examples:
        >>> desc = catalogar_imagen("foto.jpg")
        >>> print(desc)
        "A photograph of people in a formal setting..."
    """
    # código aquí
```

**✅ Beneficio:** Código autodocumentado, mejor IDE support

---

## 📋 CHECKLIST DE ACCIÓN INMEDIATA

### Semana 1 - Sprint 0 (Consolidación)

- [ ] **ACCIÓN 1:** Generar requirements.txt (15 min)
  - [ ] Instalar dependencias
  - [ ] Ejecutar `pip freeze`
  - [ ] Revisar y limpiar versiones
  - [ ] Verificar instalación

- [ ] **ACCIÓN 2:** Crear README.md (20 min)
  - [ ] Sección instalación
  - [ ] Sección uso
  - [ ] Sección requisitos
  - [ ] Ejemplos funcionales

- [ ] **ACCIÓN 3:** Agregar manejo de excepciones (30 min)
  - [ ] Envolver prueba.py en try/except
  - [ ] Envolver comparativo.py en try/except
  - [ ] Mensajes de error claros
  - [ ] Testing manual

- [ ] **ACCIÓN 4:** Crear config.yaml (25 min)
  - [ ] Archivo config.yaml
  - [ ] Load_config.py helper
  - [ ] Integrar en scripts
  - [ ] Validar funcionamiento

**Subtotal Sprint 0:** 90 minutos (1.5 horas)

### Semana 1 - Opcional

- [ ] **ACCIÓN 5:** Logging estructurado (45 min)
- [ ] **ACCIÓN 6:** Script de verificación (30 min)
- [ ] **ACCIÓN 7:** Documentar código (60 min)

**Total Semana 1 (completo):** 225 minutos (3.75 horas)

---

## 🚨 PROBLEMAS BLOQUEANTES ACTUALES

### 🔴 CRÍTICO - BLOQUEA EJECUCIÓN

**Problema 1: Archivo no existe**
```
FileNotFoundError: Proyecto/Fotos_de_Prueba/Foto Nereo Lopez.png
```
**Solución:** 
```powershell
# Crear carpeta de prueba
mkdir Proyecto\Fotos_de_Prueba
# Copiar una imagen PNG/JPG ahí
copy "ruta\a\imagen.png" Proyecto\Fotos_de_Prueba\"Foto Nereo Lopez.png"
```

**Problema 2: Symphony CSV no existe**
```
FileNotFoundError: bnco/Symphony_30_07_2025.csv
```
**Solución:**
```powershell
# Obtener archivo de sistema Symphony
# O comentar temporalmente para testear solo Portfolio
```

**Problema 3: Descarga de modelo falla**
```
ConnectionError: Failed to download Salesforce/blip2-flan-t5-xl
```
**Solución:**
```powershell
# Verificar conectividad
ping huggingface.co
# Descargar manualmente si es necesario
```

---

## 📊 IMPACTO DE ACCIONES

| Acción | Tiempo | Impacto | ROI |
|--------|--------|--------|-----|
| Acción 1: requirements.txt | 15 min | 🟢 Alto | 🟢 Muy alto |
| Acción 2: README.md | 20 min | 🟢 Alto | 🟢 Muy alto |
| Acción 3: Excepciones | 30 min | 🔴 Crítico | 🟢 Muy alto |
| Acción 4: config.yaml | 25 min | 🟠 Medio | 🟡 Medio |
| Acción 5: Logging | 45 min | 🟡 Medio | 🟡 Medio |
| Acción 6: Verify script | 30 min | 🟡 Medio | 🟡 Medio |
| Acción 7: Docstrings | 60 min | 🟡 Medio | 🟡 Bajo |

**Total:** 225 minutos (3.75 horas) para transformar de prototipo a beta viable

---

## ✅ CRITERIOS DE ÉXITO

Después de ejecutar estas acciones, el MVP debe:

1. ✅ Tener `requirements.txt` documentado
2. ✅ Poder ejecutarse sin crashes
3. ✅ Mostrar mensajes de error claros
4. ✅ Tener README funcional
5. ✅ Ser reproducible en otra máquina
6. ✅ Tener configuración centralizada
7. ✅ Ser debuggeable con logging

---

## 🎯 SIGUIENTES PASOS (DESPUÉS DE SPRINT 0)

Una vez completado Sprint 0, proceder con:

**Sprint 1 (Robustez):**
- [ ] Refactorizar en módulos
- [ ] Agregar tests unitarios
- [ ] Implementar validación de inputs
- [ ] Mejorar performance

**Sprint 2 (Escalabilidad):**
- [ ] Implementar SQLite
- [ ] Crear CLI
- [ ] Agregar batch processing
- [ ] Documentar API interna

**Sprint 3 (Producción):**
- [ ] API REST (FastAPI)
- [ ] Dockerización
- [ ] CI/CD setup
- [ ] Monitoring

---

## 📞 SOPORTE

En caso de problemas:

1. Revisar [ESPECIFICACION_DEPENDENCIAS.md](ESPECIFICACION_DEPENDENCIAS.md) sección 7 (Troubleshooting)
2. Ejecutar `verify_env.py` para diagnosticar
3. Consultar [INVENTARIO_TECNICO_MVP.md](INVENTARIO_TECNICO_MVP.md) sección 7.4 (Limitaciones)

---

**Plan creado:** 18 de enero de 2026  
**Vigencia:** Válido para próximas 2 semanas  
**Reviewer recomendado:** Tech Lead del proyecto
