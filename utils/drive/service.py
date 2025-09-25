import os
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from django.conf import settings
from apps.users.models import User
from apps.companies.models import Company
from apps.users.services import UserService
from utils.drive.service_account_client import GoogleDriveServiceAccountClient
import logging

logger = logging.getLogger(__name__)


class DriveService:
    """
    Servicio para manejar operaciones de Google Drive.
    Single Responsibility: Solo maneja lógica de negocio de Google Drive
    """
    
    def __init__(self):
        self.drive_client = GoogleDriveServiceAccountClient()
        self.user_service = UserService()
    
    def upload_file_from_message(self, file_content: bytes, filename: str, sender_number: str, 
                                file_type: str, mime_type: str = None, company_phone: str = None) -> Dict[str, Any]:
        """
        Sube un archivo a Google Drive organizándolo por estructura de carpetas.
        
        Args:
            file_content: Contenido del archivo en bytes
            filename: Nombre del archivo
            sender_number: Número del remitente
            file_type: Tipo de archivo (image, video, document, etc.)
            mime_type: Tipo MIME del archivo
            company_phone: Número de teléfono de la compañía para identificación
            
        Returns:
            Dict con información del archivo subido
        """
        try:
            # Obtener información del usuario y compañía usando UserService
            user, company = self.user_service.get_user_and_company_by_phone(sender_number, company_phone)
            
            if not user and not company:
                raise ValueError(f"No se encontró usuario o compañía para el número: {sender_number}")
            
            # Crear estructura de carpetas
            now = datetime.now()
            folder_id = self.drive_client.create_folder_structure(
                company_name=company.name,
                sender_number=sender_number,
                year=str(now.year),
                month=f"{now.month:02d}",
                day=f"{now.day:02d}"
            )
            
            # Generar nombre único para el archivo
            unique_filename = self._generate_unique_filename(filename, now)
            
            # Subir archivo
            upload_result = self.drive_client.upload_file(
                file_content=file_content,
                filename=unique_filename,
                folder_id=folder_id,
                mime_type=mime_type
            )
            
            # Generar ruta de la carpeta para almacenar en BD
            folder_path = f"/{company.name}/{sender_number}/{now.year}/{now.month:02d}/{now.day:02d}"
            
            logger.info(f"Archivo subido exitosamente: {unique_filename} para {company.name}")
            
            return {
                'drive_file_id': upload_result['file_id'],
                'drive_shared_link': upload_result['web_view_link'],
                'drive_folder_path': folder_path,
                'filename': unique_filename,
                'file_size': upload_result['size'],
                'company_name': company.name,
                'user_id': user.id if user else None
            }
            
        except Exception as e:
            logger.error(f"Error subiendo archivo desde mensaje: {e}")
            raise
    
    def _get_user_and_company(self, sender_number: str) -> Tuple[Optional[User], Optional[Company]]:
        """
        Obtiene el usuario y compañía basado en el número del remitente.
        
        Args:
            sender_number: Número del remitente
            
        Returns:
            Tuple con (User, Company) o (None, None) si no se encuentra
        """
        try:
            # Buscar usuario por número de teléfono
            print(f"Buscando usuario por número de teléfono: {sender_number}")
            user = User.objects.filter(phone_number=sender_number).first()
            
            if user and user.company:
                return user, user.company
            
            # Si no se encuentra usuario, usar compañía por defecto
            # Por ahora usaremos la primera compañía activa
            default_company = Company.objects.filter(is_active=True).first()
            
            if default_company:
                logger.warning(f"No se encontró usuario para {sender_number}, usando compañía por defecto: {default_company.name}")
                return None, default_company
            
            return None, None
            
        except Exception as e:
            logger.error(f"Error obteniendo usuario y compañía para {sender_number}: {e}")
            return None, None
    
    def _generate_unique_filename(self, filename: str, timestamp: datetime) -> str:
        """
        Genera un nombre único para el archivo.
        
        Args:
            filename: Nombre original del archivo
            timestamp: Timestamp de creación
            
        Returns:
            str: Nombre único del archivo
        """
        try:
            # Separar nombre y extensión
            name, ext = os.path.splitext(filename)
            
            # Crear timestamp único
            timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
            
            # Generar nombre único
            unique_name = f"{name}_{timestamp_str}{ext}"
            
            return unique_name
            
        except Exception as e:
            logger.error(f"Error generando nombre único para {filename}: {e}")
            # Fallback: usar timestamp como nombre
            return f"file_{timestamp.strftime('%Y%m%d_%H%M%S')}"
    
    def get_folder_contents(self, folder_path: str) -> list:
        """
        Obtiene el contenido de una carpeta.
        
        Args:
            folder_path: Ruta de la carpeta
            
        Returns:
            list: Lista de archivos en la carpeta
        """
        try:
            # TODO: Implementar búsqueda de carpeta por ruta
            # Por ahora retornamos lista vacía
            return []
            
        except Exception as e:
            logger.error(f"Error obteniendo contenido de carpeta {folder_path}: {e}")
            return []
    
    def create_summary_report(self, company_name: str, date_from: datetime, date_to: datetime) -> Dict[str, Any]:
        """
        Crea un reporte de resumen de archivos subidos.
        
        Args:
            company_name: Nombre de la compañía
            date_from: Fecha desde
            date_to: Fecha hasta
            
        Returns:
            Dict con resumen de archivos
        """
        try:
            # TODO: Implementar lógica de reportes
            # Por ahora retornamos estructura básica
            return {
                'company_name': company_name,
                'date_from': date_from.isoformat(),
                'date_to': date_to.isoformat(),
                'total_files': 0,
                'files_by_type': {},
                'files_by_sender': {}
            }
            
        except Exception as e:
            logger.error(f"Error creando reporte de resumen: {e}")
            return {}
