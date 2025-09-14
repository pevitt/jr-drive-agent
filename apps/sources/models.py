from django.db import models
from utils.models.model import BaseModel

class Source(BaseModel):
    """
    Modelo para representar fuentes de mensajería.
    Single Responsibility: Solo maneja fuentes de mensajería
    """
    SOURCE_TYPES = [
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
        ('discord', 'Discord'),
    ]
    
    # Campos básicos
    name = models.CharField(
        max_length=50, 
        choices=SOURCE_TYPES, 
        unique=True,
        help_text="Tipo de fuente de mensajería"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indica si la fuente está activa"
    )
    api_key = models.CharField(
        max_length=255, 
        unique=True,
        help_text="API Key para autenticación"
    )
    webhook_url = models.URLField(
        blank=True, 
        null=True,
        help_text="URL del webhook para recibir mensajes"
    )
    
    # Campos adicionales para credenciales y configuraciones
    additional1 = models.TextField(
        blank=True, 
        null=True,
        help_text="Campo adicional 1 - Ej: Twilio Account SID, Telegram Bot Token"
    )
    additional2 = models.TextField(
        blank=True, 
        null=True,
        help_text="Campo adicional 2 - Ej: Twilio Auth Token, Telegram Chat ID"
    )
    additional3 = models.TextField(
        blank=True, 
        null=True,
        help_text="Campo adicional 3 - Ej: Twilio Phone Number, Telegram Webhook URL"
    )
    additional4 = models.TextField(
        blank=True, 
        null=True,
        help_text="Campo adicional 4 - Ej: Configuraciones adicionales, tokens de acceso"
    )
    additional5 = models.TextField(
        blank=True, 
        null=True,
        help_text="Campo adicional 5 - Ej: Configuraciones específicas de la integración"
    )
    
    # Timestamps
    
    class Meta:
        db_table = 'sources'
        verbose_name = 'Source'
        verbose_name_plural = 'Sources'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.get_name_display()} - {self.api_key[:8]}..."
    
    def get_credentials(self) -> dict:
        """
        Retorna las credenciales específicas de la fuente
        """
        credentials = {}
        if self.additional1:
            credentials['additional1'] = self.additional1
        if self.additional2:
            credentials['additional2'] = self.additional2
        if self.additional3:
            credentials['additional3'] = self.additional3
        if self.additional4:
            credentials['additional4'] = self.additional4
        if self.additional5:
            credentials['additional5'] = self.additional5
        return credentials
    
    def set_credentials(self, **kwargs):
        """
        Establece las credenciales de la fuente
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
