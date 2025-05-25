from django.apps import AppConfig
from django.db import connection


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        import products.signals
        try:
            with connection.cursor() as cursor:
                cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
                cursor.execute("CREATE EXTENSION IF NOT EXISTS unaccent")
        except Exception as e:
            # Log the error but don't fail app initialization
            # This allows tests to run even if DB connection isn't ready yet
            print(f"Warning: Could not create PostgreSQL extensions: {e}")
            # In production, these extensions should be created manually or via migrations
