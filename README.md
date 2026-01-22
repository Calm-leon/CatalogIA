# CatalogIA - Sistema de Precatalogación Asistida por IA

**Versión:** 1.0 (Prototipo Experimental)  
**Fecha:** 22 de enero de 2026  
**Estado:** TRL 4-5 (Prototipo validado en laboratorio)

---

## 📋 Descripción

CatalogIA es un sistema experimental que automatiza la generación de descripciones bibliográficas para acervos institucionales mediante modelos de Inteligencia Artificial. Diseñado específicamente para la Biblioteca Nacional de Colombia (BNC), procesa objetos bibliográficos digitales (imágenes, libros escaneados, audios, videos) y genera fichas técnicas preliminares en formato XML, respetando los marcos normativos vigentes (MARC21, RDA, Dublin Core).

### 🎯 Objetivos
- **Automatización:** Reducir el tiempo manual de catalogación en un 70-80%
- **Precisión:** Generar descripciones preliminares válidas para revisión humana
- **Escalabilidad:** Procesar miles de objetos mensualmente
- **Conformidad:** Respeto a estándares bibliográficos internacionales
- **Privacidad:** Ejecución local sin dependencia de servicios cloud

---

## 🚀 Inicio Rápido

### Prerrequisitos
- **Python:** 3.8+ (recomendado 3.10+)
- **RAM:** 8 GB mínimo, 16 GB recomendado
- **Almacenamiento:** 10 GB libres (para modelos IA)
- **GPU:** Opcional, acelera procesamiento 5-10x (CUDA compatible)

### Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/Calm-leon/CatalogIA.git
cd CatalogIA
```

2. **Crear entorno virtual:**
```bash
python -m venv catalogia_env
# En Windows:
catalogia_env\Scripts\activate
# En Linux/Mac:
source catalogia_env/bin/activate
```

3. **Instalar dependencias:**
```bash
cd Proyecto
pip install -r requirements.txt
```

### Uso Básico

#### Catalogación de Imágenes
```bash
python prueba.py
```
- Procesa una imagen de prueba y genera descripción automática
- Requiere imagen en `Fotos_de_Prueba\Foto Nereo Lopez.png`

#### Comparación de Catálogos
```bash
python Comparativo_Portfolio_Symphony.py
```
- Compara catálogos Symphony vs Portfolio
- Genera reporte Excel con análisis de coincidencias

---

## 📁 Estructura del Proyecto

```
CatalogIA/
├── Proyecto/                    # Código fuente principal
│   ├── prueba.py               # Módulo catalogación BLIP-2
│   ├── requirements.txt        # Dependencias Python
│   └── catalogia_env/          # Entorno virtual
├── bnco/                       # Datos de referencia
│   └── Portfolio_22_08_2025.txt # Catálogo Portfolio (191K registros)
├── data/                       # Datos de entrada
│   └── Fotos/                  # Imágenes para catalogación
├── modelos/                    # Modelos IA descargados
├── outputs/                    # Resultados generados
├── docs/                       # Documentación técnica
│   ├── ARQUITECTURA_CATALOGIA.md
│   ├── GUIA_RAPIDA.md
│   └── [otros documentos...]
└── README.md                   # Este archivo
```

---

## 🏗️ Arquitectura

El sistema sigue una arquitectura monolítica modular con tres capas principales:

- **Presentación:** CLI básico y futura API REST
- **Lógica de Negocio:** Módulos de IA y procesamiento de datos
- **Datos:** Almacenamiento local de archivos y metadatos

Para detalles completos, ver [ARQUITECTURA_CATALOGIA.md](ARQUITECTURA_CATALOGIA.md).

---

## 🔧 Configuración

### Archivo de Configuración
Crear `config.yaml` en la raíz del proyecto:

```yaml
# Configuración CatalogIA
model:
  name: "Salesforce/blip2-flan-t5-xl"
  device: "auto"  # auto, cuda, cpu
  dtype: "auto"   # auto, float16, float32

processing:
  batch_size: 1
  max_tokens: 150
  temperature: 0.7

paths:
  input_images: "data/Fotos/"
  output_results: "outputs/"
  models_cache: "modelos/"

logging:
  level: "INFO"
  file: "logs/catalogia.log"
```

### Variables de Entorno
```bash
# Deshabilitar verificación SSL (solo desarrollo)
export CATALOGIA_SSL_VERIFY=false

# Configurar proxy si necesario
export HTTP_PROXY=http://proxy.bibliotecanacional.gov.co:8080
```

---

## 📊 Capacidades Actuales

| Módulo | Entrada | Proceso | Salida | Estado |
|--------|---------|---------|--------|--------|
| **Catalogación IA** | Imagen PNG/JPG | BLIP-2 + Prompt | Descripción texto | ✅ Funcional |
| **Comparación Catálogos** | CSV + TXT | Merge SQL-style | Excel análisis | ✅ Funcional |
| **Generación XML** | Metadatos | Mapeo MARC21 | Ficha XML | 🚧 En desarrollo |
| **API REST** | JSON requests | FastAPI | JSON responses | 🚧 Planificado |
| **Interfaz Web** | Navegador | Streamlit/React | GUI completa | 📋 Futuro |

---

## 🧪 Testing

### Pruebas Básicas
```bash
# Verificar instalación
python -c "import torch, transformers; print('✅ Dependencias OK')"

# Ejecutar módulo IA (requiere imagen de prueba)
python prueba.py

# Ejecutar comparación
python Comparativo_Portfolio_Symphony.py
```

### Validación de Resultados
- Descripciones generadas deben ser coherentes y relevantes
- Comparaciones deben identificar correctamente coincidencias/duplicados
- Performance: < 30 segundos por imagen en GPU

---

## 🚨 Limitaciones y Problemas Conocidos

### Críticos (Resolver inmediatamente)
- Sin manejo robusto de excepciones
- Sin persistencia de resultados
- Sin logging estructurado
- Sin validación de entrada

### Importantes
- Procesamiento secuencial (no batch)
- Sin API REST
- Sin interfaz de usuario
- Sin tests automatizados

### Mejoras Planificadas
Ver [PLAN_ACCION_INMEDIATA.md](PLAN_ACCION_INMEDIATA.md) para roadmap detallado.

---

## 📚 Documentación

| Documento | Descripción | Tiempo de Lectura |
|-----------|-------------|-------------------|
| [GUIA_RAPIDA.md](GUIA_RAPIDA.md) | Inicio en 5 minutos | 5 min |
| [ARQUITECTURA_CATALOGIA.md](ARQUITECTURA_CATALOGIA.md) | Diseño del sistema | 20 min |
| [INVENTARIO_TECNICO_MVP.md](INVENTARIO_TECNICO_MVP.md) | Análisis técnico completo | 60 min |
| [ESPECIFICACION_DEPENDENCIAS.md](ESPECIFICACION_DEPENDENCIAS.md) | Instalación detallada | 40 min |
| [PLAN_ACCION_INMEDIATA.md](PLAN_ACCION_INMEDIATA.md) | Próximos pasos | 20 min |

---

## 🤝 Contribución

### Proceso de Desarrollo
1. Crear rama desde `develop`
2. Implementar cambios
3. Agregar tests si aplicable
4. Actualizar documentación
5. Pull request a `develop`

### Estándares de Código
- **Python:** PEP 8
- **Commits:** Mensajes descriptivos en inglés
- **Documentación:** Docstrings en funciones complejas
- **Versionado:** Semantic versioning

---

## 📄 Licencia

Este proyecto es propiedad de la Biblioteca Nacional de Colombia. Uso interno autorizado.

---

## 📞 Soporte

- **Issues:** Crear issue en GitHub con etiqueta apropiada
- **Documentación:** Revisar archivos en carpeta `docs/`
- **Urgencias:** Contactar equipo de desarrollo

---

## 🔄 Historial de Versiones

- **v1.0 (2026-01-22):** Prototipo funcional con módulos básicos
- **v0.9 (2026-01-18):** Análisis técnico completado
- **v0.1 (2025-08-22):** Concepto inicial validado

---

**Última actualización:** 22 de enero de 2026  
**Mantenedor:** Camilo Andrés López León (clopezl@bibliotecanacional.gov.co)</content>
<parameter name="filePath">c:\Users\clopezl\Documents\CatalogIA\README.md