from typing import Optional, Dict, Any
from .models import Company
from .selectors import CompanySelector


class CompanyService:
    """
    Servicio para operaciones de negocio de Company.
    Single Responsibility: Solo maneja lógica de negocio para Company
    """
    
    def __init__(self):
        self.selector = CompanySelector()
    
    def get_or_create_default_company(self) -> Company:
        """
        Obtiene o crea la compañía por defecto.
        
        Returns:
            Company: Compañía por defecto
        """
        # Intentar obtener una compañía existente
        company = self.selector.get_default_company()
        
        if not company:
            # Crear compañía por defecto si no existe
            company = Company.objects.create(
                name='Default Company',
                description='Compañía por defecto para usuarios sin asignar',
                is_active=True
            )
        
        return company
    
    def get_company_by_phone_number(self, phone_number: str) -> Optional[Company]:
        """
        Obtiene una compañía por número de teléfono.
        
        Args:
            phone_number: Número de teléfono de la compañía
            
        Returns:
            Optional[Company]: Compañía si existe, None si no
        """
        return self.selector.get_company_by_phone_number(phone_number)
    
    def get_company_for_user(self, phone_number: str) -> Company:
        """
        Obtiene la compañía apropiada para un usuario.
        
        Args:
            phone_number: Número de teléfono del usuario
            
        Returns:
            Company: Compañía del usuario o por defecto
        """
        # Por ahora retornamos la compañía por defecto
        # En el futuro se podría implementar lógica para asignar compañías específicas
        return self.get_or_create_default_company()
    
    def validate_company_data(self, data: Dict[str, Any]) -> bool:
        """
        Valida los datos de una compañía.
        
        Args:
            data: Datos de la compañía
            
        Returns:
            bool: True si los datos son válidos
        """
        required_fields = ['name']
        
        for field in required_fields:
            if not data.get(field):
                return False
        
        return True
    
    def create_company(self, data: Dict[str, Any]) -> Optional[Company]:
        """
        Crea una nueva compañía.
        
        Args:
            data: Datos de la compañía
            
        Returns:
            Optional[Company]: Compañía creada o None si hay error
        """
        if not self.validate_company_data(data):
            return None
        
        try:
            company = Company.objects.create(
                name=data['name'],
                description=data.get('description', ''),
                is_active=data.get('is_active', True)
            )
            return company
        except Exception as e:
            print(f"Error creando compañía: {e}")
            return None
    
    def get_company_info(self, company_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene información de una compañía.
        
        Args:
            company_id: ID de la compañía
            
        Returns:
            Optional[Dict[str, Any]]: Información de la compañía
        """
        company = self.selector.get_company_by_id(company_id)
        
        if not company:
            return None
        
        return {
            'id': company.id,
            'name': company.name,
            'description': company.description,
            'is_active': company.is_active,
            'created_at': company.created_at,
            'updated_at': company.updated_at
        }
