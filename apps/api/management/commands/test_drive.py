from django.core.management.base import BaseCommand
from utils.drive.service import DriveService
import os


class Command(BaseCommand):
    """
    Comando para probar la conexión con Google Drive.
    Single Responsibility: Solo prueba la conexión con Google Drive
    """
    help = 'Prueba la conexión con Google Drive y crea una carpeta de prueba'

    def handle(self, *args, **options):
        """
        Ejecuta el comando para probar Google Drive
        """
        self.stdout.write(self.style.SUCCESS('🔍 Probando conexión con Google Drive...'))
        
        try:
            # Verificar que existan las credenciales
            credentials_path = 'credentials/credentials.json'
            if not os.path.exists(credentials_path):
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ Archivo de credenciales no encontrado: {credentials_path}\n'
                        'Por favor, copia tu archivo credentials.json a la carpeta credentials/'
                    )
                )
                return
            
            # Crear instancia del servicio
            drive_service = DriveService()
            self.stdout.write(self.style.SUCCESS('✅ Conexión con Google Drive establecida'))
            
            # Crear estructura de prueba
            self.stdout.write(self.style.MIGRATE_HEADING('📁 Creando estructura de prueba...'))
            
            folder_id = drive_service.drive_client.create_folder_structure(
                company_name='Test Company',
                sender_number='+1234567890',
                year='2025',
                month='09',
                day='14'
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Estructura de carpetas creada exitosamente\n'
                    f'   ID de carpeta: {folder_id}\n'
                    f'   Ruta: /Drive Agent/Test Company/+1234567890/2025/09/14'
                )
            )
            
            # Crear archivo de prueba
            self.stdout.write(self.style.MIGRATE_HEADING('📄 Creando archivo de prueba...'))
            
            test_content = b'Archivo de prueba creado por Drive Agent'
            upload_result = drive_service.drive_client.upload_file(
                file_content=test_content,
                filename='test_file.txt',
                folder_id=folder_id,
                mime_type='text/plain'
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Archivo de prueba creado exitosamente\n'
                    f'   Nombre: {upload_result["filename"]}\n'
                    f'   ID: {upload_result["file_id"]}\n'
                    f'   Enlace: {upload_result["web_view_link"]}'
                )
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    '\n🎉 ¡Prueba de Google Drive completada exitosamente!\n'
                    'El sistema está listo para procesar archivos.'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Error probando Google Drive: {str(e)}\n\n'
                    'Verifica que:\n'
                    '1. El archivo credentials.json esté en la carpeta credentials/\n'
                    '2. Las credenciales sean válidas\n'
                    '3. La Google Drive API esté habilitada en tu proyecto de Google Cloud'
                )
            )
