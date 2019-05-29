import sys
import pymongo
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from user import User
from library import Library
from author import Author
from book import Book
from PyQt5 import QtCore
from dialogs import *
from user_dialogs import *
from pymongo import MongoClient


class AppInfo:
    def __init__(self):
        client = MongoClient()
        database = client.local
        self.library = Library()
        list = database.books.find()
        for item in list:
            self.library.book_list.append(Book(item["name"], item["author"], item["year"], item["description"]))
            for tag in item["tags"]:
                self.library.return_book_by_name(item["name"]).add_tag(tag)
            for genre in item["genres"]:
                self.library.return_book_by_name(item["name"]).add_genre(genre)
        list = database.authors.find()
        for item in list:
            self.library.author_list.append(Author(item["name"], item["birth_year"], item["death_year"], item["description"]))
            for book in item["books"]:
                self.library.return_author_by_name(item["name"]).add_book(book)
            for genre in item["genres"]:
                self.library.return_author_by_name(item["name"]).add_genre(genre)
        self.users = []
        # self.users.append(User("admin", "42"))
        self.users_database = database.users
        self.books_database = database.books
        self.authors_database = database.authors
        list = database.users.find()
        for item in list:
            tag_list = []
            genre_list = []
            author_list = []
            book_list = []
            for tag in item["tags"]:
                tag_list.append(tag)
            for genre in item["genres"]:
                genre_list.append(genre)
            for book in item["books"]:
                book_list.append(book)
            for author in item["authors"]:
                author_list.append(author)
            new_user = User(item["name"], item["password"], self, book_list, author_list, tag_list, genre_list, item["moderation"])
            self.users.append(new_user)
        self.current_user = None

    def find_user_by_name(self, name):
        for user in self.users:
            if user.name == name:
                return user
        return None


class VisualApp(QtWidgets.QMainWindow):

    def __init__(self):
        self._appInfo = AppInfo()
        super(VisualApp, self).__init__()
        loadUi("welcomepage.ui", self)
        self._new_window = None
        # self.showMaximized()
        self.setWindowTitle("Welcome to the BookCorner!")
        self.pushButton.clicked.connect(lambda: self.user_input(self._appInfo))
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

    @pyqtSlot()
    def user_input(self, appInfo):
        name = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if name and password:
            if not self._appInfo.find_user_by_name(name):
                user_window = UserWindow(name, password, self._appInfo)
                user_window.exec_()
            else:
                if not self._appInfo.find_user_by_name(name).validation(password):
                    user_window = ErrorDialog()
                    user_window.exec_()
                else:
                    self._appInfo.current_user = name
                    self._new_window = MenuPage(appInfo)
                    self._new_window.show()
                    self.close()


# MAIN MENU  MAIN MENU  MAIN MENU  MAIN MENU  MAIN MENU  MAIN MENU  MAIN MENU  MAIN MENU  MAIN MENU  MAIN MENU MAIN MENU
class MenuPage(QtWidgets.QMainWindow):
    def __init__(self, appInfo):
        super(MenuPage, self).__init__()
        loadUi('menupage.ui', self)
        self._new_window = None
        self.pushButton_9.clicked.connect(lambda: self.show_user_menu(appInfo))
        self.pushButton.clicked.connect(lambda: self.show_books(appInfo))
        self.pushButton_2.clicked.connect(lambda: self.show_authors(appInfo))
        self.pushButton_3.clicked.connect(lambda: self.show_tags(appInfo))
        self.pushButton_4.clicked.connect(lambda: self.show_genres(appInfo))
        self.pushButton_5.clicked.connect(lambda: self.user_books(appInfo))
        self.pushButton_6.clicked.connect(lambda: self.user_authors(appInfo))
        self.pushButton_7.clicked.connect(lambda: self.user_tags(appInfo))
        self.pushButton_8.clicked.connect(lambda: self.user_genres(appInfo))
        self.toolButton.clicked.connect(lambda: self.change_user(appInfo))
        self.pushButton_10.clicked.connect(lambda: self.moderation(appInfo))
        self.label.setText("Current user: " + appInfo.current_user)

    @pyqtSlot()
    def moderation(self, appInfo):
        if appInfo.current_user == "admin":
            self._new_window = UserModeration(appInfo)
            self._new_window.exec_()
        else:
            message = ErrorDialog()
            message.label_2.setText("You need to log in as admin.")
            message.pushButton_2.setText("Change user.")
            message.exec_()

    @pyqtSlot()
    def user_books(self, appInfo):
        self._new_window = MyBooks(appInfo)
        self._new_window.show()
        self.close()

    @pyqtSlot()
    def user_authors(self, appInfo):
        self._new_window = myAuthors(appInfo)
        self._new_window.show()
        self.close()

    @pyqtSlot()
    def user_tags(self, appInfo):
        self._new_window = MyTags(appInfo)
        self._new_window.exec_()

    @pyqtSlot()
    def user_genres(self, appInfo):
        self._new_window = MyGenres(appInfo)
        self._new_window.exec_()

    @pyqtSlot()
    def show_genres(self, appInfo):
        message = GenresMenu(appInfo)
        message.exec_()

    @pyqtSlot()
    def show_tags(self, appInfo):
        message = TagsMenu(appInfo)
        message.exec_()

    @pyqtSlot()
    def show_user_menu(self, appInfo):
        if appInfo.current_user != "admin":
            self._new_window = UserMenu(appInfo)
            self._new_window.show()
            self.close()
        else:
            message = ErrorDialog()
            message.label_2.setText("Logged in as admin.")
            message.pushButton_2.setText("Ok")
            message.exec_()

    @pyqtSlot()
    def change_user(self, appInfo):
        user_window = ChangingUserMenu(appInfo)
        user_window.exec_()
        self.label.setText("Current user: " + appInfo.current_user)

    @pyqtSlot()
    def show_books(self, appInfo):
        self._new_window = BookMenu(appInfo)
        self._new_window.show()
        self.close()

    @pyqtSlot()
    def show_authors(self, appInfo):
        self._new_window = AuthorMenu(appInfo)
        self._new_window.show()
        self.close()


# INFO ABOUT USER  INFO ABOUT USER  INFO ABOUT USER  INFO ABOUT USER  INFO ABOUT USER  INFO ABOUT USER  INFO ABOUT USER
class UserMenu(QtWidgets.QMainWindow):
    def __init__(self, appInfo):
        super(UserMenu, self).__init__()
        loadUi('userpage.ui', self)
        self._new_window = None
        self.pushButton_5.clicked.connect(lambda: self.to_the_menu(appInfo))
        self.pushButton_6.clicked.connect(lambda: self.change_password(appInfo))
        self.label.setText(appInfo.current_user)
        self.toolButton.clicked.connect(lambda: self.change_user(appInfo))
        if appInfo.find_user_by_name(appInfo.current_user).return_status():
            self.checkBox.setChecked(True)
        self.listWidget_3.addItems(appInfo.find_user_by_name(appInfo.current_user).tags)
        self.listWidget_4.addItems(appInfo.find_user_by_name(appInfo.current_user).genres)
        name_list = [author.name for author in appInfo.find_user_by_name(appInfo.current_user).library.author_list]
        self.listWidget_2.addItems(name_list)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(("Name", "Author"))
        self.tableWidget.setRowCount(len(appInfo.find_user_by_name(appInfo.current_user).library.book_list))
        row = 0
        for book in appInfo.find_user_by_name(appInfo.current_user).library.book_list:
            item = QtWidgets.QTableWidgetItem(book.name)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(row, 0, item)
            item = QtWidgets.QTableWidgetItem(book.author)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(row, 1, item)
            row += 1

    @pyqtSlot()
    def to_the_menu(self, appInfo):
        self._new_window = MenuPage(appInfo)
        self._new_window.show()
        self.close()

    @pyqtSlot()
    def change_user(self, appInfo):
        user_window = ChangingUserMenu(appInfo)
        user_window.exec_()
        self.label.setText(appInfo.current_user)
        if appInfo.find_user_by_name(appInfo.current_user).return_status():
            self.checkBox.setChecked(True)

    @pyqtSlot()
    def change_password(self, appInfo):
        user_window = ChangePasswordDialod(appInfo)
        user_window.exec_()


# BOOK MENU  BOOK MENU  BOOK MENU  BOOK MENU  BOOK MENU  BOOK MENU  BOOK MENU  BOOK MENU  BOOK MENU  BOOK MENU
class BookMenu(QtWidgets.QMainWindow):
    def __init__(self, appInfo):
        super(BookMenu, self).__init__()
        loadUi('books_n_authors.ui', self)
        self._new_window = None
        self.pushButton_5.clicked.connect(lambda: self.to_the_menu(appInfo))
        self.toolButton.clicked.connect(lambda: self.change_user(appInfo))
        self.pushButton_6.clicked.connect(lambda: self.adding_book(appInfo))
        self.pushButton_8.clicked.connect(lambda: self.delete_book(appInfo))
        self.pushButton_9.clicked.connect(lambda: self.edit_book(appInfo))
        self.toolButton.clicked.connect(lambda: self.change_user(appInfo))
        self.pushButton_10.clicked.connect(lambda: self.initialize(appInfo))
        self.lineEdit.textChanged.connect(lambda: self.search(appInfo))
        self.tableWidget.setColumnCount(6)
        self.initialize(appInfo)
        self.pushButton_11.clicked.connect(lambda: self.add_to_fav(appInfo))
        self.current_name = None
        self.tableWidget.cellDoubleClicked.connect(lambda: self.show_description(appInfo))
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)

    @pyqtSlot()
    def show_description(self, appInfo):
        text = self.tableWidget.item(self.tableWidget.currentRow(), 3).text()
        new_window = DescriptionDialog(text)
        new_window.exec_()

    @pyqtSlot()
    def search(self, appInfo):
        if self.lineEdit.text():
            text = str(self.comboBox.currentText())
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(6)
            self.tableWidget.setHorizontalHeaderLabels(("Name", "Author", "Year", "Description", "Genres", "Tags"))
            all_items = appInfo.library.book_table_list()
            if text == "name":
                this_column = 0
            elif text == "author":
                this_column = 1
            elif text == "year":
                this_column = 2
            elif text == "description":
                this_column = 3
            elif text == "genre":
                this_column = 4
            elif text == "tag":
                this_column = 5
            row = 0
            result = []
            for result_list in all_items:
                if self.lineEdit.text().lower() in str(result_list[this_column]).lower():
                    result.append(result_list)
            self.tableWidget.setRowCount(len(result))
            row = 0
            for result1 in result:
                column = 0
                for item in result1:
                    item = QtWidgets.QTableWidgetItem(item)
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget.setItem(row, column, item)
                    column += 1
                row += 1

        else:
            self.initialize(appInfo)

    @pyqtSlot()
    def add_to_fav(self, appInfo):
        if self.tableWidget.item(self.tableWidget.currentRow(), 0):
            book = appInfo.library.return_book_by_name(self.tableWidget.item(self.tableWidget.currentRow(), 0).text())
            if book not in appInfo.find_user_by_name(appInfo.current_user).library.book_list:
                appInfo.find_user_by_name(appInfo.current_user).library.book_list.append(book)
                this_user = appInfo.find_user_by_name(appInfo.current_user)
                books = appInfo.users_database.find_one({"name": appInfo.current_user})["books"]
                books.append(self.tableWidget.item(self.tableWidget.currentRow(), 0).text())
                authors = appInfo.users_database.find_one({"name": appInfo.current_user})["authors"]
                tags = appInfo.users_database.find_one({"name": appInfo.current_user})["tags"]
                genres = appInfo.users_database.find_one({"name": appInfo.current_user})["genres"]
                appInfo.users_database.update({"name": appInfo.current_user}, {"name": appInfo.current_user,
                                                                               "password": this_user.password,
                                                                               "moderation": this_user.moderation,
                                                                               "books": books, "authors": authors,
                                                                               "tags": tags, "genres": genres})

    @pyqtSlot()
    def edit_book(self, appInfo):
        if not appInfo.find_user_by_name(appInfo.current_user).return_status():
            message = ErrorDialog()
            message.label_2.setText("Access denied.")
            message.exec_()
        else:
            if self.tableWidget.item(self.tableWidget.currentRow(), 0):
                self.current_name = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
                new_window = EditingBookMenu(appInfo, appInfo.library.return_book_by_name(self.current_name))
                new_window.exec_()
                self.initialize(appInfo)

    @pyqtSlot()
    def delete_book(self, appInfo):
        if not appInfo.find_user_by_name(appInfo.current_user).return_status():
            message = ErrorDialog()
            message.label_2.setText("Access denied.")
            message.exec_()
        else:
            if self.tableWidget.item(self.tableWidget.currentRow(), 0):
                self.current_name = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
                appInfo.library.delete_book(self.current_name)
                appInfo.books_database.delete_one({"name": self.current_name})
                for user in appInfo.users:
                    user.library.delete_author(self.tableWidget.item(self.tableWidget.currentRow(), 0).text())
                    book_list = [book.name for book in user.library.book_list]
                    author_list = [author.name for author in user.library.author_list]
                    appInfo.users_database.update({"name": user.name}, {"name": user.name, "password": user.password, "moderation": user.moderation,
                                                   "books": book_list, "authors": author_list,
                                                   "tags": user.tags, "genres": user.genres})
                self.initialize(appInfo)

    def initialize(self, appInfo):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(("Name", "Author", "Year", "Description", "Genres", "Tags"))
        self.tableWidget.setRowCount(len(appInfo.library.book_list))
        all_items = appInfo.library.book_table_list()
        row = 0
        for result_list in all_items:
            column = 0
            for item in result_list:
                item = QtWidgets.QTableWidgetItem(item)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row, column, item)
                column += 1
            row += 1

    @pyqtSlot()
    def to_the_menu(self, appInfo):
        self._new_window = MenuPage(appInfo)
        self._new_window.show()
        self.close()

    @pyqtSlot()
    def change_user(self, appInfo):
        user_window = ChangingUserMenu(appInfo)
        user_window.exec_()

    @pyqtSlot()
    def adding_book(self, appInfo):
        if not appInfo.find_user_by_name(appInfo.current_user).return_status():
            message = ErrorDialog()
            message.label_2.setText("Access denied.")
            message.exec_()
        else:
            new_window = AddingBookMenu(appInfo)
            new_window.exec_()
            self.initialize(appInfo)


class AuthorMenu(QtWidgets.QMainWindow):
    def __init__(self, appInfo):
        super(AuthorMenu, self).__init__()
        loadUi('books_n_authors.ui', self)
        self._new_window = None
        self.label.setText("AUTHORS")
        self.pushButton_5.clicked.connect(lambda: self.to_the_menu(appInfo))
        self.pushButton_6.setText("Add author")
        self.pushButton_7.setText("Search for author")
        self.comboBox.clear()
        self.comboBox.addItems(["name", "book", "birth year", "death year", "description", "genre"])
        self.pushButton_6.clicked.connect(lambda: self.adding_author(appInfo))
        self.pushButton_8.clicked.connect(lambda: self.delete_author(appInfo))
        self.pushButton_9.clicked.connect(lambda: self.edit_author(appInfo))
        self.pushButton_10.clicked.connect(lambda: self.initialize(appInfo))
        self.toolButton.clicked.connect(lambda: self.change_user(appInfo))
        self.tableWidget.setColumnCount(6)
        self.initialize(appInfo)
        self.lineEdit.textChanged.connect(lambda: self.search(appInfo))
        self.pushButton_11.clicked.connect(lambda: self.add_to_fav(appInfo))
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.current_name = None
        self.tableWidget.cellDoubleClicked.connect(lambda: self.show_description(appInfo))

    @pyqtSlot()
    def show_description(self, appInfo):
        text = self.tableWidget.item(self.tableWidget.currentRow(), 3).text()
        new_window = DescriptionDialog(text)
        new_window.exec_()

    @pyqtSlot()
    def search(self, appInfo):
        if self.lineEdit.text():
            text = str(self.comboBox.currentText())
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(6)
            self.tableWidget.setHorizontalHeaderLabels(("Name", "Birth", "Death", "Description", "Genres", "Books"))
            all_items = appInfo.library.author_table_list()
            if text == "name":
                this_column = 0
            elif text == "birth year":
                this_column = 1
            elif text == "death year":
                this_column = 2
            elif text == "description":
                this_column = 3
            elif text == "genre":
                this_column = 4
            elif text == "book":
                this_column = 5
            row = 0
            result = []
            for result_list in all_items:
                if self.lineEdit.text().lower() in str(result_list[this_column]).lower():
                    result.append(result_list)
            self.tableWidget.setRowCount(len(result))
            row = 0
            for result1 in result:
                column = 0
                for item in result1:
                    item = QtWidgets.QTableWidgetItem(item)
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget.setItem(row, column, item)
                    column += 1
                row += 1

        else:
            self.initialize(appInfo)

    @pyqtSlot()
    def add_to_fav(self, appInfo):
        if self.tableWidget.item(self.tableWidget.currentRow(), 0):
            author = appInfo.library.return_author_by_name(self.tableWidget.item(self.tableWidget.currentRow(), 0).text())
            if author not in appInfo.find_user_by_name(appInfo.current_user).library.author_list:
                appInfo.find_user_by_name(appInfo.current_user).library.author_list.append(author)
                this_user = appInfo.find_user_by_name(appInfo.current_user)
                books = appInfo.users_database.find_one({"name": appInfo.current_user})["books"]
                authors = appInfo.users_database.find_one({"name": appInfo.current_user})["authors"]
                authors.append(self.tableWidget.item(self.tableWidget.currentRow(), 0).text())
                tags = appInfo.users_database.find_one({"name": appInfo.current_user})["tags"]
                genres = appInfo.users_database.find_one({"name": appInfo.current_user})["genres"]
                appInfo.users_database.update({"name": appInfo.current_user}, {"name": appInfo.current_user,
                                                                               "password": this_user.password,
                                                                               "moderation": this_user.moderation,
                                                                               "books": books, "authors": authors,
                                                                               "tags": tags, "genres": genres})

    @pyqtSlot()
    def delete_author(self, appInfo):
        if not appInfo.find_user_by_name(appInfo.current_user).return_status():
            message = ErrorDialog()
            message.label_2.setText("Access denied.")
            message.exec_()
        else:
            if self.tableWidget.item(self.tableWidget.currentRow(), 0):
                self.current_name = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
                appInfo.library.delete_author(self.current_name)
                appInfo.authors_database.delete_one({"name": self.current_name})
                for user in appInfo.users:
                    user.library.delete_author(self.tableWidget.item(self.tableWidget.currentRow(), 0).text())
                    if user.library.book_list != [None]:
                        book_list = [book.name for book in user.library.book_list]
                    if user.library.author_list != [None]:
                        author_list = [author.name for author in user.library.author_list]
                    appInfo.users_database.update({"name": user.name}, {"name": user.name, "password": user.password, "moderation": user.moderation,
                                                   "books": book_list, "authors": author_list,
                                                   "tags": user.tags, "genres": user.genres})
                self.initialize(appInfo)

    def initialize(self, appInfo):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(("Name", "Birth", "Death", "Description", "Genres", "Books"))
        self.tableWidget.setRowCount(len(appInfo.library.author_list))
        all_items = appInfo.library.author_table_list()
        row = 0
        for result_list in all_items:
            column = 0
            for item in result_list:
                item = QtWidgets.QTableWidgetItem(item)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row, column, item)
                column += 1
            row += 1

    @pyqtSlot()
    def to_the_menu(self, appInfo):
        self._new_window = MenuPage(appInfo)
        self._new_window.show()
        self.close()

    @pyqtSlot()
    def change_user(self, appInfo):
        user_window = ChangingUserMenu(appInfo)
        user_window.exec_()

    @pyqtSlot()
    def adding_author(self, appInfo):
        if not appInfo.find_user_by_name(appInfo.current_user).return_status():
            message = ErrorDialog()
            message.label_2.setText("Access denied.")
            message.exec_()
        else:
            new_window = AddingAuthorMenu(appInfo)
            new_window.exec_()
            self.initialize(appInfo)

    @pyqtSlot()
    def edit_author(self, appInfo):
        if not appInfo.find_user_by_name(appInfo.current_user).return_status():
            message = ErrorDialog()
            message.label_2.setText("Access denied.")
            message.exec_()
        else:
            if self.tableWidget.item(self.tableWidget.currentRow(), 0):
                self.current_name = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
                new_window = EditingAuthorMenu(appInfo, appInfo.library.return_author_by_name(self.current_name))
                new_window.exec_()
                self.initialize(appInfo)


# MY BOOKS  MY BOOKS  MY BOOKS  MY BOOKS  MY BOOKS  MY BOOKS  MY BOOKS  MY BOOKS  MY BOOKS  MY BOOKS  MY BOOKS
class MyBooks(QtWidgets.QMainWindow):
    def __init__(self, appInfo):
        super(MyBooks, self).__init__()
        loadUi('my_books.ui', self)
        self._new_window = None
        self.pushButton_5.clicked.connect(lambda: self.to_the_menu(appInfo))
        self.toolButton.clicked.connect(lambda: self.change_user(appInfo))
        self.pushButton_6.clicked.connect(lambda: self.add_book(appInfo))
        self.pushButton_8.clicked.connect(lambda: self.delete_book(appInfo))
        self.pushButton_10.clicked.connect(lambda: self.initialize(appInfo))
        self.lineEdit.textChanged.connect(lambda: self.search(appInfo))
        self.tableWidget.setColumnCount(6)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.initialize(appInfo)
        self.tableWidget.cellDoubleClicked.connect(lambda: self.show_description(appInfo))

    @pyqtSlot()
    def show_description(self, appInfo):
        text = self.tableWidget.item(self.tableWidget.currentRow(), 3).text()
        new_window = DescriptionDialog(text)
        new_window.exec_()

    @pyqtSlot()
    def initialize(self, appInfo):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(("Name", "Author", "Year", "Description", "Genres", "Tags"))
        self.tableWidget.setRowCount(len(appInfo.find_user_by_name(appInfo.current_user).library.book_list))
        all_items = appInfo.find_user_by_name(appInfo.current_user).library.book_table_list()
        row = 0
        for result_list in all_items:
            column = 0
            for item in result_list:
                item = QtWidgets.QTableWidgetItem(item)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row, column, item)
                column += 1
            row += 1

    @pyqtSlot()
    def search(self, appInfo):
        if self.lineEdit.text():
            text = str(self.comboBox.currentText())
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(6)
            self.tableWidget.setHorizontalHeaderLabels(("Name", "Author", "Year", "Description", "Genres", "Tags"))
            all_items = appInfo.find_user_by_name(appInfo.current_user).library.book_table_list()
            if text == "name":
                this_column = 0
            elif text == "author":
                this_column = 1
            elif text == "year":
                this_column = 2
            elif text == "description":
                this_column = 3
            elif text == "genre":
                this_column = 4
            elif text == "tag":
                this_column = 5
            row = 0
            result = []
            for result_list in all_items:
                if self.lineEdit.text().lower() in str(result_list[this_column]).lower():
                    result.append(result_list)
            self.tableWidget.setRowCount(len(result))
            row = 0
            for result1 in result:
                column = 0
                for item in result1:
                    item = QtWidgets.QTableWidgetItem(item)
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget.setItem(row, column, item)
                    column += 1
                row += 1

        else:
            self.initialize(appInfo)

    @pyqtSlot()
    def to_the_menu(self, appInfo):
        self._new_window = MenuPage(appInfo)
        self._new_window.show()
        self.close()

    @pyqtSlot()
    def change_user(self, appInfo):
        user_window = ChangingUserMenu(appInfo)
        user_window.exec_()
        self.initialize(appInfo)

    @pyqtSlot()
    def add_book(self, appInfo):
        dialog = FavBook(appInfo)
        dialog.exec_()
        self.initialize(appInfo)

    @pyqtSlot()
    def delete_book(self, appInfo):
        if self.tableWidget.item(self.tableWidget.currentRow(), 0):
            current_name = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            appInfo.find_user_by_name(appInfo.current_user).library.delete_book(current_name)
            this_user = appInfo.find_user_by_name(appInfo.current_user)
            books = appInfo.users_database.find_one({"name": appInfo.current_user})["books"]
            books.remove(current_name)
            authors = appInfo.users_database.find_one({"name": appInfo.current_user})["authors"]
            tags = appInfo.users_database.find_one({"name": appInfo.current_user})["tags"]
            genres = appInfo.users_database.find_one({"name": appInfo.current_user})["genres"]
            appInfo.users_database.update({"name": appInfo.current_user}, {"name": appInfo.current_user,
                                                                           "password": this_user.password,
                                                                           "moderation": this_user.moderation,
                                                                           "books": books, "authors": authors,
                                                                           "tags": tags, "genres": genres})
            self.initialize(appInfo)


class myAuthors(QtWidgets.QMainWindow):
    def __init__(self, appInfo):
        super(myAuthors, self).__init__()
        loadUi('my_books.ui', self)
        self._new_window = None
        self.label.setText("MY AUTHORS")
        self.pushButton_6.setText("Add author")
        self.pushButton_7.setText("Search for author:")
        self.comboBox.clear()
        self.comboBox.addItems(["name", "book", "birth year", "death year", "description", "genre"])
        self.lineEdit.textChanged.connect(lambda: self.search(appInfo))
        self.pushButton_5.clicked.connect(lambda: self.to_the_menu(appInfo))
        self.toolButton.clicked.connect(lambda: self.change_user(appInfo))
        self.pushButton_6.clicked.connect(lambda: self.add_author(appInfo))
        self.pushButton_8.clicked.connect(lambda: self.delete_author(appInfo))
        self.tableWidget.setColumnCount(6)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.initialize(appInfo)
        self.tableWidget.cellDoubleClicked.connect(lambda: self.show_description(appInfo))

    @pyqtSlot()
    def show_description(self, appInfo):
        text = self.tableWidget.item(self.tableWidget.currentRow(), 3).text()
        new_window = DescriptionDialog(text)
        new_window.exec_()

    @pyqtSlot()
    def search(self, appInfo):
        if self.lineEdit.text():
            text = str(self.comboBox.currentText())
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(6)
            self.tableWidget.setHorizontalHeaderLabels(("Name", "Birth", "Death", "Description", "Genres", "Books"))
            all_items = appInfo.find_user_by_name(appInfo.current_user).library.author_table_list()
            if text == "name":
                this_column = 0
            elif text == "birth year":
                this_column = 1
            elif text == "death year":
                this_column = 2
            elif text == "description":
                this_column = 3
            elif text == "genre":
                this_column = 4
            elif text == "book":
                this_column = 5
            row = 0
            result = []
            for result_list in all_items:
                if self.lineEdit.text().lower() in str(result_list[this_column]).lower():
                    result.append(result_list)
            self.tableWidget.setRowCount(len(result))
            row = 0
            for result1 in result:
                column = 0
                for item in result1:
                    item = QtWidgets.QTableWidgetItem(item)
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget.setItem(row, column, item)
                    column += 1
                row += 1

        else:
            self.initialize(appInfo)

    @pyqtSlot()
    def to_the_menu(self, appInfo):
        self._new_window = MenuPage(appInfo)
        self._new_window.show()
        self.close()

    @pyqtSlot()
    def change_user(self, appInfo):
        user_window = ChangingUserMenu(appInfo)
        user_window.exec_()
        self.initialize(appInfo)

    @pyqtSlot()
    def add_author(self, appInfo):
        dialog = FavAuthors(appInfo)
        dialog.exec_()
        self.initialize(appInfo)

    @pyqtSlot()
    def delete_author(self, appInfo):
        if self.tableWidget.item(self.tableWidget.currentRow(), 0):
            current_name = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            appInfo.find_user_by_name(appInfo.current_user).library.delete_author(current_name)
            this_user = appInfo.find_user_by_name(appInfo.current_user)
            books = appInfo.users_database.find_one({"name": appInfo.current_user})["books"]
            authors = appInfo.users_database.find_one({"name": appInfo.current_user})["authors"]
            authors.remove(current_name)
            tags = appInfo.users_database.find_one({"name": appInfo.current_user})["tags"]
            genres = appInfo.users_database.find_one({"name": appInfo.current_user})["genres"]
            appInfo.users_database.update({"name": appInfo.current_user}, {"name": appInfo.current_user,
                                                                           "password": this_user.password,
                                                                           "moderation": this_user.moderation,
                                                                           "books": books, "authors": authors,
                                                                           "tags": tags, "genres": genres})
        self.initialize(appInfo)

    @pyqtSlot()
    def initialize(self, appInfo):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(("Name", "Birth", "Death", "Description", "Genres", "Books"))
        self.tableWidget.setRowCount(len(appInfo.find_user_by_name(appInfo.current_user).library.author_list))
        all_items = appInfo.find_user_by_name(appInfo.current_user).library.author_table_list()
        row = 0
        for result_list in all_items:
            column = 0
            for item in result_list:
                item = QtWidgets.QTableWidgetItem(item)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row, column, item)
                column += 1
            row += 1


# MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN# MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN# MAIN MAIN MAIN MAIN MAIN
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = VisualApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
    #латентное размещение дирихле (лда алгоритм) темы для конкретного документа
    #plsa