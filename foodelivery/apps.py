from django.apps import AppConfig


class FoodeliveryConfig(AppConfig):
    name = 'foodelivery'

    def ready(self):
    	import foodelivery.signals