from typing import Optional, List
from django.db.models import QuerySet
from .models import User


class UserSelector:
    """
    Selector para operaciones de consulta de User.
    Single Responsibility: Solo maneja consultas a la base de datos para User
    """
    
    @staticmethod
    def get_user_by_phone_number(phone_number: str) -> Optional[User]:
        """
        Obtiene un usuario por número de teléfono.
        
        Args:
            phone_number: Número de teléfono del usuario
            
        Returns:
            Optional[User]: Usuario si existe, None si no
        """
        try:
            return User.objects.get(phone_number=phone_number, is_active=True)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """
        Obtiene un usuario por ID.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Optional[User]: Usuario si existe, None si no
        """
        try:
            return User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_users_by_company(company_id: int) -> QuerySet[User]:
        """
        Obtiene todos los usuarios de una compañía.
        
        Args:
            company_id: ID de la compañía
            
        Returns:
            QuerySet[User]: Usuarios de la compañía
        """
        return User.objects.filter(company_id=company_id, is_active=True)
    
    @staticmethod
    def get_users_by_phone_numbers(phone_numbers: List[str]) -> QuerySet[User]:
        """
        Obtiene múltiples usuarios por números de teléfono.
        
        Args:
            phone_numbers: Lista de números de teléfono
            
        Returns:
            QuerySet[User]: Usuarios encontrados
        """
        return User.objects.filter(phone_number__in=phone_numbers, is_active=True)
    
    @staticmethod
    def get_active_users() -> QuerySet[User]:
        """
        Obtiene todos los usuarios activos.
        
        Returns:
            QuerySet[User]: Usuarios activos
        """
        return User.objects.filter(is_active=True)
