from typing import Optional, Dict, Any, Tuple
from .models import User
from .selectors import UserSelector
from apps.companies.services import CompanyService
from apps.companies.models import Company


class UserService:
    """
    Servicio para operaciones de negocio de User.
    Single Responsibility: Solo maneja lógica de negocio para User
    """
    
    def __init__(self):
        self.selector = UserSelector()
        self.company_service = CompanyService()
    
    def get_user_and_company_by_phone(self, sender_phone: str, company_phone: str = None) -> Tuple[Optional[User], Optional[Company]]:
        """
        Obtiene usuario y compañía por números de teléfono.
        
        Args:
            sender_phone: Número de teléfono del remitente
            company_phone: Número de teléfono de la compañía (opcional)
            
        Returns:
            Tuple[Optional[User], Optional[Company]]: (Usuario, Compañía)
        """
        # Buscar usuario existente
        user = self.selector.get_user_by_phone_number(sender_phone)
        
        # Buscar compañía por número de teléfono de la compañía
        if company_phone:
            company = self.company_service.get_company_by_phone_number(company_phone)
            if company:
                return user, company
        
        # Si hay usuario y tiene compañía asignada
        if user and user.company:
            return user, user.company
        
        # Si no hay usuario o compañía, obtener compañía por defecto
        company = self.company_service.get_or_create_default_company()
        
        return None, company
    
    def create_user(self, data: Dict[str, Any]) -> Optional[User]:
        """
        Crea un nuevo usuario.
        
        Args:
            data: Datos del usuario
            
        Returns:
            Optional[User]: Usuario creado o None si hay error
        """
        if not self.validate_user_data(data):
            return None
        
        try:
            # Obtener o crear compañía
            company = self.company_service.get_or_create_default_company()
            
            user = User.objects.create(
                phone_number=data['phone_number'],
                company=company,
                is_active=data.get('is_active', True)
            )
            return user
        except Exception as e:
            print(f"Error creando usuario: {e}")
            return None
    
    def validate_user_data(self, data: Dict[str, Any]) -> bool:
        """
        Valida los datos de un usuario.
        
        Args:
            data: Datos del usuario
            
        Returns:
            bool: True si los datos son válidos
        """
        required_fields = ['phone_number']
        
        for field in required_fields:
            if not data.get(field):
                return False
        
        return True
    
    def get_user_info(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene información de un usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Optional[Dict[str, Any]]: Información del usuario
        """
        user = self.selector.get_user_by_id(user_id)
        
        if not user:
            return None
        
        return {
            'id': user.id,
            'phone_number': user.phone_number,
            'company_id': user.company.id if user.company else None,
            'company_name': user.company.name if user.company else None,
            'is_active': user.is_active,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }
