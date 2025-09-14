import requests
from typing import Dict, Any, Optional
from django.http import JsonResponse
from django.conf import settings
from utils.strategies.base import MessageStrategy
from utils.drive.service import DriveService
from apps.agentmessages.services import MessageService as AgentMessageService
from apps.users.services import UserService
from apps.sources.services import SourceService
from utils.services.whatsapp_service import WhatsAppService


class TwilioWhatsAppStrategy(MessageStrategy):
    """
    Estrategia para procesar mensajes de WhatsApp a través de Twilio.
    Single Responsibility: Solo maneja mensajes de WhatsApp/Twilio
    """
    
    def __init__(self, source):
        super().__init__(source)
        self.message_service = AgentMessageService()
        self.user_service = UserService()
        self.source_service = SourceService()
        self.whatsapp_service = WhatsAppService(source)
    
    def process_message(self, data: Dict[str, Any]) -> JsonResponse:
        """
        Procesa un mensaje de WhatsApp desde Twilio.
        
        Args:
            data: Datos del webhook de Twilio
            
        Returns:
            JsonResponse: Respuesta del procesamiento
        """
        try:
            # Extraer información básica del mensaje
            sender_number = data.get('From', '').replace('whatsapp:', '')
            message_body = data.get('Body', '')
            message_type = data.get('MessageType', '')
            
            # Extraer número de compañía del campo 'From' (número del cliente/empresa)
            company_phone = data.get('From', '').replace('whatsapp:', '')
            
            
            # Verificar si el mensaje contiene archivo
            has_file = self.validate_message(data)
            
            if has_file:
                # Extraer información del archivo
                file_info = self.extract_file_info(data)
                
                if not file_info:
                    # Si no se pudo extraer info del archivo, guardar como mensaje sin archivo
                    message = self._save_message_to_db(data, sender_number, None, None, company_phone)
                    
                    # Enviar respuesta de error
                    self.whatsapp_service.send_error_response(sender_number, "No se pudo procesar el archivo")
                    
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Mensaje sin archivo (error extrayendo archivo)',
                        'data': {
                            'sender_number': sender_number,
                            'platform': 'whatsapp',
                            'has_file': False,
                            'message_id': message.id if message else None
                        }
                    }, status=200)
                
                # Procesar el archivo: descargar y subir a Drive
                drive_result = self._process_file_to_drive(file_info, sender_number, data)
                
                # Guardar mensaje en la base de datos
                message = self._save_message_to_db(data, sender_number, file_info, drive_result, company_phone)
                
                # Enviar respuesta apropiada según el resultado
                if drive_result.get('error'):
                    # Error procesando archivo
                    self.whatsapp_service.send_error_response(sender_number, drive_result['error'])
                else:
                    # Archivo cargado exitosamente
                    filename = drive_result.get('filename', file_info.get('filename', 'archivo'))
                    company_name = drive_result.get('company_name')
                    self.whatsapp_service.send_file_uploaded_response(sender_number, filename, company_name, message.drive_shared_link)
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Archivo recibido y procesado',
                    'data': {
                        'sender_number': sender_number,
                        'platform': 'whatsapp',
                        'has_file': True,
                        'file_info': file_info,
                        'drive_info': drive_result,
                        'message_id': message.id if message else None
                    }
                }, status=200)
            else:
                # Guardar mensaje sin archivo en la base de datos
                message = self._save_message_to_db(data, sender_number, None, None, company_phone)
                
                # Enviar respuesta indicando que debe cargar archivo
                self.whatsapp_service.send_no_file_response(sender_number)
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Mensaje sin archivo',
                    'data': {
                        'sender_number': sender_number,
                        'platform': 'whatsapp',
                        'has_file': False,
                        'message_id': message.id if message else None
                    }
                }, status=200)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error procesando mensaje de WhatsApp: {str(e)}'
            }, status=500)
    
    def validate_message(self, data: Dict[str, Any]) -> bool:
        """
        Valida si el mensaje de Twilio contiene un archivo.
        
        Args:
            data: Datos del mensaje de Twilio
            
        Returns:
            bool: True si contiene archivo multimedia
        """
        # Twilio envía diferentes campos según el tipo de mensaje
        media_url = data.get('MediaUrl0')  # Primera imagen/video
        media_content_type = data.get('MediaContentType0')
        
        # Verificar si hay archivos multimedia
        if media_url and media_content_type:
            return True
        
        # Verificar si es un documento
        message_type = data.get('MessageType', '')
        if message_type in ['document', 'image', 'video', 'audio']:
            return True
        
        return False
    
    def extract_file_info(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extrae información del archivo del mensaje de Twilio.
        
        Args:
            data: Datos del mensaje de Twilio
            
        Returns:
            Dict con información del archivo o None
        """
        try:
            media_url = data.get('MediaUrl0')
            media_content_type = data.get('MediaContentType0')
            
            if not media_url or not media_content_type:
                return None
            
            # Determinar tipo de archivo basado en content type
            file_type = self._get_file_type_from_content_type(media_content_type)
            
            # Obtener nombre del archivo si está disponible
            filename = data.get('MediaFileName0', f'file_{media_url.split("/")[-1]}')
            
            return {
                'url': media_url,
                'content_type': media_content_type,
                'filename': filename,
                'file_type': file_type,
                'message_id': data.get('MessageSid', ''),
                'timestamp': data.get('Timestamp', ''),
                'sender_number': data.get('From', '').replace('whatsapp:', ''),
            }
            
        except Exception as e:
            print(f"Error extrayendo información del archivo: {e}")
            return None
    
    def _get_file_type_from_content_type(self, content_type: str) -> str:
        """
        Determina el tipo de archivo basado en el content type.
        
        Args:
            content_type: Content type del archivo
            
        Returns:
            str: Tipo de archivo (image, video, document, audio, other)
        """
        content_type_lower = content_type.lower()
        
        if content_type_lower.startswith('image/'):
            return 'image'
        elif content_type_lower.startswith('video/'):
            return 'video'
        elif content_type_lower.startswith('audio/'):
            return 'audio'
        elif content_type_lower in ['application/pdf', 'application/msword', 
                                   'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            return 'document'
        else:
            return 'other'
    
    def download_file(self, media_url: str, auth_sid: str, auth_token: str) -> Optional[bytes]:
        """
        Descarga el archivo desde Twilio.
        
        Args:
            media_url: URL del archivo en Twilio
            auth_sid: Account SID de Twilio
            auth_token: Auth Token de Twilio
            
        Returns:
            bytes: Contenido del archivo o None si hay error
        """
        try:
            response = requests.get(media_url, auth=(auth_sid, auth_token))
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"Error descargando archivo desde Twilio: {e}")
            return None
    
    def _process_file_to_drive(self, file_info: Dict[str, Any], sender_number: str, payload: dict = None) -> Dict[str, Any]:
        """
        Procesa un archivo descargándolo y subiéndolo a Google Drive.
        
        Args:
            file_info: Información del archivo
            sender_number: Número del remitente
            payload: Payload original del webhook
            
        Returns:
            Dict con información del archivo en Drive
        """
        try:
            # Obtener credenciales de Twilio desde la fuente
            if not self.source:
                raise Exception("Source no disponible para obtener credenciales")
            
            credentials = self.source.get_credentials()
            auth_sid = credentials.get('additional1')  # Account SID
            auth_token = credentials.get('additional2')  # Auth Token
            
            if not auth_sid or not auth_token:
                raise Exception("Credenciales de Twilio no configuradas en el Source")
            
            # Descargar archivo desde Twilio
            file_content = self.download_file(
                file_info['url'], 
                auth_sid, 
                auth_token
            )
            
            if not file_content:
                raise Exception("No se pudo descargar el archivo desde Twilio")
            
            # Subir a Google Drive
            drive_service = DriveService()
            drive_result = drive_service.upload_file_from_message(
                file_content=file_content,
                filename=file_info['filename'],
                sender_number=sender_number,
                file_type=file_info['file_type'],
                mime_type=file_info['content_type'],
                company_phone=self._extract_company_phone_from_payload(payload) if payload else None
            )
            
            return drive_result
            
        except Exception as e:
            print(f"Error procesando archivo a Drive: {e}")
            return {'error': str(e)}
    
    def _extract_company_phone_from_payload(self, payload: dict) -> str:
        """
        Extrae el número de teléfono de la compañía del payload.
        
        Args:
            payload: Payload del webhook
            
        Returns:
            Número de teléfono de la compañía
        """
        return payload.get('From', '').replace('whatsapp:', '') if payload else ''
    
    def _save_message_to_db(self, payload: dict, sender_number: str, file_info: dict = None, drive_result: dict = None, company_phone: str = None):
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
            message_text = payload.get('Body', '')
            message_id = payload.get('MessageSid', '')
            
            # Preparar datos del mensaje
            message_data = {
                'source': self.source,
                'sender_number': sender_number,
                'message_id': message_id,
                'message_text': message_text,
            }
            
            # Agregar información del archivo si existe
            if file_info:
                message_data.update({
                    'filename': file_info.get('filename', ''),
                    'file_type': file_info.get('file_type', ''),
                    'file_size': file_info.get('file_size', 0),
                    'content_type': file_info.get('content_type', ''),
                })
            
            # Agregar información de Drive si existe
            if drive_result and 'drive_file_id' in drive_result:
                message_data.update({
                    'drive_file_id': drive_result['drive_file_id'],
                    'drive_shared_link': drive_result['drive_shared_link'],
                    'drive_folder_path': drive_result['drive_folder_path'],
                })
            
            # Usar el service para crear el mensaje con información de compañía
            message = self.message_service.create_message(message_data, company_phone)
            
            if message:
                print(f"✅ Mensaje guardado en BD: ID {message.id}, Sender: {sender_number}")
            
            return message
            
        except Exception as e:
            print(f"Error guardando mensaje en BD: {e}")
            return None
    
