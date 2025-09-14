from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    """
    Comando para cargar todos los datos iniciales.
    Single Responsibility: Solo ejecuta otros comandos de carga de datos
    """
    help = 'Carga todos los datos iniciales (companies y sources)'

    def handle(self, *args, **options):
        """
        Ejecuta todos los comandos de carga de datos
        """
        self.stdout.write(
            self.style.SUCCESS('🚀 Iniciando carga de datos iniciales...\n')
        )

        # Cargar companies
        self.stdout.write(
            self.style.HTTP_INFO('📁 Cargando companies...')
        )
        call_command('load_companies')
        
        # Cargar sources
        self.stdout.write(
            self.style.HTTP_INFO('\n📡 Cargando sources...')
        )
        call_command('load_sources')

        self.stdout.write(
            self.style.SUCCESS('\n✅ Carga de datos iniciales completada!')
        )
        self.stdout.write(
            self.style.WARNING(
                '\n📝 Próximos pasos:'
            )
        )
        self.stdout.write('  1. Actualizar credenciales reales en el admin')
        self.stdout.write('  2. Probar el webhook con las API keys generadas')
        self.stdout.write('  3. Configurar Google Drive integration')
