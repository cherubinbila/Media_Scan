from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    def ready(self):
        """Appelé au démarrage de l'application"""
        # Démarrer le scheduler pour l'automatisation du scraping
        # Uniquement si ce n'est pas un processus de migration ou de test
        import sys
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv[0]:
            from .scheduler import start_scheduler
            start_scheduler()
