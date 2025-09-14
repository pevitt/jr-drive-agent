from typing import Optional, Dict, Any
from .models import Source
from .selectors import SourceSelector


class SourceService:
    """
    Servicio para operaciones de negocio de Source.
    Single Responsibility: Solo maneja lógica de negocio para Source
    """
    
    def __init__(self):
        self.selector = SourceSelector()
    
    def get_source_by_name(self, name: str) -> Optional[Source]:
        """
        Obtiene una fuente por nombre.
        
        Args:
            name: Nombre de la fuente
            
        Returns:
            Optional[Source]: Fuente si existe, None si no
        """
        return self.selector.get_source_by_name(name)
    
    def get_source_by_api_key(self, api_key: str) -> Optional[Source]:
        """
        Obtiene una fuente por API key.
        
        Args:
            api_key: API key de la fuente
            
        Returns:
            Optional[Source]: Fuente si existe, None si no
        """
        return self.selector.get_source_by_api_key(api_key)
    
    def validate_source(self, source: Source) -> bool:
        """
        Valida que una fuente esté correctamente configurada.
        
        Args:
            source: Fuente a validar
            
        Returns:
            bool: True si la fuente es válida
        """
        if not source or not source.is_active:
            return False
        
        # Validaciones específicas por tipo de fuente
        if source.name == 'whatsapp':
            return self._validate_whatsapp_source(source)
        elif source.name == 'telegram':
            return self._validate_telegram_source(source)
        
        return True
    
    def _validate_whatsapp_source(self, source: Source) -> bool:
        """
        Valida una fuente de WhatsApp.
        
        Args:
            source: Fuente de WhatsApp
            
        Returns:
            bool: True si la fuente es válida
        """
        # Verificar que tenga las credenciales necesarias
        required_fields = ['additional1', 'additional2']  # Account SID, Auth Token
        
        for field in required_fields:
            if not getattr(source, field, None):
                return False
        
        return True
    
    def _validate_telegram_source(self, source: Source) -> bool:
        """
        Valida una fuente de Telegram.
        
        Args:
            source: Fuente de Telegram
            
        Returns:
            bool: True si la fuente es válida
        """
        # Verificar que tenga el token del bot
        if not getattr(source, 'additional1', None):  # Bot Token
            return False
        
        return True
    
    def get_source_credentials(self, source: Source) -> Dict[str, str]:
        """
        Obtiene las credenciales de una fuente.
        
        Args:
            source: Fuente
            
        Returns:
            Dict[str, str]: Credenciales de la fuente
        """
        credentials = {}
        
        if source.name == 'whatsapp':
            credentials = {
                'account_sid': getattr(source, 'additional1', ''),
                'auth_token': getattr(source, 'additional2', ''),
                'webhook_url': getattr(source, 'additional3', ''),
            }
        elif source.name == 'telegram':
            credentials = {
                'bot_token': getattr(source, 'additional1', ''),
                'webhook_url': getattr(source, 'additional2', ''),
            }
        
        return credentials
