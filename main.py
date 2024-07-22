import json
import os

class Book:
    """
    Класс для представления книги.

    Атрибуты:
        id (int): Уникальный идентификатор книги.
        title (str): Название книги.
        author (str): Автор книги.
        year (int): Год издания книги.
        status (str): Статус книги ("в наличии" или "выдана").
    """

    def __init__(self, title: str, author: str, year: int):
        """
        Инициализирует новый экземпляр класса Book.

        Аргументы:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.
        """
        self.id: int = self.generate_id()
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = "в наличии"

    def generate_id(self) -> int:
        """
        Генерирует уникальный идентификатор для новой книги.

        Возвращает:
            int: Уникальный идентификатор книги.
        """
        books: list = load_books()
        if not books:
            return 1
        return max(book["id"] for book in books) + 1

    def to_dict(self) -> dict:
        """
        Преобразует экземпляр класса Book в словарь.

        Возвращает:
            dict: Словарь, содержащий информацию о книге.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

def load_books() -> list:
    """
    Загружает книги из файла "books.json".

    Возвращает:
        list: Список книг в формате словаря.
    """
    if not os.path.exists("books.json"):
        return []
    try:
        with open("books.json", "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_books(books: list) -> None:
    """
    Сохраняет книги в файл "books.json".

    Аргументы:
        books (list): Список книг в формате словаря.
    """
    with open("books.json", "w") as f:
        json.dump(books, f)

def add_book(title: str, author: str, year: int) -> None:
    """
    Добавляет новую книгу в библиотеку.

    Аргументы:
        title (str): Название книги.
        author (str): Автор книги.
        year (int): Год издания книги.
    """
    book: Book = Book(title, author, year)
    books: list = load_books()
    books.append(book.to_dict())
    save_books(books)
    print(f"Книга '{title}' успешно добавлена.")

def delete_book(book_id: int) -> None:
    """
    Удаляет книгу из библиотеки по ее идентификатору.

    Аргументы:
        book_id (int): Идентификатор книги.
    """
    books: list = load_books()
    if not any(book["id"] == book_id for book in books):
        print("Книга не найдена.")
        return
    books = [book for book in books if book["id"] != book_id]
    save_books(books)
    print("Книга успешно удалена.")

def search_books(query: str, field: str = "title") -> list:
    """
    Ищет книги по заданному запросу.

    Аргументы:
        query (str): Запрос для поиска.
        field (str): Поле, по которому ведется поиск ("title", "author" или "year").

    Возвращает:
        list: Список книг, удовлетворяющих запросу.
    """
    books: list = load_books()
    results: list = [book for book in books if book[field].lower() == query.lower()]
    return results

def display_books() -> None:
    """
    Отображает все книги в библиотеке.
    """
    books: list = load_books()
    for book in books:
        print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, Год: {book['year']}, Статус: {book['status']}")

def change_status(book_id: int, new_status: str) -> None:
    """
    Изменяет статус книги в библиотеке.

    Аргументы:
        book_id (int): Идентификатор книги.
        new_status (str): Новый статус книги ("в наличии" или "выдана").
    """
    books: list = load_books()
    if not any(book["id"] == book_id for book in books):
        print("Книга не найдена.")
        return
    books = [book if book["id"] != book_id else {**book, "status": new_status} for book in books]
    save_books(books)
    print(f"Статус книги успешно изменен на '{new_status}'.")

def main() -> None:
    """
    Главная функция, запускающая систему управления библиотекой.
    """
    while True:
        print("\nСистема управления библиотекой")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice: int = int(input("Выберите действие: "))

        if choice == 1:
            title: str = input("Введите название книги: ")
            author: str = input("Введите автора книги: ")
            year: int = int(input("Введите год издания книги: "))
            add_book(title, author, year)
        elif choice == 2:
            book_id: int = int(input("Введите ID книги, которую хотите удалить: "))
            delete_book(book_id)
        elif choice == 3:
            query: str = input("Введите запрос для поиска: ")
            results: list = search_books(query)
            for result in results:
                print(f"ID: {result['id']}, Название: {result['title']}, Автор: {result['author']}, Год: {result['year']}, Статус: {result['status']}")
        elif choice == 4:
            display_books()
        elif choice == 5:
            book_id: int = int(input("Введите ID книги, статус которой хотите изменить: "))
            new_status: str = input("Введите новый статус книги ('в наличии' или 'выдана'): ")
            change_status(book_id, new_status)
        elif choice == 6:
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
