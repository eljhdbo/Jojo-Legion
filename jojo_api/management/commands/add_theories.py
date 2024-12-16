from django.core.management.base import BaseCommand
from jojo_api.theory_data import add_initial_theories  # Import modifié

class Command(BaseCommand):
    help = 'Ajoute les théories initiales dans la base de données'

    def handle(self, *args, **kwargs):
        self.stdout.write('Ajout des théories...')
        add_initial_theories()
        self.stdout.write(self.style.SUCCESS('Théories ajoutées avec succès !'))