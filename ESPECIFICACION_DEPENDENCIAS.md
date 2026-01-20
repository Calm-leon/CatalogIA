# ESPECIFICACIÓN TÉCNICA DE DEPENDENCIAS

**Versión:** 1.0  
**Fecha:** 18 de enero de 2026  
**Propósito:** Documento de referencia para reproducir entorno del MVP

---

## 1. DEPENDENCIAS IDENTIFICADAS POR ANÁLISIS DE CÓDIGO

### 1.1 Importaciones Directas en `prueba.py`

```python
import ssl                           # Librería estándar Python
import urllib3                       # HTTP client (transitive)
import os                            # Librería estándar Python
from transformers import (
    Blip2Processor,                 # Procesador de entrada
    Blip2ForConditionalGeneration   # Modelo generativo
)
from PIL import Image               # Procesamiento de imágenes
import torch                         # Computación tensor
```

### 1.2 Importaciones Directas en `Comparativo_Portfolio_Symphony.py`

```python
import pandas as pd                  # Análisis y manipulación de datos
```

---

## 2. MATRIZ DE DEPENDENCIAS

### Tabla 2.1: Dependencias Directas

| Paquete | Función | Instalación | Versión Mínima | Tipo |
|---------|---------|-------------|-----------------|------|
| **transformers** | Modelos IA + Hugging Face Hub | pip | 4.20.0 | Core |
| **torch** | Backend de ML (CPU/GPU) | pip/conda | 1.10.0 | Core |
| **pillow** | Procesamiento de imágenes | pip | 8.0.0 | Core |
| **pandas** | Análisis tabular | pip | 1.0.0 | Core |
| **urllib3** | HTTP requests (depende transformers) | pip auto | 1.26.0 | Transitive |

### Tabla 2.2: Dependencias Transitivas (Instaladas automáticamente)

| Paquete | Requerida por | Versión Mínima | Propósito |
|---------|---------------|-----------------|-----------|
| **numpy** | torch, pandas, transformers | 1.19.0 | Computación numérica |
| **scipy** | transformers | 1.5.0 | Algoritmos científicos |
| **datasets** | transformers | 2.0.0 | Manejo de datasets |
| **tokenizers** | transformers | 0.11.0 | Tokenización de texto |
| **tqdm** | transformers | 4.0.0 | Progress bars |
| **requests** | transformers, urllib3 | 2.25.0 | HTTP client |
| **pyyaml** | transformers | 5.1.0 | Parsing de configuración |
| **huggingface-hub** | transformers | 0.10.0 | Descarga de modelos |
| **filelock** | transformers, huggingface-hub | 3.0.0 | Sincronización de archivos |
| **openpyxl** | pandas (para Excel) | 2.6.0 | Lectura/escritura Excel |
| **regex** | transformers | 2021.0.0 | Pattern matching avanzado |

---

## 3. REQUERIMIENTOS RECOMENDADOS

### 3.1 Archivo `requirements.txt` Recomendado

```txt
# -*- coding: utf-8 -*-
# CatalogIA MVP - Dependencias de Producción
# Generado: 18 de enero de 2026

# Core ML Framework
torch==2.1.0
transformers==4.35.0
huggingface-hub==0.19.0

# Data Processing
pandas==2.1.1
openpyxl==3.1.0

# Image Processing
Pillow==10.0.0

# Networking
urllib3==2.0.0
requests==2.31.0

# Utilities
tqdm==4.66.0
pyyaml==6.0
filelock==3.13.0

# ML Dependencies (transitives, but explicit for clarity)
numpy==1.24.0
scipy==1.11.0
datasets==2.14.0
tokenizers==0.14.0
regex==2023.11.0
```

### 3.2 Archivo `requirements-dev.txt` Recomendado

```txt
# Development dependencies (not needed for production)
# Instalar con: pip install -r requirements-dev.txt

-r requirements.txt

# Testing
pytest==7.4.0
pytest-cov==4.1.0

# Linting & Formatting
black==23.9.0
flake8==6.1.0
pylint==2.18.0
mypy==1.5.0

# Documentation
sphinx==7.2.0
sphinx-rtd-theme==1.3.0

# Debugging
ipython==8.15.0
ipdb==0.13.0
```

### 3.3 Archivo `requirements-gpu.txt` Recomendado

```txt
# GPU-specific dependencies (NVIDIA CUDA)
# Use this instead of requirements.txt if you have NVIDIA GPU

# Core ML Framework (CUDA version)
torch==2.1.0 --index-url https://download.pytorch.org/whl/cu118
torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu118
torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu118
transformers==4.35.0
huggingface-hub==0.19.0

# Data Processing
pandas==2.1.1
openpyxl==3.1.0

# Image Processing
Pillow==10.0.0

# Networking
urllib3==2.0.0
requests==2.31.0

# Utilities
tqdm==4.66.0
pyyaml==6.0
filelock==3.13.0

# ML Dependencies
numpy==1.24.0
scipy==1.11.0
datasets==2.14.0
tokenizers==0.14.0
regex==2023.11.0
```

---

## 4. INSTRUCCIONES DE INSTALACIÓN

### 4.1 Instalación en Windows (CPU)

```powershell
# 1. Crear entorno virtual
python -m venv catalogia_env

# 2. Activar entorno
catalogia_env\Scripts\Activate.ps1

# 3. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 4. Verificar instalación
python -c "import torch; import transformers; print('✅ OK')"
```

### 4.2 Instalación en Windows (GPU NVIDIA)

```powershell
# 1. Crear entorno virtual
python -m venv catalogia_env

# 2. Activar entorno
catalogia_env\Scripts\Activate.ps1

# 3. Instalar CUDA dependencies
pip install --upgrade pip

# 4. Instalar pytorch con soporte CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 5. Instalar resto de dependencias
pip install transformers huggingface-hub pandas openpyxl pillow

# 6. Verificar GPU
python -c "import torch; print('CUDA disponible:', torch.cuda.is_available())"
```

### 4.3 Instalación en Linux/macOS

```bash
# 1. Crear entorno virtual
python3 -m venv catalogia_env

# 2. Activar entorno
source catalogia_env/bin/activate

# 3. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 4. Verificar instalación
python -c "import torch; import transformers; print('✅ OK')"
```

### 4.4 Instalación con Conda

```bash
# 1. Crear entorno conda
conda create -n catalogia python=3.10

# 2. Activar entorno
conda activate catalogia

# 3. Instalar dependencias principales
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
conda install -c conda-forge transformers pandas pillow

# 4. Instalar complementarias
pip install huggingface-hub tqdm

# 5. Verificar instalación
python -c "import torch; print(torch.__version__)"
```

---

## 5. CONFIGURACIÓN DE HUGGING FACE HUB

### 5.1 Primera Descarga de Modelo

La primera ejecución descargará automáticamente el modelo BLIP-2 (~5 GB):

```
Ubicación: ~/.cache/huggingface/hub/models--Salesforce--blip2-flan-t5-xl/
Tiempo: 5-15 minutos (depende de velocidad internet)
Almacenamiento: 5-6 GB en disco
```

### 5.2 Descargar Modelo Manualmente (Offline)

```python
from transformers import Blip2Processor, Blip2ForConditionalGeneration

# Descargar en primera ejecución
processor = Blip2Processor.from_pretrained("Salesforce/blip2-flan-t5-xl")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-flan-t5-xl")

print("✅ Modelo descargado. Ubicación:", processor.cache_dir)
```

### 5.3 Usar Modelo Offline

```python
import os

# Forzar modo offline (después de primera descarga)
os.environ["HF_HUB_OFFLINE"] = "1"

processor = Blip2Processor.from_pretrained("Salesforce/blip2-flan-t5-xl")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-flan-t5-xl")

print("✅ Modelo cargado desde caché local")
```

---

## 6. VERIFICACIÓN DE ENTORNO

### 6.1 Script de Verificación

Crea archivo `verify_environment.py`:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verifica que el entorno esté correctamente configurado"""

import sys

def check_environment():
    print("=" * 60)
    print("VERIFICACIÓN DE ENTORNO CATALOGIA")
    print("=" * 60)
    
    checks = []
    
    # Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    checks.append(("Python", py_version, sys.version_info >= (3, 7)))
    
    # PyTorch
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        device = f"CUDA ({torch.cuda.get_device_name(0)})" if cuda_available else "CPU"
        checks.append(("PyTorch", f"{torch.__version__} - {device}", True))
    except ImportError:
        checks.append(("PyTorch", "❌ No instalado", False))
    
    # Transformers
    try:
        import transformers
        checks.append(("Transformers", transformers.__version__, True))
    except ImportError:
        checks.append(("Transformers", "❌ No instalado", False))
    
    # Pandas
    try:
        import pandas
        checks.append(("Pandas", pandas.__version__, True))
    except ImportError:
        checks.append(("Pandas", "❌ No instalado", False))
    
    # PIL
    try:
        from PIL import Image
        checks.append(("Pillow", Image.__version__, True))
    except ImportError:
        checks.append(("Pillow", "❌ No instalado", False))
    
    # Numpy
    try:
        import numpy
        checks.append(("NumPy", numpy.__version__, True))
    except ImportError:
        checks.append(("NumPy", "❌ No instalado", False))
    
    # Print results
    print()
    for name, version, ok in checks:
        status = "✅ OK" if ok else "❌ FALLO"
        print(f"{name:20} {version:30} {status}")
    
    print()
    all_ok = all(ok for _, _, ok in checks)
    if all_ok:
        print("🎉 Entorno configurado correctamente")
        return 0
    else:
        print("⚠️  Hay problemas de configuración")
        return 1

if __name__ == "__main__":
    sys.exit(check_environment())
```

Uso:
```bash
python verify_environment.py
```

---

## 7. SOLUCIÓN DE PROBLEMAS

### 7.1 Error: "ModuleNotFoundError: No module named 'torch'"

```bash
# Solución
pip install torch

# O con CUDA
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### 7.2 Error: "RuntimeError: CUDA out of memory"

```python
# Reducir tamaño de modelo en prueba.py
torch_dtype=torch.float32  # En lugar de float16
device_map="cpu"           # Usar CPU en lugar de GPU
```

### 7.3 Error: "Certificate verify failed" (SSL)

El código ya incluye workaround:
```python
ssl._create_default_https_context = ssl._create_unverified_context
```

⚠️ **Nota:** Solo usar en desarrollo local. En producción, actualizar certificados:
```bash
python -m pip install --upgrade certifi
```

### 7.4 Error: "FileNotFoundError: requirements.txt"

Crear el archivo en `Proyecto/`:
```bash
cd Proyecto
touch requirements.txt
pip freeze > requirements.txt  # Generar automáticamente
```

### 7.5 Descarga de modelo muy lenta

```python
# Usar espejo de HF (si está disponible)
os.environ["HF_ENDPOINT"] = "https://huggingface-mirror.com"
```

---

## 8. VERSIONES MÍNIMAS DE SISTEMA

| Sistema | Versión Mínima | Recomendada |
|---------|----------------|------------|
| **Python** | 3.7 | 3.10+ |
| **Windows** | 10 | 11 |
| **macOS** | 10.14 | 12+ |
| **Linux** | Ubuntu 18.04 | Ubuntu 20.04+ |
| **CUDA** (GPU) | 11.0 | 11.8+ |
| **cuDNN** (GPU) | 8.0 | 8.7+ |

---

## 9. MANTENIMIENTO DE DEPENDENCIAS

### 9.1 Actualizar Todas las Dependencias

```bash
pip install --upgrade -r requirements.txt
```

### 9.2 Verificar Vulnerabilidades de Seguridad

```bash
pip install safety
safety check
```

### 9.3 Generar requirements.txt Automáticamente

```bash
pip freeze > requirements.txt
```

⚠️ **Nota:** Esto incluye TODAS las versiones actuales. Revisar y limpiar manualmente.

### 9.4 Ver Dependencias Instaladas

```bash
pip list
pip show transformers  # Info detallada de un paquete
```

---

## 10. ARCHIVOS DE CONFIGURACIÓN RECOMENDADOS

### 10.1 `setup.py` (Para empaquetamiento)

```python
from setuptools import setup, find_packages

setup(
    name="catalogia",
    version="0.1.0",
    description="Sistema de catalogación automática con IA",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "torch>=2.1.0",
        "transformers>=4.35.0",
        "pandas>=2.1.0",
        "Pillow>=10.0.0",
    ],
    python_requires=">=3.7",
)
```

### 10.2 `pyproject.toml` (Moderno)

```toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "catalogia"
version = "0.1.0"
description = "Sistema de catalogación automática"
requires-python = ">=3.7"

dependencies = [
    "torch>=2.1.0",
    "transformers>=4.35.0",
    "pandas>=2.1.0",
    "Pillow>=10.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=23.0",
    "pylint>=2.0",
]
```

---

## APÉNDICE A: REFERENCIAS

- **PyTorch:** https://pytorch.org/
- **Transformers:** https://huggingface.co/transformers/
- **BLIP-2:** https://huggingface.co/Salesforce/blip2-flan-t5-xl
- **Pandas:** https://pandas.pydata.org/
- **Pillow:** https://python-pillow.org/

---

**Última actualización:** 18 de enero de 2026  
**Responsable:** Equipo Técnico CatalogIA
