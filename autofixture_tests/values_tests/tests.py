from django.test import TestCase
from autofixture.values import Values


class ValuesTests(TestCase):
    def test_init(self):
        values = Values({'a': 1, 'c': 4}, a=2, b=3)
        self.assertEqual(values['a'], 2)
        self.assertEqual(values['b'], 3)
        self.assertEqual(values['c'], 4)

        values = Values(values)
        self.assertEqual(values['a'], 2)
        self.assertEqual(values['b'], 3)
        self.assertEqual(values['c'], 4)

        class Data:
            a = 1
            b = 3
            _c = 4
        values = Values(Data, a=2)
        self.assertEqual(values['a'], 2)
        self.assertEqual(values['b'], 3)
        self.assertEqual(values['_c'], 4)

        values = Values(Data(), a=2)
        self.assertEqual(values['a'], 2)
        self.assertEqual(values['b'], 3)
        self.assertEqual(values['_c'], 4)

        values = Values(Values(a=1, c=4), a=2, b=3)
        self.assertEqual(values['a'], 2)
        self.assertEqual(values['b'], 3)
        self.assertEqual(values['c'], 4)

    def test_add_operation(self):
        values = Values(a=1, b=3)
        values = values + {'a': 2, 'c': 4}
        self.assertEqual(values['a'], 2)
        self.assertEqual(values['b'], 3)
        self.assertEqual(values['c'], 4)

    def test_radd_operation(self):
        values = Values(a=1, b=3)
        values = {'a': 2, 'c': 4} + values
        self.assertEqual(values['a'], 1)
        self.assertEqual(values['b'], 3)
        self.assertEqual(values['c'], 4)

    def test_iadd_operation(self):
        values = Values(a=1, b=3)
        values += {'a': 2, 'c': 4}
        self.assertEqual(values['a'], 2)
        self.assertEqual(values['b'], 3)
        self.assertEqual(values['c'], 4)

    def test_subclassing(self):
        class AB(Values):
            a = 1
            b = 2

        values = AB()
        self.assertEqual(values['a'], 1)
        self.assertEqual(values['b'], 2)
        self.assertRaises(KeyError, values.__getitem__, 'c')
        self.assertRaises(AttributeError, getattr, values, 'a')
        self.assertRaises(AttributeError, getattr, values, 'b')
        self.assertRaises(AttributeError, getattr, values, 'c')

        values = AB(b=3, c=4)
        self.assertEqual(values['a'], 1)
        self.assertEqual(values['b'], 3)
        self.assertEqual(values['c'], 4)

        values += {'a': 2}
        self.assertEqual(values['a'], 2)
        self.assertEqual(values['b'], 3)
        self.assertEqual(values['c'], 4)

    def test_sub_subclassing(self):
        class AB(Values):
            a = 1
            b = 2

        class ABCD(AB):
            c = 3
            d = 4

        values = ABCD(a=2, c=4)
        self.assertEqual(values['a'], 2)
        self.assertEqual(values['b'], 2)
        self.assertEqual(values['c'], 4)
        self.assertEqual(values['d'], 4)

    def test_multiple_inheritance(self):
        class A(Values):
            a = 1

        class AB(Values):
            a = 2
            b = 3

        class ABC(A, AB):
            c = 4

        values = ABC()
        self.assertEqual(values['a'], 1)
        self.assertEqual(values['b'], 3)
        self.assertEqual(values['c'], 4)
