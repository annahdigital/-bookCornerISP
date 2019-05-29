class Author:

    def __init__(self, name=None,  birth_year=0, death_year=0, description=None):
        self._name = name
        self._birth_year = birth_year
        self._death_year = death_year
        self._description = description
        self._book_list = []
        self._genre_list = []

    def __str__(self):
        s = "\t\t\tName: " + self._name + "\n"
        if self._birth_year != 0:
            s += "Born: " + str(self._birth_year) + "\n"
        else:
            s += "Born: － \n"
        if self._death_year != 0:
            s += "Died: " + str(self._death_year) + "\n"
        else:
            s += "Died: － \n"
        if self._description != None:
            s += "Description: " + self._description + "\n"
        else:
            s += "Description: － \n"
        s += "Books: \n"
        for book in self._book_list:
            s += "\t" + book + "\n"
        s += "Genres: \n"
        for genre in self._genre_list:
            s += "\t" + genre + "\n"
        return s

    def __eq__(self, other):
        return self._name == other.name

    def add_book(self, book):
        if book not in self._book_list:
            self._book_list.append(book)

    def add_genre(self, genre):
        if genre not in self._genre_list:
            self._genre_list.append(genre)

    def delete_book(self, book):
        self._book_list.remove(book)

    def delete_genre(self, genre):
        self._genre_list.remove(genre)

    @property
    def name(self):
        return self._name

    @property
    def birth_year(self):
        return self._birth_year

    @property
    def death_year(self):
        return self._death_year

    @property
    def description(self):
        return self._description

    @property
    def book_list(self):
        return self._book_list

    @property
    def genre_list(self):
        return self._genre_list

    def set_name(self, name):
        self._name = name

    def set_death_year(self, year):
        self._death_year = year

    def set_birth_year(self, year):
        self._birth_year = year

    def set_description(self, description):
        self._description = description


