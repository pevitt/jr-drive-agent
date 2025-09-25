from django.core.management.base import BaseCommand
from apps.companies.models import Company


class Command(BaseCommand):
    """
    Comando para cargar companies iniciales.
    Single Responsibility: Solo carga datos iniciales de companies
    """
    help = 'Carga companies iniciales en la base de datos'

    def handle(self, *args, **options):
        """
        Ejecuta el comando para cargar companies
        """
        companies_data = [
            {
                'name': 'Rigoberto',
                'phone_number': '+5712312312',
                'drive_folder_id': '1XqhwTc_anck6Rt_J9N6AZ2HaXWoEGLKe',  # Tu carpeta de Drive
                'is_active': True,
            },
            {
                'name': 'Empresa Demo',
                'phone_number': '+1987654321',
                'drive_folder_id': '',  # Agregar ID cuando crees la carpeta
                'is_active': True,
            },
            {
                'name': 'Cliente Test',
                'phone_number': '+1555000000',
                'drive_folder_id': '',  # Agregar ID cuando crees la carpeta
                'is_active': True,
            },
        ]

        created_count = 0
        updated_count = 0

        for company_data in companies_data:
            company, created = Company.objects.get_or_create(
                name=company_data['name'],
                defaults={
                    'phone_number': company_data['phone_number'],
                    'drive_folder_id': company_data['drive_folder_id'],
                    'is_active': company_data['is_active'],
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Company creada: {company.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'⚠ Company ya existe: {company.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Resumen: {created_count} creadas, {updated_count} ya existían'
            )
        )
