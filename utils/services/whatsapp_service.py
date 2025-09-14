from typing import Dict, Any, Optional
from django.conf import settings
import requests
from apps.sources.models import Source


class WhatsAppService:
    """
    Servicio para manejar respuestas a WhatsApp usando Twilio.
    Single Responsibility: Solo maneja el envío de mensajes a WhatsApp
    """
    
    def __init__(self, source: Source = None):
        self.source = source
    
    def send_message(self, to_number: str, message: str) -> Dict[str, Any]:
        """
        Envía un mensaje a WhatsApp usando Twilio.
        
        Args:
            to_number: Número de destino (con prefijo internacional)
            message: Mensaje a enviar
            
        Returns:
            Dict con resultado del envío
        """
        try:
            if not self.source:
                raise Exception("Source no disponible para enviar mensaje")
            
            # Obtener credenciales de Twilio
            credentials = self.source.get_credentials()
            account_sid = credentials.get('additional1')  # Account SID
            auth_token = credentials.get('additional2')   # Auth Token
            
            if not account_sid or not auth_token:
                raise Exception("Credenciales de Twilio no configuradas")
            
            # URL de la API de Twilio
            url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
            
            # Limpiar y formatear el número de destino
            clean_number = to_number.strip().replace(' ', '')
            if not clean_number.startswith('+'):
                clean_number = '+' + clean_number
            
            # Datos para enviar
            data = {
                'From': 'whatsapp:+14155238886',  # Número de Twilio WhatsApp Sandbox
                'To': f'whatsapp:{clean_number}',
                'Body': message
            }
            
            # Enviar mensaje
            response = requests.post(
                url,
                data=data,
                auth=(account_sid, auth_token)
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Mensaje enviado a WhatsApp: {clean_number} - {message}")
                return {
                    'success': True,
                    'message_sid': result.get('sid'),
                    'status': result.get('status'),
                    'to': result.get('to'),
                    'from': result.get('from')
                }
            else:
                print(f"❌ Error enviando mensaje a WhatsApp: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            print(f"❌ Error enviando mensaje a WhatsApp: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_file_uploaded_response(self, to_number: str, filename: str, company_name: str = None, drive_shared_link: str = None) -> Dict[str, Any]:
        """
        Envía respuesta cuando se carga un archivo exitosamente.
        
        Args:
            to_number: Número de destino
            filename: Nombre del archivo cargado
            company_name: Nombre de la compañía (opcional)
            
        Returns:
            Dict con resultado del envío
        """
        if company_name:
            message = f"📁 Archivo '{filename}' cargado exitosamente en la carpeta de {company_name}. "
            if drive_shared_link:
                message += f"\n\nEnlace compartido: {drive_shared_link}"
        else:
            message = f"📁 Archivo '{filename}' cargado exitosamente."
        
        return self.send_message(to_number, message)
    
    def send_no_file_response(self, to_number: str) -> Dict[str, Any]:
        """
        Envía respuesta cuando no se carga archivo.
        
        Args:
            to_number: Número de destino
            
        Returns:
            Dict con resultado del envío
        """
        message = "⚠️ Debe cargar archivo. Por favor, envíe un archivo (imagen, documento, video, etc.)"
        return self.send_message(to_number, message)
    
    def send_error_response(self, to_number: str, error_message: str = "Error procesando archivo") -> Dict[str, Any]:
        """
        Envía respuesta cuando hay error procesando archivo.
        
        Args:
            to_number: Número de destino
            error_message: Mensaje de error específico
            
        Returns:
            Dict con resultado del envío
        """
        message = f"❌ {error_message}. Por favor, intente nuevamente."
        return self.send_message(to_number, message)
