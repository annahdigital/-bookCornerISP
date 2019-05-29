class Book:

    def __init__(self, name=None, author=None, year=0, description=None):
        self._name = name
        self._author = author
        self._year = year
        self._description = description
        self._tag_list = []
        self._genre_list = []

    def add_tag(self, tag):
        if tag not in self._tag_list:
            self._tag_list.append(tag)

    def add_genre(self, genre):
        if genre not in self._genre_list:
            self._genre_list.append(genre)

    def delete_tag(self, tag):
        self._tag_list.remove(tag)

    def delete_genre(self, genre):
        self._genre_list.remove(genre)

    def __str__(self):
        s = "\t\t\tName: " + self._name + "\n"
        s += "Author: " + self._author + "\n"
        if self._year != 0:
            s += "Year: " + str(self._year) + "\n"
        else:
            s += "Year: － \n"
        if self._description != None:
            s += "Description: " + self._description + "\n"
        else:
            s += "Description: － \n"
        s += "Genres: \n"
        for genre in self._genre_list:
            s += "\t" + genre + "\n"
        s += "Tags: \n"
        for tag in self._tag_list:
            s += "\t" + tag + "\n"
        return s

    def __eq__(self, other):
        return self._name == other.name

    def set_name(self, name):
        self._name = name

    def set_author(self, author):
        self._author = author

    def set_year(self, year):
        self._year = year

    def set_description(self, description):
        self._description = description

    @property
    def name(self):
        return self._name

    @property
    def author(self):
        return self._author

    @property
    def year(self):
        return self._year

    @property
    def description(self):
        return self._description

    @property
    def tag_list(self):
        return self._tag_list

    @property
    def genre_list(self):
        return self._genre_list





