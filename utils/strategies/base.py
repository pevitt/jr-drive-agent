from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from django.http import JsonResponse


class MessageStrategy(ABC):
    """
    Estrategia base para el procesamiento de mensajes.
    Strategy Pattern: Permite intercambiar algoritmos de procesamiento
    """
    
    def __init__(self, source=None):
        self.source = source
    
    @abstractmethod
    def process_message(self, data: Dict[str, Any]) -> JsonResponse:
        """
        Procesa un mensaje entrante.
        
        Args:
            data: Datos del mensaje entrante
            
        Returns:
            JsonResponse: Respuesta del procesamiento
        """
        pass
    
    @abstractmethod
    def validate_message(self, data: Dict[str, Any]) -> bool:
        """
        Valida si el mensaje contiene un archivo.
        
        Args:
            data: Datos del mensaje
            
        Returns:
            bool: True si contiene archivo, False en caso contrario
        """
        pass
    
    @abstractmethod
    def extract_file_info(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extrae información del archivo del mensaje.
        
        Args:
            data: Datos del mensaje
            
        Returns:
            Dict con información del archivo o None si no hay archivo
        """
        pass
    
    def create_no_file_response(self, sender_number: str, platform: str) -> JsonResponse:
        """
        Crea respuesta estándar para mensajes sin archivo.
        
        Args:
            sender_number: Número del remitente
            platform: Plataforma (whatsapp, telegram)
            
        Returns:
            JsonResponse: Respuesta estándar
        """
        return JsonResponse({
            'status': 'success',
            'message': 'Mensaje sin archivo',
            'data': {
                'sender_number': sender_number,
                'platform': platform,
                'has_file': False
            }
        }, status=200)
