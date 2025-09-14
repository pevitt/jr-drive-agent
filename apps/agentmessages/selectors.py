from typing import Optional, List
from django.db.models import QuerySet
from datetime import datetime
from .models import Message


class MessageSelector:
    """
    Selector para operaciones de consulta de Message.
    Single Responsibility: Solo maneja consultas a la base de datos para Message
    """
    
    @staticmethod
    def get_message_by_id(message_id: int) -> Optional[Message]:
        """
        Obtiene un mensaje por ID.
        
        Args:
            message_id: ID del mensaje
            
        Returns:
            Optional[Message]: Mensaje si existe, None si no
        """
        try:
            return Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            return None
    
    @staticmethod
    def get_message_by_platform_id(platform_message_id: str, source_id: int) -> Optional[Message]:
        """
        Obtiene un mensaje por ID de la plataforma y fuente.
        
        Args:
            platform_message_id: ID del mensaje en la plataforma
            source_id: ID de la fuente
            
        Returns:
            Optional[Message]: Mensaje si existe, None si no
        """
        try:
            return Message.objects.get(message_id=platform_message_id, source_id=source_id)
        except Message.DoesNotExist:
            return None
    
    @staticmethod
    def get_messages_by_sender(sender_number: str) -> QuerySet[Message]:
        """
        Obtiene todos los mensajes de un remitente.
        
        Args:
            sender_number: Número del remitente
            
        Returns:
            QuerySet[Message]: Mensajes del remitente
        """
        return Message.objects.filter(sender_number=sender_number).order_by('-created_at')
    
    @staticmethod
    def get_messages_by_company(company_id: int) -> QuerySet[Message]:
        """
        Obtiene todos los mensajes de una compañía.
        
        Args:
            company_id: ID de la compañía
            
        Returns:
            QuerySet[Message]: Mensajes de la compañía
        """
        return Message.objects.filter(company_id=company_id).order_by('-created_at')
    
    @staticmethod
    def get_messages_by_source(source_id: int) -> QuerySet[Message]:
        """
        Obtiene todos los mensajes de una fuente.
        
        Args:
            source_id: ID de la fuente
            
        Returns:
            QuerySet[Message]: Mensajes de la fuente
        """
        return Message.objects.filter(source_id=source_id).order_by('-created_at')
    
    @staticmethod
    def get_messages_with_files() -> QuerySet[Message]:
        """
        Obtiene todos los mensajes que contienen archivos.
        
        Returns:
            QuerySet[Message]: Mensajes con archivos
        """
        return Message.objects.exclude(filename='').order_by('-created_at')
    
    @staticmethod
    def get_messages_by_date_range(
        date_from: datetime, 
        date_to: datetime, 
        company_id: Optional[int] = None
    ) -> QuerySet[Message]:
        """
        Obtiene mensajes en un rango de fechas.
        
        Args:
            date_from: Fecha desde
            date_to: Fecha hasta
            company_id: ID de la compañía (opcional)
            
        Returns:
            QuerySet[Message]: Mensajes en el rango de fechas
        """
        queryset = Message.objects.filter(
            created_at__gte=date_from,
            created_at__lte=date_to
        ).order_by('-created_at')
        
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        
        return queryset
    
    @staticmethod
    def get_messages_by_file_type(file_type: str) -> QuerySet[Message]:
        """
        Obtiene mensajes por tipo de archivo.
        
        Args:
            file_type: Tipo de archivo
            
        Returns:
            QuerySet[Message]: Mensajes del tipo de archivo
        """
        return Message.objects.filter(file_type=file_type).order_by('-created_at')
