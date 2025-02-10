from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        n = int(input('Введите число '))
        count = 0
        result = ''
        while True:
            count += 1
            result += str(count) * count
            if len(result) >= n:
                break

        print(result[:n])