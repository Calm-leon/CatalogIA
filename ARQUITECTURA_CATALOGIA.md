# Arquitectura del Sistema CatalogIA

**Fecha:** 22 de enero de 2026  
**Versión:** 1.0  
**Autor:** GitHub Copilot  
**Proyecto:** CatalogIA - Sistema de Precatalogación Asistida por IA

---

## 1. VISIÓN GENERAL

CatalogIA es un sistema experimental de precatalogación asistida por Inteligencia Artificial diseñado para automatizar la generación de fichas bibliográficas en formato XML para acervos institucionales de la Biblioteca Nacional de Colombia (BNC). El sistema procesa objetos bibliográficos digitales (imágenes, libros escaneados, audios, videos) utilizando modelos de lenguaje e imagen de código abierto ejecutados en entornos locales.

### 1.1 Objetivos Arquitectónicos
- **Automatización:** Reducir el tiempo manual de catalogación en un 70-80%
- **Precisión:** Generar descripciones preliminares válidas para revisión humana
- **Escalabilidad:** Procesar miles de objetos mensualmente
- **Conformidad:** Respeto a marcos normativos (MARC21, RDA, Dublin Core)
- **Privacidad:** Ejecución local sin dependencia de servicios cloud

---

## 2. NECESIDADES TECNOLÓGICAS IDENTIFICADAS

Basado en el análisis del código actual y requerimientos del proyecto:

### 2.1 Requerimientos Funcionales
- Procesamiento de imágenes (PNG/JPG) con modelos de visión por computadora
- Generación de descripciones textuales mediante IA generativa
- Comparación y análisis de catálogos existentes (Symphony vs Portfolio)
- Exportación de metadatos en formato XML/MARC21
- Interfaz de usuario para carga y revisión de resultados

### 2.2 Requerimientos No Funcionales
- **Performance:** Procesamiento de 100-500 imágenes/hora en hardware estándar
- **Confiabilidad:** 99% uptime, manejo robusto de errores
- **Seguridad:** Ejecución offline, sin exposición de datos sensibles
- **Mantenibilidad:** Código modular y documentado
- **Escalabilidad:** Soporte para múltiples tipos de medios (audio/video futuro)

### 2.3 Tecnologías Core Identificadas
- **Lenguaje Principal:** Python 3.8+ (actualmente 3.7+)
- **IA/ML:** PyTorch, Transformers (Hugging Face)
- **Procesamiento de Datos:** Pandas, NumPy
- **Imágenes:** Pillow (PIL)
- **Base de Datos:** SQLite/PostgreSQL para persistencia
- **API/Web:** FastAPI para servicios REST
- **Contenedores:** Docker para despliegue
- **Orquestación:** Docker Compose/Kubernetes

---

## 3. ALTERNATIVAS DE ARQUITECTURA PROPUESTAS

### Alternativa 1: Arquitectura Monolítica Modular (Recomendada para MVP)

#### Descripción
Arquitectura simple y directa, evolucionando el código actual hacia una estructura modular bien organizada. Ideal para prototipo inicial con bajo overhead de desarrollo.

#### Capas Arquitectónicas

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                     │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ CLI (Command Line Interface)                            │ │
│  │ - Carga de archivos                                     │ │
│  │ - Configuración de parámetros                           │ │
│  │ - Visualización de resultados                           │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ API REST (FastAPI)                                      │ │
│  │ - Endpoints para procesamiento batch                    │ │
│  │ - Estado de procesamiento                                │ │
│  │ - Descarga de resultados                                │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                 CAPA DE LÓGICA DE NEGOCIO                   │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Servicio de Catalogación IA                              │ │
│  │ - Procesador BLIP-2                                     │ │
│  │ - Generación de descripciones                           │ │
│  │ - Post-procesamiento de texto                           │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Servicio de Análisis Comparativo                        │ │
│  │ - Parser de catálogos (CSV/TXT)                         │ │
│  │ - Merge y comparación de datasets                       │ │
│  │ - Generación de reportes                                │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Motor de Metadatos                                      │ │
│  │ - Mapeo a estándares (MARC21, Dublin Core)              │ │
│  │ - Generación XML                                        │ │
│  │ - Validación de esquemas                                │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                     CAPA DE DATOS                           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Almacén Local de Archivos                               │ │
│  │ - Imágenes originales                                   │ │
│  │ - Metadatos generados                                   │ │
│  │ - Configuraciones                                       │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Base de Datos SQLite                                    │ │
│  │ - Historial de procesamientos                           │ │
│  │ - Cache de modelos IA                                   │ │
│  │ - Logs de operaciones                                   │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### Lenguajes de Programación
- **Python 3.8+:** 95% del código (lógica de negocio, IA, procesamiento)
- **SQL:** Consultas y esquemas de base de datos
- **YAML/JSON:** Configuraciones y metadatos

#### Ventajas
- **Simplicidad:** Bajo overhead de desarrollo
- **Rápido desarrollo:** Evolución natural del código actual
- **Bajo costo operativo:** Un solo proceso
- **Fácil debugging:** Stack unificado

#### Desventajas
- **Escalabilidad limitada:** Monolítico
- **Disponibilidad:** Punto único de fallo
- **Mantenimiento:** Acoplamiento alto

#### Roadmap de Implementación
1. **Sprint 1 (2 semanas):** Refactorización modular del código actual
2. **Sprint 2 (2 semanas):** Implementación FastAPI + SQLite
3. **Sprint 3 (2 semanas):** CLI completa + logging
4. **Sprint 4 (2 semanas):** Tests + documentación

---

### Alternativa 2: Arquitectura de Microservicios

#### Descripción
Arquitectura distribuida con servicios independientes comunicándose vía APIs. Preparada para escalabilidad futura y separación de responsabilidades.

#### Capas Arquitectónicas

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE ORQUESTACIÓN                     │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ API Gateway (FastAPI + Nginx)                           │ │
│  │ - Enrutamiento de requests                              │ │
│  │ - Autenticación/Autorización                            │ │
│  │ - Rate limiting                                         │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Service Discovery (Consul/Eureka)                       │ │
│  │ - Registro de servicios                                 │ │
│  │ - Health checks                                         │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                 CAPA DE SERVICIOS                           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Microservicio: Catalogación IA                          │ │
│  │ - Puerto: 8001                                          │ │
│  │ - Modelo: BLIP-2                                        │ │
│  │ - Cola: RabbitMQ                                        │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Microservicio: Análisis Comparativo                     │ │
│  │ - Puerto: 8002                                          │ │
│  │ - Tecnología: Python + Pandas                           │ │
│  │ - Cola: RabbitMQ                                        │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Microservicio: Generador XML                            │ │
│  │ - Puerto: 8003                                          │ │
│  │ - Estándares: MARC21, Dublin Core                       │ │
│  │ - Validación: Schematron                                │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Microservicio: Gestión de Archivos                      │ │
│  │ - Puerto: 8004                                          │ │
│  │ - Almacén: MinIO (S3-compatible)                        │ │
│  │ - Compresión: Automatica                                │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                     CAPA DE DATOS                           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ PostgreSQL (Metadatos)                                  │ │
│  │ - Esquemas normalizados                                 │ │
│  │ - Índices optimizados                                   │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Redis (Cache)                                           │ │
│  │ - Cache de modelos IA                                   │ │
│  │ - Sesiones de usuario                                   │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Elasticsearch (Búsqueda)                                │ │
│  │ - Indexación de metadatos                               │ │
│  │ - Búsqueda full-text                                    │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### Lenguajes de Programación
- **Python 3.8+:** Servicios principales (85%)
- **Go:** API Gateway y herramientas de infraestructura (10%)
- **JavaScript/Node.js:** Interfaz web si se implementa (5%)
- **SQL:** Base de datos
- **YAML:** Configuraciones de servicios

#### Ventajas
- **Escalabilidad:** Servicios independientes escalan individualmente
- **Resiliencia:** Fallo en un servicio no afecta otros
- **Tecnologías especializadas:** Cada servicio usa la mejor herramienta
- **Desarrollo paralelo:** Equipos pueden trabajar en servicios diferentes

#### Desventajas
- **Complejidad:** Mayor overhead operativo
- **Latencia:** Comunicación entre servicios
- **Debugging:** Más complejo
- **Costo:** Mayor infraestructura requerida

#### Roadmap de Implementación
1. **Sprint 1-2:** Arquitectura monolítica (como Alternativa 1)
2. **Sprint 3-4:** Extracción de microservicios + contenedores
3. **Sprint 5-6:** Orquestación con Kubernetes
4. **Sprint 7-8:** Monitoring y observabilidad

---

### Alternativa 3: Arquitectura Híbrida Cloud-Edge (Futuro)

#### Descripción
Combinación de procesamiento local (edge) para privacidad y cloud para escalabilidad. Procesamiento IA local, análisis batch en cloud.

#### Capas Arquitectónicas
- **Edge (Local):** Procesamiento IA y catalogación inicial
- **Cloud:** Almacenamiento, análisis avanzado, colaboración
- **Híbrido:** Sincronización selectiva de datos

#### Lenguajes de Programación
- **Python:** Lógica core
- **TypeScript:** Interfaces web
- **Rust:** Componentes de performance crítica

---

## 4. RECOMENDACIÓN ARQUITECTURAL

### Elección: **Alternativa 1 (Monolítica Modular)**
**Justificación:**
- El proyecto está en fase de prototipo (TRL 4-5)
- Equipo pequeño, presupuesto limitado
- Requerimientos iniciales no demandan alta escalabilidad
- Evolución natural del código existente
- Menor riesgo técnico y tiempo de desarrollo

### Plan de Evolución
1. **Fase 1 (3 meses):** Monolítica modular → Producto mínimo viable
2. **Fase 2 (6 meses):** Microservicios → Escalabilidad horizontal
3. **Fase 3 (12 meses):** Cloud híbrido → Capacidades avanzadas

---

## 5. REFERENCIAS Y ESTÁNDARES

### Estándares Bibliográficos
- **MARC21:** [Library of Congress - MARC Standards](https://www.loc.gov/marc/)
- **RDA (Resource Description and Access):** [RDA Toolkit](https://www.rdatoolkit.org/)
- **Dublin Core:** [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)

### Tecnologías de Referencia
- **BLIP-2:** [Salesforce Research Paper](https://arxiv.org/abs/2301.12597)
- **Transformers:** [Hugging Face Documentation](https://huggingface.co/docs/transformers/index)
- **FastAPI:** [FastAPI Documentation](https://fastapi.tiangolo.com/)
- **PyTorch:** [PyTorch Documentation](https://pytorch.org/docs/)

### Arquitecturas Similares
- **Hugging Face Spaces:** Para interfaces de modelos IA
- **Label Studio:** Para anotación y revisión de datos
- **DigiKam/Shotwell:** Para gestión de metadatos de imágenes

### Mejores Prácticas
- **Twelve-Factor App:** [12factor.net](https://12factor.net/)
- **SOLID Principles:** Para diseño orientado a objetos
- **Clean Architecture:** Para separación de responsabilidades

---

## 6. CONCLUSIONES

La arquitectura monolítica modular representa el mejor punto de partida para CatalogIA, permitiendo una evolución controlada desde el prototipo actual hacia un sistema de producción robusto. Las alternativas de microservicios y cloud híbrido están documentadas para futuras fases de crecimiento.

**Próximos pasos:**
1. Implementar la refactorización modular (Sprint 1)
2. Desarrollar API REST básica
3. Implementar persistencia con SQLite
4. Agregar logging y monitoring

Esta arquitectura respeta las necesidades de privacidad de datos de la BNC mientras proporciona una base sólida para automatizar la catalogación bibliográfica con IA.</content>
<parameter name="filePath">c:\Users\clopezl\Documents\CatalogIA\ARQUITECTURA_CATALOGIA.md