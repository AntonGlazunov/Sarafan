from rest_framework.serializers import ValidationError


class QuantityValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if int(dict(value).get(self.field)) < 0:
            raise ValidationError("Значение должно быть больше 0")