from typing import Optional, List
from django.db.models import QuerySet
from .models import Source


class SourceSelector:
    """
    Selector para operaciones de consulta de Source.
    Single Responsibility: Solo maneja consultas a la base de datos para Source
    """
    
    @staticmethod
    def get_source_by_name(name: str) -> Optional[Source]:
        """
        Obtiene una fuente por nombre.
        
        Args:
            name: Nombre de la fuente
            
        Returns:
            Optional[Source]: Fuente si existe, None si no
        """
        try:
            return Source.objects.get(name=name, is_active=True)
        except Source.DoesNotExist:
            return None
    
    @staticmethod
    def get_source_by_api_key(api_key: str) -> Optional[Source]:
        """
        Obtiene una fuente por API key.
        
        Args:
            api_key: API key de la fuente
            
        Returns:
            Optional[Source]: Fuente si existe, None si no
        """
        try:
            return Source.objects.get(api_key=api_key, is_active=True)
        except Source.DoesNotExist:
            return None
    
    @staticmethod
    def get_source_by_id(source_id: int) -> Optional[Source]:
        """
        Obtiene una fuente por ID.
        
        Args:
            source_id: ID de la fuente
            
        Returns:
            Optional[Source]: Fuente si existe, None si no
        """
        try:
            return Source.objects.get(id=source_id, is_active=True)
        except Source.DoesNotExist:
            return None
    
    @staticmethod
    def get_active_sources() -> QuerySet[Source]:
        """
        Obtiene todas las fuentes activas.
        
        Returns:
            QuerySet[Source]: Fuentes activas
        """
        return Source.objects.filter(is_active=True)
    
    @staticmethod
    def get_sources_by_names(names: List[str]) -> QuerySet[Source]:
        """
        Obtiene múltiples fuentes por nombres.
        
        Args:
            names: Lista de nombres de fuentes
            
        Returns:
            QuerySet[Source]: Fuentes encontradas
        """
        return Source.objects.filter(name__in=names, is_active=True)
