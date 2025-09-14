# 📋 Product Requirements Document (PRD)
## Drive Agent - Agente de Memoria Digital

**Versión:** 2.0  
**Fecha:** Diciembre 2024  
**Autor:** Rigo Drive Agent Team  

---

## 📖 Resumen Ejecutivo

Drive Agent es un sistema inteligente que actúa como un asistente personal digital para capturar y organizar archivos multimedia desde múltiples fuentes de mensajería. El sistema utiliza WhatsApp y Telegram como canales de entrada, el agente almacena los archivos enviados dependiendo del destino en una carpeta específica de drive y lo va subiendo dependiendo del año, mes y del día.

### Propuesta de Valor
- **Gestión de archivos multimedia** con subida automática a Google Drive. Cada número de WhatsApp o cliente debe tener una carpeta.
- **Resúmenes estructurados** para indicar cuántos archivos se han subido con su nombre en los últimos días, semanas, meses.
- **Arquitectura escalable** basada en principios SOLID y patrón Strategy para fácil extensión.

---

## 🎯 Objetivos del Producto

### Objetivos Primarios
1. **Automatizar la captura** de archivos enviados a una conversación.
2. **Organizar información** de manera estructurada y accesible
3. **Facilitar la recuperación** de información mediante búsqueda inteligente
4. **Gestionar archivos multimedia** de forma centralizada
5. **Proporcionar resúmenes** para revisión rápida del contenido

### Objetivos Secundarios
1. **Escalabilidad** para múltiples fuentes de datos
2. **Integración** con servicios de almacenamiento en la nube
3. **API robusta** para integraciones futuras
4. **Experiencia de usuario** fluida y sin fricciones

---

## 👥 Audiencia Objetivo

### Usuarios Primarios
- **Profesionales creativos**: Diseñadores, escritores, artistas
- **Emprendedores**: Fundadores de startups, innovadores
- **Estudiantes e investigadores**: Académicos, estudiantes de posgrado
- **Consultores**: Profesionales que manejan múltiples proyectos
- **Freelancers**: Trabajadores independientes con ideas diversas

---

## 🚀 Funcionalidades Principales

### 1. Captura de Ideas
- **Entrada multi-canal**: WhatsApp, Telegram
- **Procesamiento automático**: Detección de comandos vs. archivos
- **Timestamp preciso**: Registro de fecha y hora

### 2. Gestión de Archivos Multimedia
- **Detección automática**: Fotos, videos, documentos, audio
- **Subida a Google Drive**: Organización por fecha (mes/día)
- **Metadatos completos**: Tipo, nombre, enlace de acceso
- **Respuesta automática**: Confirmación de carga exitosa con el nombre del archivo.

### 3. Sistema de Comandos
- **`/resumen`**: Resumen general de todas las ideas
- **`/hoy`**: Ideas del día actual
- **`/semana`**: Ideas de la última semana
- **`/buscar [término]`**: Búsqueda por palabras clave

### 4. Organización Inteligente
- **Estructura por fechas**: Organización cronológica
- **Metadatos enriquecidos**: Fuente, tipo, fecha, contenido
- **Enlaces de acceso**: Acceso directo a archivos, devolver en el mensaje de carga el nombre del archivo y el enlace compartido para verlo.

### 5. API REST
- **Endpoints webhook**: Para integración con fuentes
- **Autenticación por API Key**: Seguridad robusta
- **Respuestas estructuradas**: JSON estándar
- **Health checks**: Monitoreo del sistema

---

## 🏗️ Arquitectura Técnica

### Principios de Diseño
- **SOLID**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Clean Architecture**: Separación clara de responsabilidades
- **Strategy Pattern**: Extensibilidad para nuevas fuentes
- **Repository Pattern**: Abstracción del acceso a datos
- **Service Layer**: Lógica de negocio centralizada
- **Arquitectura por Capas**: Presentación, Servicios, Estrategias, Repositorio

### Stack Tecnológico
- **Backend**: Django 5.0 + Django REST Framework
- **Base de Datos**: PostgreSQL
- **Contenedores**: Docker + Docker Compose
- **Almacenamiento**: Google Drive API
- **Mensajería**: Twilio (WhatsApp), Telegram Bot API
- **Autenticación**: API Keys
- **Type Checking**: Pyright

### Arquitectura por Capas

#### 1. **Capa de Presentación (Presentation Layer)**
- **Views**: Manejo de requests HTTP
- **Serializers**: Transformación de datos
- **Authentication**: Validación de API Keys

#### 2. **Capa de Servicios (Service Layer)**
- **MessageService**: Procesamiento principal de mensajes
- **SummaryService**: Generación de resúmenes
- **SourceCredentialsService**: Manejo de credenciales
- **StrategyFactory**: Creación de estrategias

#### 3. **Capa de Estrategias (Strategy Pattern)**
- **WhatsAppStrategy**: Procesamiento WhatsApp
- **TelegramStrategy**: Procesamiento Telegram
- **BaseStrategy**: Interfaz común

#### 4. **Capa de Repositorio (Repository Pattern)**
- **MessageSelector**: Acceso a datos de mensajes
- **SourceSelector**: Acceso a datos de fuentes

### Componentes del Sistema

#### 1. **Models (Entidades)**
- `Source`: Fuentes de mensajería con credenciales
- `Message`: Archivos capturados con metadatos
- `Company`: Compañías para organización
- `User`: Usuarios extendidos de Django

#### 2. **Services (Lógica de Negocio)**
- `MessageService`: Procesamiento principal
- `SummaryService`: Generación de resúmenes
- `GoogleDriveService`: Gestión de archivos
- `SourceCredentialsService`: Manejo de credenciales

#### 3. **Strategies (Patrón Strategy)**
- `WhatsAppStrategy`: Procesamiento WhatsApp
- `TelegramStrategy`: Procesamiento Telegram

#### 4. **Selectors (Repository Pattern)**
- `MessageSelector`: Acceso a datos de mensajes
- `SourceSelector`: Acceso a datos de fuentes

#### 5. **Views (API Layer)**
- `AgentWebhookView`: Endpoint principal
- `HealthCheckView`: Monitoreo del sistema

---

## 📊 Modelos de Base de Datos

### 1. **Modelo Source (Fuentes de Mensajería)**
```python
class Source(models.Model):
    SOURCE_TYPES = [
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
        ('discord', 'Discord'),
    ]
    
    # Campos básicos
    name = models.CharField(max_length=50, choices=SOURCE_TYPES, unique=True)
    is_active = models.BooleanField(default=True)
    api_key = models.CharField(max_length=255, unique=True)
    webhook_url = models.URLField(blank=True, null=True)
    
    # Campos adicionales para credenciales y configuraciones
    additional1 = models.TextField(blank=True, null=True, help_text="Twilio Account SID, Telegram Bot Token")
    additional2 = models.TextField(blank=True, null=True, help_text="Twilio Auth Token, Telegram Chat ID")
    additional3 = models.TextField(blank=True, null=True, help_text="Twilio Phone Number, Telegram Webhook URL")
    additional4 = models.TextField(blank=True, null=True, help_text="Configuraciones adicionales, tokens de acceso")
    additional5 = models.TextField(blank=True, null=True, help_text="Configuraciones específicas de la integración")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 2. **Modelo Message (Archivos Capturados)**
```python
class Message(models.Model):
    FILE_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ]
    
    # Relación con Source
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='messages')
    
    # Información del archivo
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)
    file_size = models.BigIntegerField()  # en bytes
    
    # Información del remitente
    sender_number = models.CharField(max_length=20)  # Número de WhatsApp/Telegram
    
    # Metadatos de Drive
    drive_file_id = models.CharField(max_length=255, unique=True)
    drive_shared_link = models.URLField()
    drive_folder_path = models.CharField(max_length=500)
    
    # Timestamps
    received_at = models.DateTimeField(auto_now_add=True)
    uploaded_to_drive_at = models.DateTimeField(auto_now=True)
    
    # Estado del procesamiento
    is_processed = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True, null=True)
```

### 3. **Modelo Company (Compañías)**
```python
class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    drive_folder_id = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 4. **Modelo User (Usuarios - Django Auth)**
```python
class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
```

---

## 🔒 Sistema de Autenticación

### Autenticación por API Key
- **APIKeyAuthentication**: Validación de API Keys por fuente
- **UserIdentificationMiddleware**: Identificación de usuarios por número de teléfono
- **Relación User-Company**: Identificación de compañía para organización de archivos

### Flujo de Autenticación
1. Request con API Key → Validación de Source
2. Extracción de sender_number → Búsqueda de User
3. Identificación de Company → Estructura de carpetas
4. Procesamiento del archivo → Subida a Drive

---

## 📁 Estructura de Carpetas

### Estructura del Proyecto
```
drive_agent/
├── core/ (configuración Django)
├── apps/
│   ├── sources/ (modelo Source y lógica)
│   ├── messages/ (modelo Message y servicios)
│   ├── companies/ (modelo Company y lógica)
│   ├── users/ (modelo User extendido)
│   └── api/ (views, auth, middleware)
├── services/ (lógica de negocio)
│   ├── interfaces/ (contratos y abstracciones)
│   ├── message_service/
│   ├── summary_service/
│   └── strategy_factory/
├── selectors/ (repository pattern)
│   ├── interfaces/
│   └── message_selector/
├── utils/ (helpers y servicios externos)
│   ├── drive/ (Google Drive integration)
│   ├── strategies/ (WhatsApp, Telegram strategies)
│   │   ├── interfaces/
│   │   ├── whatsapp/
│   │   └── telegram/
│   └── validators/ (validaciones y helpers)
└── config/ (configuraciones adicionales)
```

### Estructura en Google Drive
```
Google Drive/
├── {company_name}/
│   ├── {sender_number}/
│   │   ├── {año}/
│   │   │   ├── {mes}/
│   │   │   │   ├── {día}/
│   │   │   │   │   ├── archivo1.jpg
│   │   │   │   │   └── archivo2.pdf
│   │   │   │   └── {día+1}/
│   │   │   └── {mes+1}/
│   │   └── {sender_number+1}/
│   └── {company_name+1}/
```

---

## 🚀 Roadmap de Desarrollo

### Fase 1: MVP (4-6 semanas)
- ✅ Configuración del proyecto Django con Docker
- ✅ Implementación de modelos base y migraciones
- ✅ Sistema de autenticación por API Key
- ✅ Integración con Google Drive API
- ✅ Estrategia WhatsApp con Twilio
- ✅ Webhook para recepción de archivos
- ✅ Sistema de comandos básicos (/resumen, /hoy, /semana)
- ✅ API REST funcional
- ✅ Testing básico

### Fase 2: Extensibilidad (2-3 semanas)
- 🔄 Estrategia Telegram
- 🔄 Mejoras en el sistema de comandos
- 🔄 Optimización de performance
- 🔄 Logging y monitoreo

### Fase 3: Mejoras de UX (Q1 2026)
- 🔄 Interfaz web para gestión
- 🔄 Dashboard de estadísticas
- 🔄 Exportación de datos
- 🔄 Notificaciones push

### Fase 4: Inteligencia Avanzada (Q2 2026)
- 📋 Categorización automática con IA
- 📋 Resúmenes inteligentes con NLP
- 📋 Sugerencias de contenido relacionado
- 📋 Análisis de tendencias

### Fase 5: Escalabilidad (Q3 2026)
- 📋 Soporte para más fuentes (Discord, Slack)
- 📋 Integración con más servicios de almacenamiento
- 📋 API pública para desarrolladores
- 📋 Marketplace de integraciones

---

## 📊 Métricas de Éxito

### Métricas Técnicas
- **Uptime**: > 99.5%
- **Response Time**: < 2 segundos
- **Error Rate**: < 1%
- **API Availability**: > 99.9%

### Métricas de Usuario
- **Archivos procesados**: > 5 por usuario activo
- **Búsquedas realizadas**: > 3 por usuario activo
- **Retención de usuarios**: > 80% después de 30 días

### Métricas de Negocio
- **Usuarios activos mensuales**: > 100
- **Tiempo de respuesta promedio**: < 1 segundo
- **Satisfacción del usuario**: > 4.5/5
- **Adopción de nuevas fuentes**: > 50% de usuarios

---

## 🔒 Requisitos de Seguridad

### Autenticación y Autorización
- **API Keys**: Autenticación por clave única por fuente
- **Validación de fuentes**: Verificación de fuentes activas
- **Rate Limiting**: Límites de requests por minuto
- **Logging de seguridad**: Registro de accesos y errores

### Protección de Datos
- **Encriptación en tránsito**: HTTPS obligatorio
- **Encriptación en reposo**: Base de datos encriptada
- **Credenciales seguras**: Variables de entorno y campos adicionales
- **Tokens de acceso**: Renovación automática

### Privacidad
- **Datos mínimos**: Solo información necesaria
- **Retención limitada**: Política de retención de datos
- **Acceso controlado**: Solo usuarios autorizados
- **Auditoría**: Registro de accesos y modificaciones

---

## 💰 Modelo de Negocio

### Estrategia de Monetización
1. **Freemium**: Funcionalidades básicas gratuitas
2. **Suscripción Pro**: Funcionalidades avanzadas
3. **Enterprise**: Soluciones corporativas
4. **API Licensing**: Acceso a la API para terceros

### Precios Propuestos
- **Free**: 100 archivos/mes, 1 fuente, almacenamiento básico
- **Pro ($9.99/mes)**: Archivos ilimitados, todas las fuentes, Google Drive
- **Enterprise ($49.99/mes)**: API completa, soporte prioritario, analytics

### Costos Operacionales
- **Infraestructura**: $50-100/mes
- **APIs externas**: $20-50/mes
- **Almacenamiento**: $10-30/mes
- **Desarrollo**: $2000-5000/mes

---

## 🧪 Plan de Testing

### Testing Funcional
- **Unit Tests**: Cobertura > 80%
- **Integration Tests**: APIs y servicios
- **End-to-End Tests**: Flujos completos
- **Performance Tests**: Carga y estrés

### Testing de Usuario
- **Beta Testing**: 10-20 usuarios iniciales
- **Usability Testing**: Flujos de usuario
- **A/B Testing**: Diferentes interfaces
- **Feedback Sessions**: Retroalimentación directa

### Testing de Seguridad
- **Penetration Testing**: Vulnerabilidades
- **Security Audits**: Revisión de código
- **Compliance Testing**: Cumplimiento de regulaciones
- **Data Privacy Testing**: Protección de datos

---

## 🔧 Configuraciones de Ejemplo

### Configuración WhatsApp (Twilio)
```python
whatsapp_source = Source.objects.create(
    name='whatsapp',
    api_key='whatsapp_api_key_123',
    additional1='TWILIO_ACCOUNT_SID_PLACEHOLDER',  # Twilio Account SID
    additional2='your_twilio_auth_token_here',          # Twilio Auth Token
    additional3='+1234567890',                          # Twilio Phone Number
    additional4='https://your-webhook-url.com/webhook', # Webhook URL
    additional5='{"verify_token": "your_verify_token"}' # Configuraciones adicionales
)
```

### Configuración Telegram
```python
telegram_source = Source.objects.create(
    name='telegram',
    api_key='telegram_api_key_456',
    additional1='1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ', # Bot Token
    additional2='@your_bot_username',                      # Bot Username
    additional3='https://your-webhook-url.com/telegram',  # Webhook URL
    additional4='{"chat_id": "-1001234567890"}',          # Chat ID
    additional5='{"parse_mode": "HTML"}'                  # Configuraciones adicionales
)
```

---

## 📋 Próximos Pasos de Implementación

### Semana 1-2: Configuración Base
1. Configurar entorno de desarrollo con Docker
2. Implementar modelos base y migraciones
3. Configurar Google Drive API
4. Implementar autenticación por API Key

### Semana 3-4: Integración WhatsApp
1. Configurar Twilio WhatsApp Business API
2. Implementar estrategia WhatsApp
3. Crear webhook básico para pruebas
4. Implementar subida de archivos a Drive

### Semana 5-6: Sistema de Comandos
1. Implementar comandos básicos (/resumen, /hoy, /semana)
2. Crear servicio de resúmenes
3. Implementar búsqueda por términos
4. Testing de integración

### Semana 7-8: API y Seguridad
1. Implementar endpoints REST completos
2. Configurar rate limiting y logging
3. Testing de seguridad
4. Documentación de API

---

**Documento aprobado por:** Rigo Drive Agent Team  
**Fecha de aprobación:** Diciembre 2024  
**Próxima revisión:** Marzo 2025
