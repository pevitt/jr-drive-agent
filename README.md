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

## Configuración de Google Drive con Service Account

### ¿Por qué usar Service Account?

- ✅ **Sin expiraciones**: Los tokens no expiran nunca
- ✅ **Cuenta empresarial**: Identidad dedicada para tu aplicación
- ✅ **Unidades compartidas por cliente**: Cada cliente tiene su propia carpeta
- ✅ **Escalabilidad**: Fácil agregar nuevos clientes
- ✅ **Sin reautenticación manual**: Configuración inicial única

### 1. Crear Service Account en Google Cloud Console

#### Paso 1: Acceder a Google Cloud Console
```bash
# Ve a Google Cloud Console
https://console.cloud.google.com/
```

#### Paso 2: Crear o seleccionar proyecto
1. Selecciona un proyecto existente o crea uno nuevo
2. Anota el **Project ID** (lo necesitarás más tarde)

#### Paso 3: Habilitar Google Drive API
1. Ve a **"APIs & Services"** → **"Library"**
2. Busca **"Google Drive API"**
3. Clic en **"Enable"**

#### Paso 4: Crear Service Account
1. Ve a **"IAM & Admin"** → **"Service Accounts"**
2. Clic en **"Create Service Account"**
3. Completa los campos:
   - **Service account name**: `jr-drive-agent-service`
   - **Service account ID**: `jr-drive-agent-service` (se genera automáticamente)
   - **Description**: `Service account para JR Drive Agent`
4. Clic en **"Create and Continue"**

#### Paso 5: Asignar roles
1. En **"Grant this service account access to project"**:
   - Selecciona **"Editor"** o **"Storage Admin"**
2. Clic en **"Continue"**
3. Clic en **"Done"**

#### Paso 6: Crear y descargar clave
1. Busca el Service Account creado en la lista
2. Clic en el **email del Service Account**
3. Ve a la pestaña **"Keys"**
4. Clic en **"Add Key"** → **"Create New Key"**
5. Selecciona **"JSON"**
6. Clic en **"Create"**
7. El archivo se descarga automáticamente

### 2. Configurar archivos en el proyecto

#### Paso 1: Colocar archivo de credenciales
```bash
# Copiar el archivo descargado a tu proyecto
cp ~/Downloads/your-project-name-xxxxx.json credentials/service_account.json
```

#### Paso 2: Verificar estructura de archivos
```bash
credentials/
├── service_account.json  # ← Archivo del Service Account
├── credentials.json      # ← Opcional (para OAuth tradicional)
└── token.json           # ← Opcional (para OAuth tradicional)
```

### 3. Crear y configurar carpetas compartidas en Google Drive

#### Paso 1: Crear carpeta para cada cliente
1. Ve a **Google Drive** (https://drive.google.com)
2. Clic derecho en espacio vacío → **"Nueva carpeta"**
3. Nombre: `Cliente A - Empresa XYZ`
4. Clic en **"Crear"**

#### Paso 2: Obtener ID de la carpeta
1. Clic en la carpeta para abrirla
2. Mira la URL en el navegador:
   ```
   https://drive.google.com/drive/folders/1XqhwTc_anck6Rt_J9N6AZ2HaXWoEGLKe
                                                      ↑
                                              Este es el ID
   ```
3. Copia el ID: `1XqhwTc_anck6Rt_J9N6AZ2HaXWoEGLKe`

#### Paso 3: Compartir carpeta con Service Account
1. Clic derecho en la carpeta → **"Compartir"**
2. En **"Agregar personas y grupos"**:
   - Ingresa el **email del Service Account** (lo encuentras en el archivo JSON)
   - Ejemplo: `jr-drive-agent-service@tu-proyecto.iam.gserviceaccount.com`
3. Permisos: **"Editor"**
4. Clic en **"Enviar"**

#### Paso 4: Repetir para cada cliente
```bash
# Ejemplo de estructura de carpetas por cliente
Cliente A - Empresa XYZ/     → ID: 1XqhwTc_anck6Rt_J9N6AZ2HaXWoEGLKe
Cliente B - Empresa ABC/     → ID: 1ABC123DEF456GHI789
Cliente C - Empresa DEF/     → ID: 1XYZ789ABC123DEF456
```

### 4. Configurar companies en la base de datos

#### Paso 1: Actualizar comando de carga
Edita `apps/companies/management/commands/load_companies.py`:

```python
companies_data = [
    {
        'name': 'Empresa XYZ',
        'phone_number': '+573212518445',
        'drive_folder_id': '1XqhwTc_anck6Rt_J9N6AZ2HaXWoEGLKe',  # Tu ID real
        'is_active': True,
    },
    {
        'name': 'Empresa ABC',
        'phone_number': '+573001234567',
        'drive_folder_id': '1ABC123DEF456GHI789',  # ID de otra carpeta
        'is_active': True,
    },
]
```

#### Paso 2: Cargar companies
```bash
# Cargar companies con carpetas de Drive
docker compose exec web python manage.py load_companies
```

### 5. Verificar configuración

#### Paso 1: Probar conexión
```bash
# Probar que el Service Account funciona
docker compose exec web python manage.py test_drive
```

#### Paso 2: Verificar estructura en Drive
Después de procesar un mensaje, deberías ver:
```
Cliente A - Empresa XYZ/
├── +573212518445/           # Número del remitente
│   ├── 2025/                # Año
│   │   ├── 09/              # Mes
│   │   │   ├── 23/          # Día
│   │   │   │   ├── archivo_20250923_143022.jpg
│   │   │   │   └── documento_20250923_143045.pdf
```

### 6. Ventajas del Service Account vs OAuth

| Característica | OAuth 2.0 | Service Account |
|----------------|-----------|-----------------|
| **Expiraciones** | ❌ Tokens expiran | ✅ Sin expiraciones |
| **Reautenticación** | ❌ Requerida | ✅ No requerida |
| **Cuenta personal** | ❌ Usa tu cuenta | ✅ Cuenta dedicada |
| **Múltiples clientes** | ❌ Complejo | ✅ Fácil |
| **Escalabilidad** | ❌ Limitada | ✅ Excelente |
| **Configuración inicial** | ✅ Fácil | ⚠️ Más pasos |

### 7. Migración desde OAuth a Service Account

Si ya tienes el sistema funcionando con OAuth:

#### Paso 1: Backup de datos
```bash
# Hacer backup de la base de datos
docker compose exec db pg_dump -U postgres drive_agent_db > backup.sql
```

#### Paso 2: Configurar Service Account
Sigue los pasos 1-3 de esta guía

#### Paso 3: Actualizar código
```bash
# El código ya está actualizado para usar Service Account
# Solo necesitas configurar los archivos y carpetas
```

#### Paso 4: Probar sistema
```bash
# Probar con un mensaje de WhatsApp
# Verificar que se sube a la carpeta correcta
```

### 8. Troubleshooting

#### Error: "Service Account file not found"
```bash
# Verificar que el archivo existe
ls -la credentials/service_account.json

# Verificar permisos
chmod 644 credentials/service_account.json
```

#### Error: "Permission denied on folder"
```bash
# Verificar que la carpeta está compartida con el Service Account
# El email del Service Account debe tener permisos de "Editor"
```

#### Error: "Invalid folder ID"
```bash
# Verificar que el ID de la carpeta es correcto
# Debe ser algo como: 1XqhwTc_anck6Rt_J9N6AZ2HaXWoEGLKe
```

### Configuración tradicional de Google Drive (OAuth 2.0)

Si prefieres usar OAuth 2.0 tradicional:

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
