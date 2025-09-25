import os
from typing import Optional, Dict, Any
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import logging

logger = logging.getLogger(__name__)


class GoogleDriveServiceAccountClient:
    """
    Cliente para interactuar con Google Drive API usando Service Account.
    Single Responsibility: Solo maneja operaciones con Google Drive usando Service Account
    """
    
    # Scopes necesarios para Google Drive
    SCOPES = [
        'https://www.googleapis.com/auth/drive'
    ]
    
    def __init__(self, service_account_file: str = None):
        """
        Inicializa el cliente con Service Account.
        
        Args:
            service_account_file: Ruta al archivo JSON del Service Account
        """
        self.service = None
        self.credentials = None
        
        # Ruta por defecto al archivo de Service Account
        if not service_account_file:
            service_account_file = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'credentials',
                'service_account.json'
            )
        
        self.service_account_file = service_account_file
        self._authenticate()
    
    def _authenticate(self):
        """
        Autentica con Google Drive API usando Service Account.
        """
        try:
            if not os.path.exists(self.service_account_file):
                raise FileNotFoundError(f"Archivo de Service Account no encontrado: {self.service_account_file}")
            
            # Cargar credenciales del Service Account
            self.credentials = service_account.Credentials.from_service_account_file(
                self.service_account_file,
                scopes=self.SCOPES
            )
            
            # Construir el servicio
            self.service = build('drive', 'v3', credentials=self.credentials)
            logger.info("Autenticación con Google Drive usando Service Account exitosa")
            
        except Exception as e:
            logger.error(f"Error autenticando con Service Account: {e}")
            raise
    
    def create_folder_structure_in_company_folder(self, company_folder_id: str, sender_number: str, year: str, month: str, day: str) -> str:
        """
        Crea la estructura de carpetas dentro de la carpeta de la compañía.
        
        Args:
            company_folder_id: ID de la carpeta de la compañía
            sender_number: Número del remitente
            year: Año
            month: Mes
            day: Día
            
        Returns:
            str: ID de la carpeta del día
        """
        try:
            # Estructura: /{company_folder}/{sender}/{year}/{month}/{day}
            folder_names = [
                sender_number,
                year,
                month,
                day
            ]
            
            current_parent_id = company_folder_id
            current_path = ""
            
            for folder_name in folder_names:
                current_path = f"{current_path}/{folder_name}" if current_path else folder_name
                
                # Buscar si la carpeta ya existe
                folder_id = self._find_folder_by_name(folder_name, current_parent_id)
                
                if not folder_id:
                    # Crear la carpeta si no existe
                    folder_id = self._create_folder(folder_name, current_parent_id)
                    logger.info(f"Carpeta creada: {current_path} (ID: {folder_id})")
                else:
                    logger.info(f"Carpeta encontrada: {current_path} (ID: {folder_id})")
                
                current_parent_id = folder_id
            
            return folder_id
            
        except Exception as e:
            logger.error(f"Error creando estructura de carpetas en carpeta de compañía: {e}")
            raise
    
    def _find_folder_by_name(self, folder_name: str, parent_id: Optional[str] = None) -> Optional[str]:
        """
        Busca una carpeta por nombre y padre.
        
        Args:
            folder_name: Nombre de la carpeta
            parent_id: ID de la carpeta padre
            
        Returns:
            str: ID de la carpeta si existe, None si no
        """
        try:
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            
            if parent_id:
                query += f" and '{parent_id}' in parents"
            
            results = self.service.files().list(
                q=query,
                fields="files(id, name)"
            ).execute()
            
            folders = results.get('files', [])
            return folders[0]['id'] if folders else None
            
        except Exception as e:
            logger.error(f"Error buscando carpeta '{folder_name}': {e}")
            return None
    
    def _create_folder(self, folder_name: str, parent_id: Optional[str] = None) -> str:
        """
        Crea una carpeta en Google Drive.
        
        Args:
            folder_name: Nombre de la carpeta
            parent_id: ID de la carpeta padre
            
        Returns:
            str: ID de la carpeta creada
        """
        try:
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_id:
                folder_metadata['parents'] = [parent_id]
            
            folder = self.service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
            
            return folder.get('id')
            
        except Exception as e:
            logger.error(f"Error creando carpeta '{folder_name}': {e}")
            raise
    
    def upload_file(self, file_content: bytes, filename: str, folder_id: str, mime_type: str = None) -> Dict[str, Any]:
        """
        Sube un archivo a Google Drive.
        
        Args:
            file_content: Contenido del archivo en bytes
            filename: Nombre del archivo
            folder_id: ID de la carpeta destino
            mime_type: Tipo MIME del archivo
            
        Returns:
            Dict con información del archivo subido
        """
        try:
            # Crear metadata del archivo
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            
            # Crear objeto de media
            media = MediaIoBaseUpload(
                io.BytesIO(file_content),
                mimetype=mime_type,
                resumable=True
            )
            
            # Subir archivo
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,size,webViewLink,webContentLink'
            ).execute()
            
            logger.info(f"Archivo subido exitosamente: {filename} (ID: {file.get('id')})")
            
            return {
                'file_id': file.get('id'),
                'filename': file.get('name'),
                'size': file.get('size'),
                'web_view_link': file.get('webViewLink'),
                'web_content_link': file.get('webContentLink'),
                'folder_id': folder_id
            }
            
        except Exception as e:
            logger.error(f"Error subiendo archivo '{filename}': {e}")
            raise
    
    def get_file_info(self, file_id: str) -> Dict[str, Any]:
        """
        Obtiene información de un archivo en Google Drive.
        
        Args:
            file_id: ID del archivo en Google Drive
            
        Returns:
            Dict con información del archivo
        """
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields='id,name,size,mimeType,createdTime,modifiedTime,webViewLink,webContentLink'
            ).execute()
            
            return {
                'file_id': file.get('id'),
                'filename': file.get('name'),
                'size': file.get('size'),
                'mime_type': file.get('mimeType'),
                'created_time': file.get('createdTime'),
                'modified_time': file.get('modifiedTime'),
                'web_view_link': file.get('webViewLink'),
                'web_content_link': file.get('webContentLink')
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo información del archivo '{file_id}': {e}")
            raise
