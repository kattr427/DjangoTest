from django.core.management import BaseCommand
class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Создание продукта")

        self.stdout.write(self.style.SUCCSESS"Продукт создан")

