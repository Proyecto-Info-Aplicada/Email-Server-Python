# Documentación Técnica - Email Server Python

## 📋 Índice
1. [Arquitectura General](#arquitectura-general)
2. [Flujo de Datos](#flujo-de-datos)
3. [Componentes Principales](#componentes-principales)
4. [Patrones de Diseño](#patrones-de-diseño)
5. [Guía de Desarrollo](#guía-de-desarrollo)

---

## 🏗️ Arquitectura General

El proyecto sigue una **arquitectura en capas limpia (Clean Architecture)** con separación de responsabilidades:

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│                     (Flask REST API)                         │
│                   src/controller/                            │
│                   src/middleware/                            │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   Application Layer                          │
│              (Business Logic Orchestration)                  │
│                    src/services/                             │
│         - SendEmailService (Orquestador)                     │
│         - GmailService (Envío de emails)                     │
│         - StorageService (Obtención de PDFs)                 │
│         - KafkaProducerService (Logging a Kafka)             │
│         - RequestLogger (Logger estructurado)                │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   Infrastructure Layer                       │
│              (External Connections & Data)                   │
│            src/connection/, src/data/                        │
│         - Gmail API Connection                               │
│         - HTTP Requests to Storage Server                    │
│         - Kafka Producer Connection (opcional)               │
└──────────────────────────────────────────────────────────────┘

      ┌────────────────────────────────────────┐
      │         Cross-Cutting Concerns          │
      │                                        │
      │  - src/config/ (Configuration)         │
      │  - src/dto/ (Data Transfer Objects)    │
      │  - src/interfaces/ (Contracts)         │
      │  - src/middleware/ (Request/Response)  │
      └────────────────────────────────────────┘
```

---

## 🔄 Flujo de Datos

### Flujo de envío de email con PDF (con Kafka integrado)

```
1. Cliente HTTP
   │
   │ POST /send-email-task
   │ {CorrelationId, EmailAddress, ...}
   │ Headers: X-Correlation-ID (opcional)
   │
   ▼
2. Correlation Middleware (src/middleware/correlation_middleware.py)
   │ - Extrae/Genera Correlation ID
   │ - Almacena en Flask g context
   │ - Registra request entrante
   │
   ▼
3. EmailController (src/controller/email_controller.py)
   │ - Recibe request HTTP
   │ - Valida JSON
   │ - Inicia tracking de tiempo
   │
   ▼
4. SendEmailService (src/services/send_email_service.py)
   │ - Crea EmailRequest DTO
   │ - Valida campos obligatorios
   │ - Registra flujo de validación
   │
   ├──► 5a. StorageService (src/services/storage_service.py)
   │        │ - Solicita PDF al Storage Server
   │        │ - GET http://storage:5000/pdf-storage/{id}
   │        │
   │        ▼ HTTP Request
   │    Storage Server Externo
   │        │
   │        ▼ PDF bytes
   │    └─ Retorna PDF en bytes
   │
   ├──► 5b. GmailService (src/services/gmail_service.py)
   │        │ - Construye mensaje MIME con PDF adjunto
   │        │ - Llama a gmail_connection
   │        │
   │        ▼
   │    6. GmailConnection (src/connection/gmail_connection.py)
   │        │ - Autentica con OAuth 2.0
   │        │ - Envía mensaje vía Gmail API
   │        │
   │        ▼ API Call
   │    Gmail API (Google)
   │        │
   │        ▼ Email enviado
   │    Destinatario
   │
   └──► 5c. RequestLogger (src/services/request_logger.py)
            │ - Prepara log estructurado
            │ - Incluye tiempo de ejecución
            │ - Incluye flujo de validación
            │
            ▼
        7. KafkaProducerService (src/services/kafka_service.py)
            │ - Envía mensaje a Kafka
            │ - Topic: email-server-requests
            │ - Headers: CorrelationId, LogLevel, Source
            │
            ▼ Kafka Message
        Apache Kafka (opcional)
            │
            ▼ (si falla Kafka)
        Fallback a Consola/Archivo
```

---

## 🧩 Componentes Principales

### 1. **Controllers** (`src/controller/`)
**Responsabilidad:** Exponer endpoints REST y manejar HTTP requests/responses.

- `email_controller.py`: 
  - `POST /send-email-task`: Envía email con PDF
  - `GET /health`: Health check

### 2. **Services** (`src/services/`)
**Responsabilidad:** Lógica de negocio y orquestación.

- `send_email_service.py`: Orquesta el flujo completo de envío
- `gmail_service.py`: Implementa envío de emails con Gmail API
- `storage_service.py`: Obtiene PDFs del Storage Server

### 3. **Connection** (`src/connection/`)
**Responsabilidad:** Gestionar conexiones con servicios externos.

- `gmail_connection.py`: 
  - Autenticación OAuth 2.0
  - Manejo de tokens y refresh
  - Envío de mensajes vía Gmail API

### 4. **DTOs** (`src/dto/`)
**Responsabilidad:** Transferencia de datos entre capas.

- `email_dto.py`:
  - `EmailRequest`: Datos del request de envío
  - `BaseRequest`: Base para otros DTOs

### 5. **Interfaces** (`src/interfaces/`)
**Responsabilidad:** Contratos y abstracciones.

- `email_interfaces.py`:
  - `IEmailSender`: Contrato para servicios de envío
  - `IPdfRetriever`: Contrato para obtención de PDFs

### 6. **Config** (`src/config/`)
**Responsabilidad:** Configuración centralizada.

- `settings.py`: Variables de configuración
- `logging_config.py`: Configuración de logs

---

## 🎨 Patrones de Diseño

### 1. **Dependency Injection**
Los servicios reciben sus dependencias en el constructor:
```python
class SendEmailService:
    def __init__(self):
        self.gmail_service = GmailService()
        self.storage_service = StorageService()
```

### 2. **Interface Segregation**
Interfaces específicas para cada responsabilidad:
```python
class IEmailSender(ABC):
    @abstractmethod
    def send_email_with_attachment(...): pass

class IPdfRetriever(ABC):
    @abstractmethod
    def get_pdf_by_correlation(...): pass
```

### 3. **DTO Pattern**
Objetos para transferir datos entre capas:
```python
@dataclass
class EmailRequest:
    correlation_id: str
    email_address: str
    # ...
```

### 4. **Facade Pattern**
`send_email_service.py` actúa como fachada que simplifica la interacción entre múltiples servicios.

### 5. **Single Responsibility Principle**
Cada clase tiene una única responsabilidad:
- `GmailService`: Solo envío de emails
- `StorageService`: Solo obtención de PDFs
- `SendEmailService`: Solo orquestación

---

## 👨‍💻 Guía de Desarrollo

### Agregar un nuevo endpoint

1. **Crear método en controller:**
```python
# src/controller/email_controller.py
@email_blueprint.route('/nuevo-endpoint', methods=['POST'])
def nuevo_endpoint():
    data = request.get_json()
    # Lógica aquí
    return jsonify(result), 200
```

2. **Crear servicio si es necesario:**
```python
# src/services/nuevo_service.py
class NuevoService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def execute(self, data: dict):
        # Lógica de negocio
        pass
```

3. **Actualizar interfaces si corresponde:**
```python
# src/interfaces/nueva_interface.py
class INuevaInterface(ABC):
    @abstractmethod
    def metodo(self): pass
```

### Agregar nueva configuración

Editar `src/config/settings.py`:
```python
# Nueva configuración
NUEVA_CONFIG = os.getenv("NUEVA_CONFIG", "valor_default")
```

### Logging

Usar el logger en cualquier módulo:
```python
import logging
logger = logging.getLogger(__name__)

logger.info("Mensaje informativo")
logger.warning("Advertencia")
logger.error("Error", exc_info=True)
```

### Testing (Futuro)

Estructura recomendada:
```
tests/
├── unit/
│   ├── test_services.py
│   └── test_dto.py
├── integration/
│   └── test_api.py
└── conftest.py
```

---

## 🔐 Seguridad

### OAuth 2.0 Flow
1. Primera ejecución: Abre navegador para autorizar
2. Guarda `token.json` localmente
3. Renovación automática de tokens expirados

### Variables Sensibles
**NUNCA** subir a Git:
- `credentials.json`
- `token.json`
- Variables de entorno con secrets

---

## 📈 Mejoras Futuras

- [ ] Implementar tests unitarios e integración
- [ ] Agregar soporte para múltiples proveedores de email
- [ ] Implementar queue system (Redis/RabbitMQ)
- [ ] Agregar retry logic con exponential backoff
- [ ] Implementar rate limiting
- [ ] Agregar métricas y monitoring (Prometheus)
- [ ] Dockerizar la aplicación
- [ ] CI/CD pipeline

---

**Última actualización:** 2025-10-22
