from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from apps.sources.models import Source


class SourceWrapper:
    """
    Wrapper para el objeto Source que agrega compatibilidad con DRF.
    Single Responsibility: Solo agrega métodos necesarios para DRF
    """
    
    def __init__(self, source):
        self.source = source
        self.is_authenticated = True
    
    def __getattr__(self, name):
        """Delega atributos al objeto Source subyacente"""
        return getattr(self.source, name)
    
    def __str__(self):
        return str(self.source)


class APIKeyAuthentication(BaseAuthentication):
    """
    Autenticación por API Key para fuentes.
    Single Responsibility: Solo maneja autenticación por API Key
    """
    
    def authenticate(self, request):
        """
        Autentica usando API Key del header X-API-Key
        """
        api_key = request.META.get('HTTP_X_API_KEY')
        
        if not api_key:
            return None
        
        try:
            source = Source.objects.get(api_key=api_key, is_active=True)
            # Envolvemos el Source en un wrapper compatible con DRF
            wrapped_source = SourceWrapper(source)
            return (wrapped_source, None)  # (user, auth)
        except Source.DoesNotExist:
            raise AuthenticationFailed('Invalid API Key')
    
    def authenticate_header(self, request):
        """
        Retorna el header de autenticación requerido
        """
        return 'X-API-Key'
