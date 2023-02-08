import typing
import unittest
from unittest import TestCase

from parameterized import parameterized  # type: ignore

from vmngclient.dataclasses import User
from vmngclient.typed_list import TypedList


class TestTypedList(TestCase):
    def setUp(self):
        self.u = User(username="User1")
        u1 = User(username="User1")
        u2 = User(username="User2")
        u3 = User(username="User3")
        self.users = [u1, u2, u3]
        self.typed_list = TypedList(User, self.users)

    @parameterized.expand([(str, []), (int, [1, 2, 3]), (User, [User("User1")])])  # type: ignore
    def test_init(self, _type, iterable):
        # Arrange, Act
        TypedList(_type, iterable)

    @parameterized.expand([(str, [1]), (int, [1, 2, "3"]), (User, [User(username="User1"), 1])])  # type: ignore
    def test_init_type_error(self, _type, iterable):
        # Arrange, Act, Assert
        with self.assertRaises(TypeError):
            TypedList(_type, iterable)

    def test_init_no_args(self):
        # Arrange, Act, Assert
        with self.assertRaises(TypeError):
            TypedList()

    def test_init_only_type(self):
        # Arrange, Act, Assert
        TypedList(str)

    @parameterized.expand([(str, [], "TypedList(str, [])"), (int, [1, 2, 3], "TypedList(int, [1, 2, 3])")])
    def test_repr_trival(self, _type, iterable, output):
        # Arrange, Act
        representation = repr(TypedList(_type, iterable))

        # Assert
        self.assertEqual(representation, output)

    # Integration
    def test_repr(self):
        # Arrange
        typed_list = TypedList(User, self.users)
        output = (
            "TypedList(User, ["
            "User(username='User1', password=None, group=[], locale=None, description=None, resource_group=None), "
            "User(username='User2', password=None, group=[], locale=None, description=None, resource_group=None), "
            "User(username='User3', password=None, group=[], locale=None, description=None, resource_group=None)])"
        )
        # Act
        representation = repr(typed_list)

        # Assert
        self.assertEqual(representation, output)

    @typing.no_type_check
    @parameterized.expand(
        [
            (str, ["1"], 1),
            (int, [1, 2, 3], 3),
            (User, None, 0),
            (User, [User(username="User1")], 1),
            (User, [User(username="User1"), User(username="User2")], 2),
        ]
    )
    def test_len(self, _type, iterable, length):
        # Arrange, Act
        output_length = len(TypedList(_type, iterable))

        # Assert
        self.assertEqual(output_length, length)

    @typing.no_type_check
    @parameterized.expand(
        [
            (str, ["1"], "1"),
            (int, [1, 2, 3], 3),
            (User, [User(username="User1")], User(username="User1")),
            (User, [User(username="User1"), User(username="User2")], User(username="User1")),
        ]
    )
    def test_contains_positive(self, _type, iterable, other):
        # Arrange, Act
        typed_list = TypedList(_type, iterable)

        # Assert
        self.assertTrue(other in typed_list)

    @typing.no_type_check
    @parameterized.expand(
        [
            (str, ["1"], "2"),
            (int, [1, 2, 3], 4),
            (User, [User(username="User1")], User(username="User2")),
            (User, [User(username="User1"), User(username="User2")], User(username="User3")),
        ]
    )
    def test_negative(self, _type, iterable, other):
        # Arrange, Act
        typed_list = TypedList(_type, iterable)

        # Assert
        self.assertFalse(other in typed_list)

    @typing.no_type_check
    @parameterized.expand(
        [
            (1, User(username="User2")),
            (slice(1, 3, 1), TypedList(User, [User(username="User2"), User(username="User3")])),
        ]
    )
    def test_get_item(self, index, output):
        self.assertEqual(self.typed_list[index], output)

    @typing.no_type_check
    @parameterized.expand([(User(username="User1"),), (TypedList(User, [User("User3")]),)])
    def test_eq_negative(self, other):
        self.assertFalse(self.users == other)

    def test_eq_false_sort(self):
        # Arrange
        u1 = User(username="User1")
        u2 = User(username="User2")
        u3 = User(username="User3")

        # Act, Assert
        self.assertFalse(self.users == [u1, u3, u2])

    def test_eq(self):
        # Arrange
        u1 = User(username="User1")
        u2 = User(username="User2")
        u3 = User(username="User3")

        # Act, Assert
        self.assertTrue(self.users == [u1, u2, u3])

    def test_set_item(self):
        # Arrange
        u1 = User(username="User1")
        u2 = User(username="User2")
        u3 = User(username="User3")

        users = TypedList(User, [u1, u2])

        # Act
        users[1] = u3

        # Assert
        self.assertEqual(users[1], u3)
        self.assertEqual(users[0], u1)
        with self.assertRaises(IndexError):
            users[2]
        self.assertNotEqual(users[1], u2)
        with self.assertRaises(TypeError):
            users[1] = 2

    def test_insert(self):
        # Arrange
        u1 = User(username="User1")
        u2 = User(username="User2")
        u3 = User(username="User3")

        users = TypedList(User, [u1, u2])

        # Act
        users.insert(1, u3)

        # Assert
        self.assertEqual(users[0], u1)
        self.assertEqual(users[1], u3)
        self.assertEqual(users[2], u2)
        with self.assertRaises(IndexError):
            users[3]
        self.assertNotEqual(users[1], u2)
        with self.assertRaises(TypeError):
            users.insert(1, "2")


if __name__ == "__main__":
    unittest.main()
