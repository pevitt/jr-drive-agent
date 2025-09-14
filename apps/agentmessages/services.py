from typing import Optional, Dict, Any
from .models import Message
from .selectors import MessageSelector
from apps.sources.models import Source
from apps.users.services import UserService


class MessageService:
    """
    Servicio para operaciones de negocio de Message.
    Single Responsibility: Solo maneja lógica de negocio para Message
    """
    
    def __init__(self):
        self.selector = MessageSelector()
        self.user_service = UserService()
    
    def create_message(self, data: Dict[str, Any], company_phone: str = None) -> Optional[Message]:
        """
        Crea un nuevo mensaje.
        
        Args:
            data: Datos del mensaje
            
        Returns:
            Optional[Message]: Mensaje creado o None si hay error
        """
        if not self.validate_message_data(data):
            return None
        
        try:
            # Obtener usuario y compañía
            user, company = self.user_service.get_user_and_company_by_phone(
                data['sender_number'], company_phone
            )
            
            # Crear el mensaje
            message = Message.objects.create(
                source=data['source'],
                sender_number=data['sender_number'],
                message_id=data.get('message_id', ''),
                message_text=data.get('message_text', ''),
                user=user,
                company=company,
                filename=data.get('filename', ''),
                file_type=data.get('file_type', ''),
                file_size=data.get('file_size'),
                content_type=data.get('content_type', ''),
                drive_file_id=data.get('drive_file_id', ''),
                drive_shared_link=data.get('drive_shared_link', ''),
                drive_folder_path=data.get('drive_folder_path', ''),
            )
            return message
        except Exception as e:
            print(f"Error creando mensaje: {e}")
            return None
    
    def validate_message_data(self, data: Dict[str, Any]) -> bool:
        """
        Valida los datos de un mensaje.
        
        Args:
            data: Datos del mensaje
            
        Returns:
            bool: True si los datos son válidos
        """
        required_fields = ['source', 'sender_number']
        
        for field in required_fields:
            if not data.get(field):
                return False
        
        return True
    
    def get_message_summary(self, company_id: int, date_from=None, date_to=None) -> Dict[str, Any]:
        """
        Obtiene un resumen de mensajes para una compañía.
        
        Args:
            company_id: ID de la compañía
            date_from: Fecha desde (opcional)
            date_to: Fecha hasta (opcional)
            
        Returns:
            Dict[str, Any]: Resumen de mensajes
        """
        if date_from and date_to:
            messages = self.selector.get_messages_by_date_range(
                date_from, date_to, company_id
            )
        else:
            messages = self.selector.get_messages_by_company(company_id)
        
        # Contar por tipo de archivo
        files_by_type = {}
        total_files = 0
        
        for message in messages:
            if message.file_type:
                files_by_type[message.file_type] = files_by_type.get(message.file_type, 0) + 1
                total_files += 1
        
        # Contar por remitente
        files_by_sender = {}
        for message in messages:
            if message.file_type:
                sender = message.sender_number
                files_by_sender[sender] = files_by_sender.get(sender, 0) + 1
        
        return {
            'total_messages': messages.count(),
            'total_files': total_files,
            'files_by_type': files_by_type,
            'files_by_sender': files_by_sender,
        }
    
    def get_message_info(self, message_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene información detallada de un mensaje.
        
        Args:
            message_id: ID del mensaje
            
        Returns:
            Optional[Dict[str, Any]]: Información del mensaje
        """
        message = self.selector.get_message_by_id(message_id)
        
        if not message:
            return None
        
        return {
            'id': message.id,
            'source_name': message.source.name,
            'sender_number': message.sender_number,
            'message_text': message.message_text,
            'filename': message.filename,
            'file_type': message.file_type,
            'file_size': message.file_size,
            'drive_shared_link': message.drive_shared_link,
            'company_name': message.company.name if message.company else None,
            'created_at': message.created_at,
        }
