from typing import Optional, List
from django.db.models import QuerySet
from .models import Company


class CompanySelector:
    """
    Selector para operaciones de consulta de Company.
    Single Responsibility: Solo maneja consultas a la base de datos para Company
    """
    
    @staticmethod
    def get_active_companies() -> QuerySet[Company]:
        """
        Obtiene todas las compañías activas.
        
        Returns:
            QuerySet[Company]: Compañías activas
        """
        return Company.objects.filter(is_active=True)
    
    @staticmethod
    def get_company_by_id(company_id: int) -> Optional[Company]:
        """
        Obtiene una compañía por ID.
        
        Args:
            company_id: ID de la compañía
            
        Returns:
            Optional[Company]: Compañía si existe, None si no
        """
        try:
            return Company.objects.get(id=company_id, is_active=True)
        except Company.DoesNotExist:
            return None
    
    @staticmethod
    def get_company_by_name(name: str) -> Optional[Company]:
        """
        Obtiene una compañía por nombre.
        
        Args:
            name: Nombre de la compañía
            
        Returns:
            Optional[Company]: Compañía si existe, None si no
        """
        try:
            return Company.objects.get(name=name, is_active=True)
        except Company.DoesNotExist:
            return None
    
    @staticmethod
    def get_company_by_phone_number(phone_number: str) -> Optional[Company]:
        """
        Obtiene una compañía por número de teléfono.
        
        Args:
            phone_number: Número de teléfono de la compañía
            
        Returns:
            Optional[Company]: Compañía si existe, None si no
        """
        try:
            return Company.objects.get(phone_number=phone_number, is_active=True)
        except Company.DoesNotExist:
            return None
    
    @staticmethod
    def get_default_company() -> Optional[Company]:
        """
        Obtiene la primera compañía activa como compañía por defecto.
        
        Returns:
            Optional[Company]: Primera compañía activa
        """
        return Company.objects.filter(is_active=True).first()
    
    @staticmethod
    def get_companies_by_ids(company_ids: List[int]) -> QuerySet[Company]:
        """
        Obtiene múltiples compañías por IDs.
        
        Args:
            company_ids: Lista de IDs de compañías
            
        Returns:
            QuerySet[Company]: Compañías encontradas
        """
        return Company.objects.filter(id__in=company_ids, is_active=True)
