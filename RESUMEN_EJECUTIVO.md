# RESUMEN EJECUTIVO - MVP CATALOGIA

**Fecha:** 18 de enero de 2026  
**Clasificación:** Resumen Técnico Ejecutivo

---

## VISIÓN GENERAL

**CatalogIA** es un prototipo experimental (TRL 4-5) que automatiza la generación de descripciones bibliográficas para acervos fotográficos institucionales mediante modelos de Inteligencia Artificial.

---

## CAPACIDADES ACTUALES

### ✅ Módulo 1: Catalogación Automática de Imágenes
- **Modelo:** BLIP-2 Flan-T5-XL (Salesforce)
- **Entrada:** Imágenes PNG/JPG
- **Salida:** Descripción bibliográfica en lenguaje natural
- **Estado:** Funcional
- **Dispositivo:** GPU (CUDA) o CPU (fallback automático)

### ✅ Módulo 2: Análisis Comparativo de Catálogos
- **Función:** Compara sistemas Symphony vs. Portfolio
- **Entrada:** Archivos CSV/TXT de catálogos
- **Salida:** Reporte Excel con análisis de coincidencias
- **Estado:** Funcional
- **Volumen:** Procesado portfolio de 191K registros

---

## STACK TÉCNICO

| Componente | Tecnología |
|-----------|-----------|
| **Lenguaje** | Python 3.7+ |
| **Modelo IA** | Transformers (Hugging Face) |
| **Computación** | PyTorch (CPU/GPU) |
| **Datos** | Pandas + Excel |
| **Versionado** | Git |

---

## DEPENDENCIAS CRÍTICAS

**⚠️ ESTADO:** requirements.txt **VACÍO** - Las dependencias no están documentadas

```
transformers  (Hugging Face - Modelos IA)
torch        (PyTorch - Backend computacional)
pandas       (Análisis de datos)
pillow       (Procesamiento de imágenes)
```

**Impacto:** Reproducibilidad comprometida, difícil setup en otros entornos

---

## LIMITACIONES CLAVE

| Limitación | Impacto | Prioridad |
|-----------|--------|----------|
| Sin manejo de excepciones | Fallos catastóficos sin mensajes útiles | 🔴 Crítica |
| Sin persistencia de resultados | Salidas no se guardan | 🔴 Crítica |
| Sin API/CLI | Solo ejecución de scripts directa | 🟠 Alta |
| Sin validación de entrada | Fallos silenciosos con datos malos | 🟠 Alta |
| SSL deshabilitado globalmente | Riesgo de seguridad en producción | 🟠 Alta |
| Sin tests unitarios | 0% cobertura de tests | 🟡 Media |
| Código sin documentación | Difícil mantenimiento | 🟡 Media |
| Parámetros hardcodeados | Difícil configuración | 🟡 Media |

---

## ARQUITECTURA SIMPLIFICADA

```
INPUT (Imagen)
    ↓
[Descargar Modelo BLIP-2 desde Hugging Face]
    ↓
[Procesar imagen → Generar descripción]
    ↓
OUTPUT (Texto en consola)

INPUT (CSVs de catálogos)
    ↓
[Expandir & Limpiar datos]
    ↓
[Merge por URLs]
    ↓
OUTPUT (Archivo Excel con análisis)
```

---

## REQUISITOS DE INFRAESTRUCTURA

### Mínimos:
- CPU moderna (Intel i5+, AMD Ryzen 5+)
- 8 GB RAM
- 10 GB espacio disco (para caché de modelos)
- Internet (primera ejecución descarga ~5 GB)

### Recomendados:
- GPU NVIDIA con CUDA 11.8+
- 16+ GB RAM
- 50 GB espacio disco
- Conexión estable a internet

---

## PUNTUACIÓN DE MADUREZ

| Dimensión | Puntuación | Color |
|-----------|-----------|-------|
| Viabilidad técnica | 8/10 | 🟢 Buena |
| Escalabilidad | 3/10 | 🔴 Baja |
| Confiabilidad | 4/10 | 🔴 Baja |
| Mantenibilidad | 4/10 | 🔴 Baja |
| Documentación | 2/10 | 🔴 Muy baja |
| **Promedio** | **4.2/10** | **🟠 Prototipo** |

**Veredicto:** No listo para producción. Requiere 4-6 semanas de refactorización.

---

## ROADMAP RECOMENDADO

### Sprint 1 (1-2 semanas) - **Consolidación**
- [ ] Documentar dependencias en `requirements.txt`
- [ ] Crear `README.md` con instrucciones setup
- [ ] Agregar manejo básico de excepciones
- [ ] Crear archivo `config.yaml`

### Sprint 2 (2-3 semanas) - **Robustez**
- [ ] Refactorizar en módulos reutilizables
- [ ] Implementar logging estructurado
- [ ] Agregar validación de inputs
- [ ] Crear 5-10 tests unitarios

### Sprint 3 (2-4 semanas) - **Escalabilidad**
- [ ] Implementar BD SQLite para persistencia
- [ ] Crear CLI con argparse/click
- [ ] Agregar procesamiento batch paralelo
- [ ] Documentar API interna

### Sprint 4+ (Producción)
- [ ] API REST (FastAPI)
- [ ] Containerización Docker
- [ ] Orquestación con Celery
- [ ] Monitoreo y observabilidad

---

## RIESGOS PRINCIPALES

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|--------|-----------|
| Descarga de modelo falla | Alta | Crítico | Caché offline + retry logic |
| Memoria insuficiente | Media | Crítico | Streaming, reducir batch size |
| Inconsistencia de versiones | Alta | Alto | requirements.txt congelado |
| Derivación de prompts | Media | Medio | Sanitización de inputs |

---

## CONCLUSIÓN

**CatalogIA** demuestra que es **técnicamente viable** usar BLIP-2 para catalogación automática. El prototipo funciona pero necesita:

1. **Inmediato:** Documentación de dependencias + manejo de errores
2. **Corto plazo:** Refactorización + testing
3. **Mediano plazo:** Persistencia + API
4. **Largo plazo:** Production hardening

**Recomendación:** Continuar desarrollo priorizando sprint 1-2 antes de cualquier uso institucional.

---

**Contacto técnico:** GitHub Copilot  
**Siguiente revisión:** Post-Sprint 2
