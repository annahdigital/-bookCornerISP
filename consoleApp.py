from library import Library
from user import User


class ConsoleApp:

    def __init__(self):
        self._library = Library()
        self._users = []
        self._users.append(User("admin", "42"))
        self._current_user = None

    def change_user(self):
        name = input("Enter user name.")
        if User(name) not in self._users:
            char = input("There is no user like that! Wanna add user? [+/-]\t")
            if char == "+":
                password = input("Enter a password or - if there is no password for user.\t")
                if password == "-":
                    password = None
                self._users.append(User(name, password))
                self._current_user = self._users[-1].name
            else:
                print("Can't find this user, so it's impossible to change current user.")
                return
        else:
            password = input("Enter a password or - if it doesn't exist,\t")
            if password == "-":
                password = None
            if not self.find_user_by_name(name).validation(password):
                print("Error. Incorrect password.")
                return
            self._current_user = name

    def adding_book_menu(self, name=None, author=None):
        if not name:
            name = input("Enter a name.\t")
            author = input("Enter an author.\t")
        else:
            print("Name - " + name)
            print("Author - " + author)
        try:
            year = int(input("Enter a year or 0 if unknown.\t"))
        except ValueError:
            print("Not valid year.")
            exit(1)
        description = input("Enter a description or - of unknown.\t")
        if description == "-":
            description = None
        if not self._library.add_book(name, author, year, description):
            print("This book already exists!")
        char = "+"
        while char == "+":
            char = input("Wanna add tags? \t")
            if char == "+":
                tag = input("Enter a tag. \t")
                self.library.book_list[-1].add_tag(tag)
        char = "+"
        while char == "+":
            char = input("Wanna add genres? \t")
            if char == "+":
                genre = input("Enter a genre. \t")
                self.library.book_list[-1].add_genre(genre)
        if not self._library.search_author(author):
            answer = input("Wanna add an author? [+/-]\t")
            if answer == "+":
                self.adding_author_menu(author)

    def adding_author_menu(self, name=None):
        if not name:
            name = input("Enter a name.\t")
        else:
            print("Name - " + name)
        try:
            birth_year = int(input("Enter a year of birth or 0 if unknown.\t"))
        except ValueError:
            print("Not valid year.")
            exit(1)
        try:
            death_year = int(input("Enter a year of death or 0 if unknown.\t"))
        except ValueError:
            print("Not valid year.")
            exit(1)
        description = input("Enter a description or - of unknown.\t")
        if description == "-":
            description = None
        if not self._library.add_author(name, birth_year, death_year, description):
            print("This author already exists.")
            return
        char = "+"
        while char == "+":
            char = input("Wanna add genres? \t")
            if char == "+":
                genre = input("Enter a genre. \t")
                self.library.author_list[-1].add_genre(genre)
        char = "+"
        while char == "+":
            char = input("Wanna add books? \t")
            if char == "+":
                book = input("Enter a book. \t")
                self._library.author_list[-1].add_book(book)
                if not self._library.search_book(book):
                    answer = input("Wanna add this book to the library? [+/-] \t")
                    if answer == "+":
                        self.adding_book_menu(book, name)

    def deleting_book_menu(self):
        if self.find_user_by_name(self._current_user).moderation:
            name = input("Enter a name.\t")
            if not self._library.delete_book(name):
                print("There is no book with that name.")
        else:
            print("You have no rights to do it. Change the user first.")

    def deleting_author_menu(self):
        if self.find_user_by_name(self._current_user).moderation:
            name = input("Enter a name.\t")
            if not self._library.delete_author(name):
                print("There is no author with that name.")
        else:
            print("You have no rights to do it. Change the user first.")

    def editing_book_menu(self):
        if self.find_user_by_name(self._current_user).moderation:
            name = input("Enter a name.\t")
            author = input("Enter an author.\t")
            try:
                year = int(input("Enter a year or 0 if unknown.\t"))
            except ValueError:
                print("Not valid year.")
                exit(1)
            description = input("Enter a description or - of unknown.\t")
            if description == "-":
                description = None
            if not self._library.edit_book(name, author, year, description):
                char = input("This book does not exist. Wanna add this book? [+/-]\t")
                if char == "+":
                    self._library.add_book(name, author, year, description)
        else:
            print("You have no rights to do it. Change the user first.")

    def editing_author_menu(self):
        if self.find_user_by_name(self._current_user).moderation:
            name = input("Enter a name.\t")
            try:
                birth_year = int(input("Enter a year of birth or 0 if unknown.\t"))
            except ValueError:
                print("Not valid year.")
                exit(1)
            try:
                death_year = int(input("Enter a year of death or 0 if unknown.\t"))
            except ValueError:
                print("Not valid year.")
                exit(1)
            description = input("Enter a description or - of unknown.\t")
            if description == "-":
                description = None
            if not self._library.edit_author(name, birth_year, death_year, description):
                char = input("This author does not exist. Wanna add this author? [+/-]\t")
                if char == "+":
                    self._library.add_author(name, birth_year, death_year, description)
        else:
            print("You have no rights to do it. Change the user first.")

    def book_info_menu(self):
        name = input("Enter a name.\t")
        self._library.get_info_about_book(name)

    def author_info_menu(self):
        name = input("Enter a name.\t")
        self._library.get_info_about_author(name)

    def tag_searching_menu(self):
        tag = input("Enter a tag.\t")
        this_book_list = self.library.search_by_tag(tag)
        print("Books with this tag:")
        if not len(this_book_list):
            print("There is no books with this tag.")
        for books in this_book_list:
            print(books.name + ", " + books.author)

    def genre_searching_menu(self):
        genre = input("Enter a genre.\t")
        this_book_list, this_author_list = self.library.search_by_genre(genre)
        print("Books with this genre:")
        if not len(this_book_list):
            print("There is no books with this genre.")
        for books in this_book_list:
            print(books.name + ", " + books.author)
        print("Authors associated with this genre:")
        if not len(this_author_list):
            print("There is no authors associated with this genre.")
        for authors in this_author_list:
            print(authors.name)

    def find_user_by_name(self, name):
        for user in self._users:
            if user.name == name:
                return user
        return None

    def add_favourite_tags(self):
        tag = input("Enter a tag.\t")
        if self._current_user != "admin":
            self.find_user_by_name(self._current_user).add_tags(tag)
        else:
            print("Forbidden operation - admin can't do it.")

    def add_favourite_genres(self):
        genre = input("Enter a genre.\t")
        if self._current_user != "admin":
            self.find_user_by_name(self._current_user).add_genres(genre)
        else:
            print("Forbidden operation - admin can't do it.")

    def add_favourite_authors(self):
        author = input("Enter a genre.\t")
        if self._current_user != "admin":
            self.find_user_by_name(self._current_user).add_authors(author)
        else:
            print("Forbidden operation - admin can't do it.")

    def add_favourite_books(self):
        book = input("Enter a name of the book.\t")
        author = input("Enter a name of the author.\t")
        if self._current_user != "admin":
            self.find_user_by_name(self._current_user).add_books(book, author)
        else:
            print("Forbidden operation - admin can't do it.")
        if not self._library.search_book(book):
            char = input("This book does not exist. Wanna add this book? [+/-]\t")
            if char == "+":
                self.adding_book_menu(book, author)

    def delete_user(self):
        name = input("Enter a name of the user.\t")
        if name != "admin":
            password = input("Enter a password or - if it doesn't exist,\t")
            if password == "-":
                password = None
            if not self.find_user_by_name(name).validation(password):
                print("Error. There is no user like this.")
                return
            self._users.remove(User(name, password))

    def user_preferences(self):
        print(self.find_user_by_name(self._current_user))

    def change_user_status(self):
        if self.find_user_by_name(self._current_user).moderation:
            name = input("Enter a name.\t")
            if not self.find_user_by_name(name):
                print("There is no user with this name!")
                return
            print("Current status: moderation rights  - " + str(self.find_user_by_name(name).moderation))
            char = input("Wanna change? [+/-]\t")
            if char == "+":
                self.find_user_by_name(name).moderation = not self.find_user_by_name(name).moderation
        else:
            print("Current user have no rights to change status.")

    @property
    def library(self):
        return self._library






