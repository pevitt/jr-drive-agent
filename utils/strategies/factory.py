from typing import Dict, Type
from utils.strategies.base import MessageStrategy
from utils.strategies.twilio_strategy import TwilioWhatsAppStrategy
from utils.strategies.telegram_strategy import TelegramStrategy


class StrategyFactory:
    """
    Factory para crear estrategias de procesamiento de mensajes.
    Factory Pattern: Centraliza la creación de estrategias
    """
    
    _strategies: Dict[str, Type[MessageStrategy]] = {
        'whatsapp': TwilioWhatsAppStrategy,
        'telegram': TelegramStrategy,
    }
    
    @classmethod
    def create_strategy(cls, platform: str, source=None) -> MessageStrategy:
        """
        Crea una estrategia para la plataforma especificada.
        
        Args:
            platform: Nombre de la plataforma (whatsapp, telegram)
            source: Objeto Source para la estrategia
            
        Returns:
            MessageStrategy: Instancia de la estrategia
            
        Raises:
            ValueError: Si la plataforma no está soportada
        """
        if platform not in cls._strategies:
            raise ValueError(f"Plataforma no soportada: {platform}")
        
        strategy_class = cls._strategies[platform]
        return strategy_class(source)
    
    @classmethod
    def get_supported_platforms(cls) -> list:
        """
        Retorna lista de plataformas soportadas.
        
        Returns:
            list: Lista de plataformas soportadas
        """
        return list(cls._strategies.keys())
