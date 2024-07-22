import json
import os
import unittest
from unittest.mock import patch

import main

class TestLibrary(unittest.TestCase):
    def setUp(self):
        # Очищаем файл books.json перед каждым тестом
        with open("books.json", "w") as f:
            json.dump([], f)

    def tearDown(self):
        # Удаляем файл books.json после каждого теста
        os.remove("books.json")

    def test_add_book(self):
        main.add_book("Тестовая книга", "Тестовый автор", 2000)

        with open("books.json", "r") as f:
            books = json.load(f)

        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["title"], "Тестовая книга")
        self.assertEqual(books[0]["author"], "Тестовый автор")
        self.assertEqual(books[0]["year"], 2000)
        self.assertEqual(books[0]["status"], "в наличии")

    def test_delete_book(self):
        main.add_book("Тестовая книга", "Тестовый автор", 2000)

        with patch("builtins.input", return_value="1"):
            with patch("builtins.print"):
                main.delete_book(1)

        with open("books.json", "r") as f:
            books = json.load(f)

        self.assertEqual(len(books), 0)

    def test_search_books(self):
        main.add_book("Тестовая книга", "Тестовый автор", 2000)

        results = main.search_books("Тестовая книга")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Тестовая книга")
        self.assertEqual(results[0]["author"], "Тестовый автор")
        self.assertEqual(results[0]["year"], 2000)
        self.assertEqual(results[0]["status"], "в наличии")

    def test_change_status(self):
        main.add_book("Тестовая книга", "Тестовый автор", 2000)

        with patch("builtins.input", side_effect=["1", "выдана"]):
            with patch("builtins.print"):
                main.change_status(1, "выдана")

        with open("books.json", "r") as f:
            books = json.load(f)

        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["status"], "выдана")

if __name__ == "__main__":
    unittest.main()
