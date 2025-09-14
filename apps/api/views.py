from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from apps.sources.models import Source
from utils.services.message_service import MessageService


class AgentWebhookView(APIView):
    """
    Vista principal para recibir webhooks de fuentes.
    Single Responsibility: Solo maneja requests HTTP de webhooks
    """
    permission_classes = [AllowAny]  # No requerimos autenticación, usamos source_type del path
    authentication_classes = []  # No usar autenticación para webhooks
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message_service = MessageService()
    
    def post(self, request, source_type):
        """
        Procesa archivos recibidos via webhook
        
        Args:
            source_type: Tipo de fuente (whatsapp, telegram) desde la URL
        """
        try:
            # Buscar la fuente por tipo
            try:
                source = Source.objects.get(name=source_type, is_active=True)
            except Source.DoesNotExist:
                return Response({
                    'status': 'error',
                    'message': f'Fuente no encontrada o inactiva: {source_type}'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Validar que la fuente sea válida
            print(f"Source: {source}")
            if not self.message_service.validate_source(source):
                return Response({
                    'status': 'error',
                    'message': 'Fuente no válida o no configurada correctamente'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Procesar el mensaje usando el servicio
            data = request.data
            response = self.message_service.process_webhook_message(source, data)
            
            # Convertir JsonResponse a Response de DRF
            # JsonResponse tiene el contenido en response.content (bytes)
            import json
            response_data = json.loads(response.content)
            return Response(response_data, status=response.status_code)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Error procesando archivo: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HealthCheckView(APIView):
    """
    Vista para health check del sistema.
    Single Responsibility: Solo verifica el estado del sistema
    """
    permission_classes = [AllowAny]  # No requiere autenticación
    authentication_classes = []  # No usar autenticación
    
    def get(self, request):
        """
        Retorna el estado del sistema
        """
        return JsonResponse({
            'status': 'healthy',
            'service': 'Drive Agent API',
            'version': '1.0.0'
        })
