from django.db import models
from utils.models.model import BaseModel


class Message(BaseModel):
    """
    Modelo para representar mensajes capturados.
    Single Responsibility: Solo maneja mensajes capturados
    """
    FILE_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ]
    
    # Relación con Source
    source = models.ForeignKey(
        'sources.Source', 
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="Fuente de donde proviene el mensaje"
    )
    
    # Relación con User y Company
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Usuario que envió el mensaje"
    )
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Compañía del usuario"
    )
    
    # Información del mensaje
    message_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="ID del mensaje en la plataforma"
    )
    message_text = models.TextField(
        blank=True,
        null=True,
        help_text="Texto del mensaje"
    )
    
    # Información del remitente
    sender_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Número de teléfono del remitente"
    )
    
    # Información del archivo (opcional)
    filename = models.CharField(
        max_length=255,
        blank=True,
        help_text="Nombre del archivo"
    )
    file_type = models.CharField(
        max_length=20, 
        choices=FILE_TYPES,
        blank=True,
        help_text="Tipo de archivo"
    )
    file_size = models.BigIntegerField(
        null=True,
        blank=True,
        help_text="Tamaño del archivo en bytes"
    )
    content_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="Tipo MIME del archivo"
    )
    
    # Metadatos de Drive (opcional)
    drive_file_id = models.CharField(
        max_length=255, 
        blank=True,
        help_text="ID del archivo en Google Drive"
    )
    drive_shared_link = models.URLField(
        blank=True,
        help_text="Enlace compartido del archivo en Google Drive"
    )
    drive_folder_path = models.CharField(
        max_length=500,
        blank=True,
        help_text="Ruta de la carpeta en Google Drive"
    )
    
    
    class Meta:
        db_table = 'messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
    
    def __str__(self):
        return f"{self.filename} from {self.sender_number}"
