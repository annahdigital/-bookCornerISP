from library import Library

class User:

    def __init__(self, name, password=None, appInfo=None, book_list=None, author_list=None, tag_list=None, genre_list=None, moderation=False):
        self.library = Library()
        if not appInfo:
            self._favourite_books = []
            self._favourite_authors = []
            self._tags = []
            self._genres = []
            if name != "admin":
                self._moderation = False
            else:
                self._moderation = True
        else:
            self._tags = tag_list
            self._genres = genre_list
            for book_name in book_list:
                self.library.book_list.append(appInfo.library.return_book_by_name(book_name))
            for author_name in author_list:
                self.library.author_list.append(appInfo.library.return_author_by_name(author_name))
            self._moderation = moderation
        self._name = name
        self.thisname = name
        self._password = password

    def __eq__(self, other):
        return self._name == other.thisname

    @property
    def favourite_books(self):
        return self._favourite_books

    @property
    def favourite_authors(self):
        return self._favourite_authors

    @property
    def tags(self):
        return self._tags

    @property
    def genres(self):
        return self._genres

    @property
    def password(self):
        return self._password

    @property
    def name(self):
        return self._name

    @property
    def moderation(self):
        return self._moderation

    def add_books(self, name, author):
        self._favourite_books.update({name: author})

    def add_authors(self, name):
        self._favourite_authors.append(name)

    def add_tags(self, tag):
        self._tags.append(tag)

    def add_genres(self, genre):
        self._genres.append(genre)

    def change_password(self, current_password, new_password):
        if current_password == self._password:
            self._password = new_password
            return True
        return False

    def change_name(self, current_password, new_name):
        if current_password == self._password:
            self._name = new_name
            return True
        return False

    def validation(self, password):
        if password == self._password:
            return True
        return False

    def return_status(self):
        return self._moderation

    def change_status(self, moderation):
        self._moderation = moderation

    ''' def __str__(self):
            s = ""
            if self._name != "admin":
                s += "Name - " + self._name + "\t"
                s += "Favourite books: \t"
                for book in self._favourite_books:
                    s += book.password + ", " + book.value + "\n"
                s += "Favourite authors:"
                for author in self._favourite_authors:
                    s += author + "\t"
                s += "Favourite tags:"
                for tag in self._tags:
                    s += tag + "\t"
                s += "Favourite genres:"
                for genre in self._genre:
                    s += genre + "\t"
                if self._moderation:
                    s += "\nSpecial rights: True"
                else:
                    s += "\nSpecial rights: False"
                return s
            s += "It's admin."
            return s'''

