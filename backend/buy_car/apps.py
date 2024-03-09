from django.apps import AppConfig


class BuyCarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'buy_car'
    
    def ready(self) -> None:
        import buy_car.signals.handlers
