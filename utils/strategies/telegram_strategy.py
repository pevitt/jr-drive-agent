import requests
from typing import Dict, Any, Optional
from django.http import JsonResponse
from django.conf import settings
from utils.strategies.base import MessageStrategy
from utils.drive.service import DriveService
from apps.agentmessages.services import MessageService as AgentMessageService
from apps.users.services import UserService
from apps.sources.services import SourceService


class TelegramStrategy(MessageStrategy):
    """
    Estrategia para procesar mensajes de Telegram.
    Single Responsibility: Solo maneja mensajes de Telegram
    """
    
    def __init__(self, source):
        super().__init__(source)
        self.message_service = AgentMessageService()
        self.user_service = UserService()
        self.source_service = SourceService()
    
    def process_message(self, data: Dict[str, Any]) -> JsonResponse:
        """
        Procesa un mensaje de Telegram.
        
        Args:
            data: Datos del webhook de Telegram
            
        Returns:
            JsonResponse: Respuesta del procesamiento
        """
        try:
            # Telegram envía updates, necesitamos extraer el mensaje
            message = data.get('message', {})
            if not message:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No se encontró mensaje en el update de Telegram'
                }, status=400)
            
            # Extraer información básica
            sender_number = str(message.get('from', {}).get('id', ''))
            chat_id = message.get('chat', {}).get('id')
            message_id = message.get('message_id')
            
            # Validar si el mensaje contiene archivo
            if not self.validate_message(data):
                return self.create_no_file_response(sender_number, 'telegram')
            
            # Extraer información del archivo
            file_info = self.extract_file_info(data)
            if not file_info:
                # Guardar mensaje sin archivo en la base de datos
                message = self._save_message_to_db(data, sender_number, None, None)
                return JsonResponse({
                    'status': 'success',
                    'message': 'Mensaje sin archivo',
                    'data': {
                        'sender_number': sender_number,
                        'platform': 'telegram',
                        'has_file': False,
                        'chat_id': chat_id,
                        'message_id': message_id,
                        'message_id': message.id if message else None
                    }
                }, status=200)
            
            # Procesar el archivo: descargar y subir a Drive
            drive_result = self._process_file_to_drive(file_info, sender_number)
            
            # Guardar mensaje en la base de datos
            message = self._save_message_to_db(data, sender_number, file_info, drive_result)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Archivo recibido y procesado',
                'data': {
                    'sender_number': sender_number,
                    'platform': 'telegram',
                    'has_file': True,
                    'file_info': file_info,
                    'drive_info': drive_result,
                    'chat_id': chat_id,
                    'message_id': message_id,
                    'db_message_id': message.id if message else None
                }
            }, status=200)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error procesando mensaje de Telegram: {str(e)}'
            }, status=500)
    
    def validate_message(self, data: Dict[str, Any]) -> bool:
        """
        Valida si el mensaje de Telegram contiene un archivo.
        
        Args:
            data: Datos del update de Telegram
            
        Returns:
            bool: True si contiene archivo multimedia
        """
        message = data.get('message', {})
        
        # Verificar diferentes tipos de archivos que Telegram puede enviar
        file_fields = [
            'photo', 'video', 'document', 'audio', 'voice', 
            'video_note', 'sticker', 'animation'
        ]
        
        for field in file_fields:
            if field in message and message[field]:
                return True
        
        return False
    
    def extract_file_info(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extrae información del archivo del mensaje de Telegram.
        
        Args:
            data: Datos del update de Telegram
            
        Returns:
            Dict con información del archivo o None
        """
        try:
            message = data.get('message', {})
            sender_info = message.get('from', {})
            
            # Determinar tipo de archivo y extraer información
            file_type, file_data = self._get_file_data(message)
            
            if not file_type or not file_data:
                return None
            
            # Obtener información del archivo
            file_id = file_data.get('file_id')
            file_unique_id = file_data.get('file_unique_id')
            
            # Obtener nombre del archivo si está disponible
            filename = file_data.get('file_name', f'telegram_file_{file_unique_id}')
            
            # Obtener tamaño del archivo
            file_size = file_data.get('file_size', 0)
            
            # Obtener información del remitente
            sender_number = str(sender_info.get('id', ''))
            sender_username = sender_info.get('username', '')
            sender_first_name = sender_info.get('first_name', '')
            
            return {
                'file_id': file_id,
                'file_unique_id': file_unique_id,
                'filename': filename,
                'file_type': file_type,
                'file_size': file_size,
                'sender_number': sender_number,
                'sender_username': sender_username,
                'sender_first_name': sender_first_name,
                'chat_id': message.get('chat', {}).get('id'),
                'message_id': message.get('message_id'),
                'timestamp': message.get('date'),
            }
            
        except Exception as e:
            print(f"Error extrayendo información del archivo de Telegram: {e}")
            return None
    
    def _get_file_data(self, message: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
        """
        Extrae los datos del archivo según su tipo.
        
        Args:
            message: Datos del mensaje de Telegram
            
        Returns:
            tuple: (tipo_archivo, datos_archivo)
        """
        # Verificar diferentes tipos de archivos
        if 'photo' in message and message['photo']:
            # Las fotos en Telegram vienen en diferentes resoluciones
            # Tomamos la de mayor resolución (última en la lista)
            photo = message['photo'][-1]  # Mayor resolución
            return 'image', photo
        
        elif 'video' in message and message['video']:
            return 'video', message['video']
        
        elif 'document' in message and message['document']:
            return 'document', message['document']
        
        elif 'audio' in message and message['audio']:
            return 'audio', message['audio']
        
        elif 'voice' in message and message['voice']:
            return 'audio', message['voice']
        
        elif 'video_note' in message and message['video_note']:
            return 'video', message['video_note']
        
        elif 'sticker' in message and message['sticker']:
            return 'image', message['sticker']
        
        elif 'animation' in message and message['animation']:
            return 'video', message['animation']
        
        return None, {}
    
    def download_file(self, file_id: str, bot_token: str) -> Optional[bytes]:
        """
        Descarga el archivo desde Telegram usando la Bot API.
        
        Args:
            file_id: ID del archivo en Telegram
            bot_token: Token del bot de Telegram
            
        Returns:
            bytes: Contenido del archivo o None si hay error
        """
        try:
            # Primero obtener la información del archivo
            get_file_url = f"https://api.telegram.org/bot{bot_token}/getFile"
            get_file_response = requests.get(get_file_url, params={'file_id': file_id})
            get_file_response.raise_for_status()
            
            file_info = get_file_response.json()
            if not file_info.get('ok'):
                return None
            
            file_path = file_info['result']['file_path']
            
            # Descargar el archivo
            download_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
            download_response = requests.get(download_url)
            download_response.raise_for_status()
            
            return download_response.content
            
        except Exception as e:
            print(f"Error descargando archivo desde Telegram: {e}")
            return None
    
    def _process_file_to_drive(self, file_info: Dict[str, Any], sender_number: str) -> Dict[str, Any]:
        """
        Procesa un archivo descargándolo y subiéndolo a Google Drive.
        
        Args:
            file_info: Información del archivo
            sender_number: Número del remitente
            
        Returns:
            Dict con información del archivo en Drive
        """
        try:
            # Obtener token del bot desde la fuente
            # Por ahora usamos token por defecto para testing
            bot_token = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"  # TODO: Obtener desde source
            
            # Descargar archivo desde Telegram
            file_content = self.download_file(
                file_info['file_id'], 
                bot_token
            )
            
            if not file_content:
                raise Exception("No se pudo descargar el archivo desde Telegram")
            
            # Determinar MIME type basado en el tipo de archivo
            mime_type = self._get_mime_type_from_file_type(file_info['file_type'])
            
            # Subir a Google Drive
            drive_service = DriveService()
            drive_result = drive_service.upload_file_from_message(
                file_content=file_content,
                filename=file_info['filename'],
                sender_number=sender_number,
                file_type=file_info['file_type'],
                mime_type=mime_type
            )
            
            return drive_result
            
        except Exception as e:
            print(f"Error procesando archivo a Drive: {e}")
            return {'error': str(e)}
    
    def _get_mime_type_from_file_type(self, file_type: str) -> str:
        """
        Obtiene el MIME type basado en el tipo de archivo.
        
        Args:
            file_type: Tipo de archivo
            
        Returns:
            str: MIME type correspondiente
        """
        mime_types = {
            'image': 'image/jpeg',
            'video': 'video/mp4',
            'audio': 'audio/mpeg',
            'document': 'application/pdf',
            'other': 'application/octet-stream'
        }
        
        return mime_types.get(file_type, 'application/octet-stream')
    
    def _save_message_to_db(self, payload: dict, sender_number: str, file_info: dict = None, drive_result: dict = None):
        """
        Guarda el mensaje en la base de datos usando el service.
        
        Args:
            payload: Payload completo del webhook
            sender_number: Número del remitente
            file_info: Información del archivo (si existe)
            drive_result: Resultado de la subida a Drive (si existe)
            
        Returns:
            Message: Instancia del mensaje guardado o None si hay error
        """
        try:
            # Extraer información del mensaje
            message_data = payload.get('message', {})
            message_text = message_data.get('text', '')
            message_id = str(message_data.get('message_id', ''))
            
            # Preparar datos del mensaje
            message_data_dict = {
                'source': self.source,
                'sender_number': sender_number,
                'message_id': message_id,
                'message_text': message_text,
            }
            
            # Agregar información del archivo si existe
            if file_info:
                message_data_dict.update({
                    'filename': file_info.get('filename', ''),
                    'file_type': file_info.get('file_type', ''),
                    'file_size': file_info.get('file_size', 0),
                    'content_type': file_info.get('content_type', ''),
                })
            
            # Agregar información de Drive si existe
            if drive_result and 'drive_file_id' in drive_result:
                message_data_dict.update({
                    'drive_file_id': drive_result['drive_file_id'],
                    'drive_shared_link': drive_result['drive_shared_link'],
                    'drive_folder_path': drive_result['drive_folder_path'],
                })
            
            # Usar el service para crear el mensaje
            message = self.message_service.create_message(message_data_dict)
            
            if message:
                print(f"Mensaje guardado en BD: ID {message.id}, Sender: {sender_number}")
            
            return message
            
        except Exception as e:
            print(f"Error guardando mensaje en BD: {e}")
            return None
    
