import autofixture
from .models import TestModel


class CustomTestModelFixture(autofixture.AutoFixture):
    pass


autofixture.register(TestModel, CustomTestModelFixture)
