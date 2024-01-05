from django.core.management.base import BaseCommand

from api.models import Category  # isort:skip

CATEGORIES = (
    "🧀Продукты", "🌭На работе", "🍤Доставка", "🧋Кофе",
    "🚕Такси/Шеринг", "🚇Транспорт", "🏠Дом", "🙈ЖКХ",
    "🎁Подарки", "💵Долги", "👔Одежда", "🏥Здоровье",
    "🙊Животные", "🎲Развлечения", "😎Разное", "⚙️Меню"
)


class Command(BaseCommand):
    help = 'Load categories to db'

    def handle(self, *args, **options):
        for category in CATEGORIES:
            Category.objects.get_or_create(title=category)
        self.stdout.write(
            self.style.SUCCESS('Categories has been loaded succesfully'))
