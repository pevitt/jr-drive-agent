# Drive Agent

Sistema inteligente de gestión de archivos multimedia que captura y organiza automáticamente archivos de fuentes de mensajería (WhatsApp, Telegram) y los sube a Google Drive organizados por cliente, año, mes y día.

## Características

- **Multi-canal**: Soporte para WhatsApp (Twilio) y Telegram
- **Organización automática**: Archivos organizados por compañía/fecha en Google Drive
- **Resúmenes estructurados**: Reportes de archivos subidos
- **Comandos del sistema**: `/resumen`, `/hoy`, `/semana`, `/buscar`
- **API REST**: Webhooks, autenticación por API Key, respuestas JSON

## Tecnologías

- **Backend**: Django 5.0 + Django REST Framework
- **Base de datos**: PostgreSQL
- **Containerización**: Docker + Docker Compose
- **APIs**: Twilio (WhatsApp), Telegram Bot API
- **Almacenamiento**: Google Drive API

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd jr-drive-agent
```

### 2. Configurar variables de entorno
```bash
cp env.example .env
# Editar .env con tus credenciales
```

### 3. Configurar credenciales de Google Drive
```bash
# Crear directorio para credenciales
mkdir -p credentials

# Copiar archivos de credenciales de Google Drive
# Reemplaza 'path/to/your/' con la ruta real de tus archivos
cp path/to/your/credentials.json credentials/
cp path/to/your/token.json credentials/

# O si tienes los archivos en otro proyecto:
docker cp <container_id>:/app/credentials/credentials.json ./credentials/
docker cp <container_id>:/app/credentials/token.json ./credentials/
```

### 4. Ejecutar con Docker
```bash
# Construir y ejecutar
make up

# O manualmente:
docker compose up --build
```

### 5. Cargar datos iniciales
```bash
# Cargar compañías y fuentes iniciales
docker compose run web python manage.py load_initial_data
```

### 6. Crear superusuario (opcional)
```bash
docker compose run web python manage.py createsuperuser
```

## Estructura del Proyecto

```
├── apps/
│   ├── api/           # API REST endpoints
│   ├── companies/     # Gestión de compañías
│   ├── sources/       # Fuentes de mensajería (WhatsApp, Telegram)
│   ├── users/         # Usuarios del sistema
│   └── agentmessages/ # Mensajes y archivos capturados
├── core/              # Configuración principal de Django
├── utils/
│   ├── drive/         # Integración con Google Drive
│   └── strategies/    # Estrategias de integración (Twilio, Telegram)
└── requirements.txt
```

## API Endpoints

- `GET /api/health/` - Health check
- `POST /api/webhook/whatsapp/` - Webhook para recibir archivos de WhatsApp (Twilio)
- `POST /api/webhook/telegram/` - Webhook para recibir archivos de Telegram

## Comandos de Gestión

```bash
# Cargar datos iniciales (compañías y fuentes)
docker compose run web python manage.py load_initial_data

# Cargar solo compañías
docker compose run web python manage.py load_companies

# Cargar solo fuentes
docker compose run web python manage.py load_sources

# Probar conexión con Google Drive
docker compose run web python manage.py test_drive

# Crear migraciones
docker compose run web python manage.py makemigrations

# Aplicar migraciones
docker compose run web python manage.py migrate

# Acceder al shell de Django
docker compose run web python manage.py shell
```

## Desarrollo

### Ejecutar localmente (sin Docker)
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos (SQLite para desarrollo)
python manage.py migrate

# Cargar datos iniciales
python manage.py load_initial_data

# Ejecutar servidor
python manage.py runserver
```

### Estructura de Archivos en Google Drive
```
/Drive Agent/
├── {company_name}/
│   ├── {sender_number}/
│   │   ├── {year}/
│   │   │   ├── {month}/
│   │   │   │   ├── {day}/
│   │   │   │   │   └── archivos...
```

**Ejemplo de estructura:**
```
/Drive Agent/
├── Rigoberto/
│   ├── +1234567890/
│   │   ├── 2025/
│   │   │   ├── 09/
│   │   │   │   ├── 14/
│   │   │   │   │   ├── imagen_20250914_143022.jpg
│   │   │   │   │   ├── documento_20250914_143045.pdf
│   │   │   │   │   └── video_20250914_143100.mp4
```

### Configuración de Google Drive

1. **Crear proyecto en Google Cloud Console**
2. **Habilitar Google Drive API**
3. **Crear credenciales OAuth 2.0**
4. **Descargar `credentials.json`**
5. **Copiar archivos a la carpeta `credentials/`**

Los archivos necesarios:
- `credentials/credentials.json` - Credenciales OAuth 2.0
- `credentials/token.json` - Token de acceso (se genera automáticamente)

## Uso de Webhooks

### WhatsApp (Twilio)
```bash
curl -X POST http://localhost:8000/api/webhook/whatsapp/ \
  -H "Content-Type: application/json" \
  -d '{
    "From": "whatsapp:+1234567890",
    "Body": "Mensaje de prueba",
    "MessageType": "text",
    "MessageSid": "SM1234567890abcdef"
  }'
```

### Telegram
```bash
curl -X POST http://localhost:8000/api/webhook/telegram/ \
  -H "Content-Type: application/json" \
  -d '{
    "update_id": 123456789,
    "message": {
      "message_id": 123,
      "from": {"id": 987654321, "first_name": "Test"},
      "chat": {"id": 987654321, "type": "private"},
      "date": 1694629800,
      "text": "Mensaje de prueba"
    }
  }'
```

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.
