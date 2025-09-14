from typing import Dict, Any
from django.http import JsonResponse
from apps.sources.models import Source
from utils.strategies.factory import StrategyFactory
from utils.strategies.base import MessageStrategy
from apps.sources.services import SourceService


class MessageService:
    """
    Servicio principal para el procesamiento de mensajes.
    Single Responsibility: Coordina el procesamiento de mensajes
    Dependency Inversion: Depende de abstracciones (Strategy)
    """
    
    def __init__(self):
        self.strategy_factory = StrategyFactory()
        self.source_service = SourceService()
    
    def process_webhook_message(self, source: Source, data: Dict[str, Any]) -> JsonResponse:
        """
        Procesa un mensaje entrante desde un webhook.
        
        Args:
            source: Fuente del mensaje (Source model)
            data: Datos del webhook
            
        Returns:
            JsonResponse: Respuesta del procesamiento
        """
        try:
            # Crear estrategia basada en el tipo de fuente
            strategy = self.strategy_factory.create_strategy(source.name, source)
            
            # Procesar el mensaje usando la estrategia
            response = strategy.process_message(data)
            
            # TODO: Aquí se puede agregar lógica adicional como:
            # - Logging del mensaje
            # - Guardado en base de datos
            # - Notificaciones
            # - Métricas
            
            return response
            
        except ValueError as e:
            # Plataforma no soportada
            return JsonResponse({
                'status': 'error',
                'message': f'Plataforma no soportada: {source.name}'
            }, status=400)
            
        except Exception as e:
            # Error general
            return JsonResponse({
                'status': 'error',
                'message': f'Error procesando mensaje: {str(e)}'
            }, status=500)
    
    def get_supported_platforms(self) -> list:
        """
        Retorna las plataformas soportadas.
        
        Returns:
            list: Lista de plataformas soportadas
        """
        return self.strategy_factory.get_supported_platforms()
    
    def validate_source(self, source: Source) -> bool:
        """
        Valida que la fuente esté configurada correctamente.
        
        Args:
            source: Fuente a validar
            
        Returns:
            bool: True si la fuente es válida
        """
        try:
            # Usar el SourceService para validar la fuente
            return self.source_service.validate_source(source)
            
        except Exception:
            return False
