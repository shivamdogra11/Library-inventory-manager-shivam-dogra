import os

FILENAME = "books.txt"

class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def to_line(self):
        return f"{self.title} | {self.author} | {self.isbn} | {self.status}\n"

    @classmethod
    def from_line(cls, line):
        parts = line.strip().split(" | ")
        if len(parts) == 4:
            return cls(parts[0], parts[1], parts[2], parts[3])
        return None

class LibraryInventory:
    def __init__(self):
        self.books = []
        self.load_books()

    def load_books(self):
        if not os.path.exists(FILENAME):
            return
        with open(FILENAME, "r") as f:
            for line in f:
                b = Book.from_line(line)
                if b:
                    self.books.append(b)

    def save_books(self):
        with open(FILENAME, "w") as f:
            for b in self.books:
                f.write(b.to_line())

    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        if not self.books:
            print("\nNo books in library.\n")
            return
        print("\n--- Library Books ---")
        for b in self.books:
            print(f"{b.title} - {b.author} (ISBN: {b.isbn}) [{b.status}]")
        print()

    def issue_book(self, isbn):
        b = self.search_by_isbn(isbn)
        if b:
            if b.issue():
                self.save_books()
                print("Book issued!\n")
            else:
                print("Book already issued.\n")
        else:
            print("Book not found.\n")

    def return_book(self, isbn):
        b = self.search_by_isbn(isbn)
        if b:
            if b.return_book():
                self.save_books()
                print("Book returned!\n")
            else:
                print("Book already available.\n")
        else:
            print("Book not found.\n")

library = LibraryInventory()

while True:
    print("----- Library Menu (Class + TXT) -----")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("0. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        title = input("Title: ")
        author = input("Author: ")
        isbn = input("ISBN: ")

        new_book = Book(title, author, isbn)
        library.add_book(new_book)
        print("Book added!\n")

    elif choice == "2":
        isbn = input("Enter ISBN to issue: ")
        library.issue_book(isbn)

    elif choice == "3":
        isbn = input("Enter ISBN to return: ")
        library.return_book(isbn)

    elif choice == "4":
        library.display_all()

    elif choice == "0":
        print("Exiting program...")
        break

    else:
        print("Invalid option.\n")
