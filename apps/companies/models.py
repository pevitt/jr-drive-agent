from django.db import models
from utils.models.model import BaseModel


class Company(BaseModel):
    """
    Modelo para representar compañías.
    Single Responsibility: Solo maneja información de compañías
    """
    name = models.CharField(
        max_length=255, 
        unique=True,
        help_text="Nombre de la compañía"
    )
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        help_text="Número de teléfono identificador de la compañía"
    )
    drive_folder_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="ID de la carpeta compartida en Google Drive"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indica si la compañía está activa"
    )
    
    class Meta:
        db_table = 'companies'
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['name']
    
    def __str__(self):
        return self.name
