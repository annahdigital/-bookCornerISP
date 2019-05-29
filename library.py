from book import Book
from author import Author


class Library:

    def __init__(self):
        self._book_list = []
        self._author_list = []

    def __len__(self):
        if not self._author_list and not self._book_list:
            return 0
        else:
            return len(self._book_list)

    def __str__(self):
        s = "\t\t\tCurrent library: \n"
        s += "\t\tBooks: \n"
        for book in self._book_list:
            s += book.name + ", " + book.author + "\n"
        s += "\t\tAuthors: \n"
        for author in self._author_list:
            s += author.name + "\n"
        return s

    def genre_list(self):
        genre_list = list()
        for book in self.book_list:
            for genre in book.genre_list:
                if genre not in genre_list:
                    genre_list.append(genre)
        for author in self.author_list:
            for genre in author.genre_list:
                if genre not in genre_list:
                    genre_list.append(genre)
        return genre_list

    def tag_list(self):
        tag_list = list()
        for book in self.book_list:
            for tag in book.tag_list:
                if tag not in tag_list:
                    tag_list.append(tag)
        return tag_list

    def add_book(self, name, author=None, year=0, description=None):
        new_book = Book(name, author, year, description)
        if new_book not in self._book_list:
            self._book_list.append(new_book)
            return True
        return False

    def add_author(self, name,  birth_year=0, death_year=0, description=None):
        new_author = Author(name,  birth_year, death_year, description)
        if new_author not in self._author_list:
            self._author_list.append(new_author)
            return True
        return False

    def delete_book(self, name):
        this_book = Book(name)
        if this_book in self._book_list:
            self._book_list.remove(this_book)
            return True
        return False

    def delete_author(self, name):
        '''this_author = Author(name)
        if this_author in self._author_list:
            self._author_list.remove(this_author)
            return True
        return False'''
        if len(self.author_list) > 0:
            for author in self._author_list:
                if author.name == name:
                    self.author_list.remove(author)
                    return True
        return False

    def edit_book(self, name, author=None, year=0, description=None):
        this_book = Book(name, author, year, description)
        if this_book not in self._book_list:
            return False
        self.delete_book(this_book.name)
        self._book_list.append(this_book)
        return True

    def edit_author(self, name,  birth_year=0, death_year=0, description=None):
        this_author = Author(name,  birth_year, death_year, description)
        if this_author not in self._author_list:
            return False
        self.delete_author(this_author.name)
        self._author_list.append(this_author)
        return True

    def search_author(self, name):
        this_author = Author(name)
        if this_author not in self._author_list:
            return False
        else:
            return True

    def search_book(self, name):
        this_book = Book(name)
        if this_book not in self._book_list:
            return False
        else:
            return True

    def return_book_by_name(self, name):
        this_book = Book(name)
        for book in self.book_list:
            if book.name == name:
                return book
        return None

    def return_author_by_name(self, name):
        this_author = Author(name)
        for author in self.author_list:
            if author.name == name:
                return author
        return None

    def get_info_about_book(self, name):
        for book in self._book_list:
            if book.name == name:
                print(book)
                return
        print("There is no book with this name.")

    def get_info_about_author(self, name):
        for author in self._author_list:
            if author.name == name:
                print(author)
                return
        print("There is no author with this name.")

    def search_by_tag(self, tag):
        needed_books = []
        for book in self._book_list:
            for tags in book.tag_list:
                if tags == tag:
                    needed_books.append(book)
        return needed_books

    def search_by_genre(self, genre):
        needed_books = []
        needed_authors = []
        for book in self._book_list:
            for genres in book.genre_list:
                if genres == genre:
                    needed_books.append(book)
        for author in self._author_list:
            for genres in author.genre_list:
                if genres == genre:
                    needed_authors.append(author)
        return needed_books, needed_authors

    def add_book_object(self, book):
        if book not in self._book_list:
            self._book_list.append(book)
            return True
        return False

    def add_author_object(self, author):
        if author not in self._author_list:
            self._author_list.append(author)
            return True
        return False

    def book_table_list(self):
        table_list = list()
        for book in self.book_list:
            this_book_list = list()
            this_book_list.append(book.name)
            this_book_list.append(book.author)
            this_book_list.append(book.year)
            this_book_list.append(book.description)
            s = ""
            for genre in book.genre_list:
                s += genre + ", "
            s = s[:-2]
            this_book_list.append(s)
            s = ""
            for tag in book.tag_list:
                s += tag + ", "
            s = s[:-2]
            this_book_list.append(s)
            table_list.append(this_book_list)
        return table_list

    def author_table_list(self):
        table_list = list()
        for author in self.author_list:
            this_author = list()
            this_author.append(author.name)
            this_author.append(author.birth_year)
            this_author.append(author.death_year)
            this_author.append(author.description)
            s = ""
            for genre in author.genre_list:
                s += genre + ", "
            s = s[:-2]
            this_author.append(s)
            s = ""
            for book in author.book_list:
                s += book + ", "
            s = s[:-2]
            this_author.append(s)
            table_list.append(this_author)
        return table_list

    @property
    def book_list(self):
        return self._book_list

    @property
    def author_list(self):
        return self._author_list
