from django.core.management.base import BaseCommand
from apps.sources.models import Source


class Command(BaseCommand):
    """
    Comando para cargar sources iniciales.
    Single Responsibility: Solo carga datos iniciales de sources
    """
    help = 'Carga sources iniciales (Twilio, Telegram) en la base de datos'

    def handle(self, *args, **options):
        """
        Ejecuta el comando para cargar sources
        """
        sources_data = [
            {
                'name': 'whatsapp',
                'api_key': 'twilio-whatsapp-key-123',
                'is_active': True,
                'webhook_url': 'https://your-domain.com/api/webhook/',
                'additional1': 'TWILIO_ACCOUNT_SID_PLACEHOLDER',  # Twilio Account SID
                'additional2': 'your-twilio-auth-token',  # Twilio Auth Token
                'additional3': '+1234567890',  # Twilio Phone Number
                'additional4': 'https://api.twilio.com/2010-04-01',  # Twilio API Base URL
                'additional5': '{"webhook_events": ["message", "media"]}',  # Configuración adicional
            },
            {
                'name': 'telegram',
                'api_key': 'telegram-bot-key-456',
                'is_active': True,
                'webhook_url': 'https://your-domain.com/api/webhook/',
                'additional1': '1234567890:ABCdefGHIjklMNOpqrsTUVwxyz',  # Telegram Bot Token
                'additional2': '-1001234567890',  # Telegram Chat ID
                'additional3': 'https://api.telegram.org/bot',  # Telegram API Base URL
                'additional4': 'your-telegram-webhook-secret',  # Webhook Secret
                'additional5': '{"allowed_updates": ["message", "channel_post"]}',  # Configuración adicional
            },
        ]

        created_count = 0
        updated_count = 0

        for source_data in sources_data:
            source, created = Source.objects.get_or_create(
                name=source_data['name'],
                defaults={
                    'api_key': source_data['api_key'],
                    'is_active': source_data['is_active'],
                    'webhook_url': source_data['webhook_url'],
                    'additional1': source_data['additional1'],
                    'additional2': source_data['additional2'],
                    'additional3': source_data['additional3'],
                    'additional4': source_data['additional4'],
                    'additional5': source_data['additional5'],
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Source creada: {source.get_name_display()}')
                )
                self.stdout.write(f'  API Key: {source.api_key}')
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'⚠ Source ya existe: {source.get_name_display()}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Resumen: {created_count} creadas, {updated_count} ya existían'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                '\n🔑 Recuerda actualizar las credenciales reales en el admin de Django'
            )
        )
