from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from user import User
from book import Book
from author import Author


# NEW USER OR ERROR  NEW USER OR ERROR  NEW USER OR ERROR  NEW USER OR ERROR  NEW USER OR ERROR  NEW USER OR ERROR
class UserWindow(QtWidgets.QDialog):
    def __init__(self, name, password, appInfo):
        super(UserWindow, self).__init__()
        loadUi('new_user_login_dialog.ui', self)
        self.pushButton.clicked.connect(lambda: self.add_user(name, password, appInfo))
        self.pushButton_2.clicked.connect(self.closing)

    @pyqtSlot()
    def add_user(self, name, password, appInfo):
        this_user = User(name, password)
        appInfo.users.append(this_user)
        appInfo.current_user = name
        appInfo.users_database.insert_one({"name": name, "password": password, "moderation": False, "books": [], "authors": [], "tags": [], "genres": []})
        self.close()

    @pyqtSlot()
    def closing(self):
        self.close()


# ERROR WHILE ENTERING PASSWORD  ERROR WHILE ENTERING PASSWORD  ERROR WHILE ENTERING PASSWORD  ERROR WHILE ENTERING
class ErrorDialog(QtWidgets.QDialog):
    def __init__(self):
        super(ErrorDialog, self).__init__()
        loadUi('input_login_dialog.ui', self)
        self.pushButton_2.clicked.connect(self.closing)

    @pyqtSlot()
    def closing(self):
        self.close()


# CHANGE PASSWORD  CHANGE PASSWORD  CHANGE PASSWORD  CHANGE PASSWORD  CHANGE PASSWORD  CHANGE PASSWORD  CHANGE PASSWORD
class ChangePasswordDialod(QtWidgets.QDialog):
    def __init__(self, appInfo):
        super(ChangePasswordDialod, self).__init__()
        loadUi('changing_password.ui', self)
        self.pushButton_2.clicked.connect(self.closing)
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton_3.clicked.connect(lambda: self.changing(appInfo))

    @pyqtSlot()
    def closing(self):
        self.close()

    @pyqtSlot()
    def changing(self, appInfo):
        old_password = self.lineEdit.text()
        new_password = self.lineEdit_2.text()
        if new_password != self.lineEdit_3.text():
            message = ErrorDialog()
            message.label_2.setText("Passwords don't match.")
            message.exec_()
        else:
            if not appInfo.find_user_by_name(appInfo.current_user).change_password(old_password, new_password):
                message = ErrorDialog()
                message.exec_()
            else:
                this_user = appInfo.find_user_by_name(appInfo.current_user)
                books = appInfo.users_database.find_one({"name": appInfo.current_user})["books"]
                authors = appInfo.users_database.find_one({"name": appInfo.current_user})["authors"]
                tags = appInfo.users_database.find_one({"name": appInfo.current_user})["tags"]
                genres = appInfo.users_database.find_one({"name": appInfo.current_user})["genres"]
                appInfo.users_database.update({"name": appInfo.current_user}, {"name": appInfo.current_user,
                                                                               "password": new_password,
                                                                               "moderation": this_user.moderation,
                                                                               "books": books, "authors": authors,
                                                                               "tags": tags, "genres": genres})
                self.close()


# CHANGE USER  CHANGE USER  CHANGE USER  CHANGE USER  CHANGE USER  CHANGE USER  CHANGE USER  CHANGE USER  CHANGE USER
class ChangingUserMenu(QtWidgets.QDialog):
    def __init__(self, appInfo, changing_rights=False):
        super(ChangingUserMenu, self).__init__()
        loadUi('change_user_dialog.ui', self)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton_2.clicked.connect(self.closing)
        if not changing_rights:
            self.pushButton_3.clicked.connect(lambda: self.change(appInfo))
        else:
            pass
            # self.pushButton_3.clicked.connect(lambda: self.rights_page(appInfo))

    @pyqtSlot()
    def closing(self):
        self.close()

    @pyqtSlot()
    def change(self, appInfo):
        name = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if name and password:
            if not appInfo.find_user_by_name(name):
                user_window = UserWindow(name, password, appInfo)
                user_window.exec_()
            else:
                if not appInfo.find_user_by_name(name).validation(password):
                    user_window = ErrorDialog()
                    user_window.exec_()
                else:
                    appInfo.current_user = name
                    self.close()


# ADD A BOOK  ADD A BOOK ADD A BOOK ADD A BOOK ADD A BOOK ADD A BOOK ADD A BOOK ADD A BOOK ADD A BOOK ADD A BOOK
class AddingBookMenu(QtWidgets.QDialog):
    def __init__(self, appInfo):
        super(AddingBookMenu, self).__init__()
        loadUi('adding_book.ui', self)
        this_book = Book()
        self.pushButton_8.clicked.connect(self.closing)
        self.pushButton_7.clicked.connect(lambda: self.adding(appInfo, this_book))
        self.pushButton_6.clicked.connect(lambda: self.adding_genre(this_book))
        self.pushButton_5.clicked.connect(lambda: self.adding_tag(this_book))
        self.pushButton_10.clicked.connect(lambda: self.delete_tag(this_book))
        self.pushButton_11.clicked.connect(lambda: self.delete_genre(this_book))
        self.update_tables(this_book)

    def update_tables(self, this_book):
        self.listWidget_2.clear()
        self.listWidget_3.clear()
        for tag in this_book.tag_list:
            self.listWidget_2.addItem(tag)
        for genre in this_book.genre_list:
            self.listWidget_3.addItem(genre)

    @pyqtSlot()
    def closing(self):
        self.close()

    @pyqtSlot()
    def delete_genre(self, this_book):
        if self.listWidget_3.currentItem():
            this_book.delete_genre(self.listWidget_3.currentItem().text())
        self.update_tables(this_book)

    @pyqtSlot()
    def delete_tag(self, this_book):
        if self.listWidget_2.currentItem():
            this_book.delete_tag(self.listWidget_2.currentItem().text())
        self.update_tables(this_book)

    @pyqtSlot()
    def adding_tag(self, this_book):
        if self.lineEdit_4.text():
            tag = self.lineEdit_4.text()
            self.lineEdit_4.setText("")
            if tag not in this_book.tag_list:
                this_book.tag_list.append(tag)
        self.update_tables(this_book)

    @pyqtSlot()
    def adding_genre(self, this_book):
        if self.lineEdit_5.text():
            genre = self.lineEdit_5.text()
            self.lineEdit_5.setText("")
            if genre not in this_book.genre_list:
                this_book.genre_list.append(genre)
        self.update_tables(this_book)

    @pyqtSlot()
    def adding(self, appInfo, this_book):
        if self.lineEdit.text() and self.lineEdit_2.text():
            valid = True
            if self.lineEdit_3.text():
                try:
                    int(self.lineEdit_3.text())
                except ValueError:
                    message = ErrorDialog()
                    message.label_2.setText("Year must be a digit!.")
                    message.exec_()
                    valid = False
            if valid:
                this_book.set_name(self.lineEdit.text())
                this_book.set_author(self.lineEdit_2.text())
                author = Author(self.lineEdit_2.text())
                if author not in appInfo.library.author_list:
                    author.book_list.append(this_book.name)
                    appInfo.library.add_author_object(author)
                    message = CreateAnAuthor(appInfo, this_book)
                    message.exec_()
                if self.textEdit.toPlainText():
                    this_book.set_description(self.textEdit.toPlainText())
                else:
                    this_book.set_description("Description unknown.")
                if self.lineEdit_3.text():
                    this_book.set_year(self.lineEdit_3.text())
                else:
                    this_book.set_year(0)
                if not appInfo.library.add_book_object(this_book):
                    message = ErrorDialog()
                    message.label_2.setText("This book already exists.")
                    message.exec_()
                else:
                    appInfo.books_database.insert_one({"name": this_book.name, "author": this_book.author,
                                                       "year": this_book.year, "description": this_book.description,
                                                       "tags": this_book.tag_list, "genres": this_book.genre_list})
                    self.close()


# EDIT BOOK  EDIT BOOK  EDIT BOOK  EDIT BOOK  EDIT BOOK  EDIT BOOK  EDIT BOOK  EDIT BOOK  EDIT BOOK  EDIT BOOK
class EditingBookMenu(QtWidgets.QDialog):
    def __init__(self, appInfo, book):
        super(EditingBookMenu, self).__init__()
        loadUi('adding_book.ui', self)
        self.lineEdit.setText(book.name)
        self.lineEdit_2.setText(book.author)
        self.lineEdit_3.setText(str(book.year))
        self.textEdit.setText(book.description)
        self.pushButton_8.clicked.connect(self.closing)
        self.pushButton_10.clicked.connect(lambda: self.delete_tag(this_book))
        self.pushButton_11.clicked.connect(lambda: self.delete_genre(this_book))
        appInfo.library.delete_book(book.name)
        this_book = Book()
        for tag in book.tag_list:
            this_book.add_tag(tag)
        for genre in book.genre_list:
            this_book.add_genre(genre)
        self.pushButton_7.clicked.connect(lambda: self.adding(appInfo, this_book, book.name))
        self.pushButton_6.clicked.connect(lambda: self.adding_genre(this_book))
        self.pushButton_5.clicked.connect(lambda: self.adding_tag(this_book))
        self.update_tables(this_book)

    def update_tables(self, this_book):
        self.listWidget_2.clear()
        self.listWidget_3.clear()
        for tag in this_book.tag_list:
            self.listWidget_2.addItem(tag)
        for genre in this_book.genre_list:
            self.listWidget_3.addItem(genre)

    @pyqtSlot()
    def delete_genre(self, this_book):
        if self.listWidget_3.currentItem():
            this_book.delete_genre(self.listWidget_3.currentItem().text())
        self.update_tables(this_book)

    @pyqtSlot()
    def delete_tag(self, this_book):
        if self.listWidget_2.currentItem():
            this_book.delete_tag(self.listWidget_2.currentItem().text())
        self.update_tables(this_book)

    @pyqtSlot()
    def closing(self):
        self.close()

    @pyqtSlot()
    def adding(self, appInfo, this_book, book_name):
        if self.lineEdit.text() and self.lineEdit_2.text():
            valid = True
            if self.lineEdit_3.text():
                try:
                    int(self.lineEdit_3.text())
                except ValueError:
                    message = ErrorDialog()
                    message.label_2.setText("Year must be a digit!.")
                    message.exec_()
                    valid = False
            if valid:
                this_book.set_name(self.lineEdit.text())
                this_book.set_author(self.lineEdit_2.text())
                author = Author(self.lineEdit_2.text())
                if author not in appInfo.library.author_list:
                    author.book_list.append(this_book.name)
                    appInfo.library.add_author_object(author)
                    message = CreateAnAuthor(appInfo, this_book)
                    message.exec_()
                if self.textEdit.toPlainText():
                    this_book.set_description(self.textEdit.toPlainText())
                else:
                    this_book.set_description("Description unknown.")
                if self.lineEdit_3.text():
                    this_book.set_year(self.lineEdit_3.text())
                else:
                    this_book.set_year(0)
                if not appInfo.library.add_book_object(this_book):
                    message = ErrorDialog()
                    message.label_2.setText("This book already exists.")
                    message.exec_()
                else:
                    appInfo.books_database.update({"name": book_name}, {"name": this_book.name, "author": this_book.author,
                                                       "year": this_book.year, "description": this_book.description,
                                                       "tags": this_book.tag_list, "genres": this_book.genre_list})
                    self.close()

    @pyqtSlot()
    def adding_tag(self, this_book):
        if self.lineEdit_4.text():
            tag = self.lineEdit_4.text()
            self.lineEdit_4.setText("")
            if tag not in this_book.tag_list:
                this_book.tag_list.append(tag)
        self.update_tables(this_book)

    @pyqtSlot()
    def adding_genre(self, this_book):
        if self.lineEdit_5.text():
            genre = self.lineEdit_5.text()
            self.lineEdit_5.setText("")
            if genre not in this_book.genre_list:
                this_book.genre_list.append(genre)
        self.update_tables(this_book)


# ADD AUTHOR ADD AUTHOR ADD AUTHOR ADD AUTHOR ADD AUTHOR ADD AUTHOR ADD AUTHOR ADD AUTHOR ADD AUTHOR ADD AUTHOR ADD
class AddingAuthorMenu(QtWidgets.QDialog):
    def __init__(self, appInfo):
        super(AddingAuthorMenu, self).__init__()
        loadUi('adding_author.ui', self)
        this_author = Author()
        self.pushButton_8.clicked.connect(self.closing)
        self.pushButton_9.clicked.connect(lambda: self.adding(appInfo, this_author))
        self.pushButton_5.clicked.connect(lambda: self.adding_book(this_author, appInfo))
        self.pushButton_6.clicked.connect(lambda: self.adding_genre(this_author))
        self.pushButton_10.clicked.connect(lambda: self.delete_book(this_author, appInfo))
        self.pushButton_11.clicked.connect(lambda: self.delete_genre(this_author))
        self.update_tables(this_author)

    def update_tables(self, this_author):
        self.listWidget_2.clear()
        self.listWidget.clear()
        for genre in this_author.genre_list:
            self.listWidget_2.addItem(genre)
        for book in this_author.book_list:
            self.listWidget.addItem(book)

    @pyqtSlot()
    def closing(self):
        self.close()

    @pyqtSlot()
    def delete_book(self, this_author, appInfo):
        if self.listWidget.currentItem():
            this_author.delete_book(self.listWidget.currentItem().text())
            appInfo.library.delete_book(self.listWidget.currentItem().text())
        self.update_tables(this_author)

    @pyqtSlot()
    def delete_genre(self, this_author):
        if self.listWidget_2.currentItem():
            this_author.delete_genre(self.listWidget_2.currentItem().text())
        self.update_tables(this_author)

    @pyqtSlot()
    def adding_book(self, this_author, appInfo):
        if self.lineEdit_4.text():
            if self.lineEdit.text():
                book = self.lineEdit_4.text()
                self.lineEdit_4.setText("")
                if book not in this_author.book_list:
                    this_author.book_list.append(book)
                this_book = Book(book, self.lineEdit.text())
                if this_book not in appInfo.library.book_list:
                    appInfo.library.add_book_object(this_book)
                    message = CreateABook(appInfo, this_book)
                    message.exec_()
            else:
                message = ErrorDialog()
                message.label_2.setText("Enter a name first.")
                message.exec_()
        self.update_tables(this_author)

    @pyqtSlot()
    def adding_genre(self, this_author):
        if self.lineEdit_5.text():
            genre = self.lineEdit_5.text()
            self.lineEdit_5.setText("")
            if genre not in this_author.genre_list:
                this_author.genre_list.append(genre)
        self.update_tables(this_author)

    @pyqtSlot()
    def adding(self, appInfo, this_author):
        if self.lineEdit.text():
            valid = True
            if self.lineEdit_3.text():
                try:
                    int(self.lineEdit_3.text())
                except ValueError:
                    message = ErrorDialog()
                    message.label_2.setText("Year must be a digit!.")
                    message.exec_()
                    valid = False
            if self.lineEdit_2.text():
                try:
                    int(self.lineEdit_2.text())
                except ValueError:
                    message = ErrorDialog()
                    message.label_2.setText("Year must be a digit!.")
                    message.exec_()
                    valid = False
            if valid:
                this_author.set_name(self.lineEdit.text())
                if self.textEdit.toPlainText():
                    this_author.set_description(self.textEdit.toPlainText())
                else:
                    this_author.set_description("Description unknown.")
                if self.lineEdit_2.text():
                    this_author.set_birth_year(self.lineEdit_2.text())
                else:
                    this_author.set_birth_year(0)
                if self.lineEdit_3.text():
                    this_author.set_death_year(self.lineEdit_3.text())
                else:
                    this_author.set_death_year(0)
                if not appInfo.library.add_author_object(this_author):
                    message = ErrorDialog()
                    message.label_2.setText("This author already exists.")
                    message.exec_()
                else:
                    appInfo.authors_database.insert_one({"name": this_author.name, "birth_year": this_author.birth_year,
                                                       "death_year": this_author.death_year,
                                                       "description": this_author.description,
                                                       "books": this_author.book_list, "genres": this_author.genre_list})
                    self.close()


# EDIT AUTHOR  EDIT AUTHOR  EDIT AUTHOR  EDIT AUTHOR  EDIT AUTHOR  EDIT AUTHOR  EDIT AUTHOR  EDIT AUTHOR  EDIT AUTHOR
class EditingAuthorMenu(QtWidgets.QDialog):
    def __init__(self, appInfo, author):
        super(EditingAuthorMenu, self).__init__()
        loadUi('adding_author.ui', self)
        this_author = Author()
        for book in author.book_list:
            this_author.add_book(book)
        for genre in author.genre_list:
            this_author.add_genre(genre)
        appInfo.library.delete_author(author.name)
        self.lineEdit.setText(author.name)
        self.lineEdit_2.setText(str(author.birth_year))
        self.lineEdit_3.setText(str(author.death_year))
        self.textEdit.setText(author.description)
        self.pushButton_8.clicked.connect(self.closing)
        self.pushButton_9.clicked.connect(lambda: self.adding(appInfo, this_author, author.name))
        self.pushButton_5.clicked.connect(lambda: self.adding_book(this_author, appInfo))
        self.pushButton_6.clicked.connect(lambda: self.adding_genre(this_author))
        self.pushButton_10.clicked.connect(lambda: self.delete_book(this_author))
        self.pushButton_11.clicked.connect(lambda: self.delete_genre(this_author))
        self.update_tables(this_author)

    def update_tables(self, this_author):
        self.listWidget_2.clear()
        self.listWidget.clear()
        for genre in this_author.genre_list:
            self.listWidget_2.addItem(genre)
        for book in this_author.book_list:
            self.listWidget.addItem(book)

    @pyqtSlot()
    def closing(self):
        self.close()

    @pyqtSlot()
    def delete_book(self, this_author):
        if self.listWidget.currentItem():
            this_author.delete_book(self.listWidget.currentItem().text())
        self.update_tables(this_author)

    @pyqtSlot()
    def delete_genre(self, this_author):
        if self.listWidget_2.currentItem():
            this_author.delete_genre(self.listWidget_2.currentItem().text())
        self.update_tables(this_author)

    @pyqtSlot()
    def adding_book(self, this_author, appInfo):
        if self.lineEdit_4.text():
            if self.lineEdit.text():
                book = self.lineEdit_4.text()
                self.lineEdit_4.setText("")
                if book not in this_author.book_list:
                    this_author.book_list.append(book)
                this_book = Book(book, self.lineEdit.text())
                if this_book not in appInfo.library.book_list:
                    appInfo.library.add_book_object(this_book)
                    appInfo.books_database.insert_one({"name": this_book.name, "author": this_book.author,
                                                       "year": this_book.year, "description": this_book.description,
                                                       "tags": this_book.tag_list, "genres": this_book.genre_list})
                    message = CreateABook(appInfo, this_book)
                    message.exec_()
            else:
                message = ErrorDialog()
                message.label_2.setText("Enter a name first.")
                message.exec_()
        self.update_tables(this_author)

    @pyqtSlot()
    def adding_genre(self, this_author):
        if self.lineEdit_5.text():
            genre = self.lineEdit_5.text()
            self.lineEdit_5.setText("")
            if genre not in this_author.genre_list:
                this_author.genre_list.append(genre)
        self.update_tables(this_author)

    @pyqtSlot()
    def adding(self, appInfo, this_author, author_name):
        if self.lineEdit.text():
            valid = True
            if self.lineEdit_3.text():
                try:
                    int(self.lineEdit_3.text())
                except ValueError:
                    message = ErrorDialog()
                    message.label_2.setText("Year must be a digit!.")
                    message.exec_()
                    valid = False
            if self.lineEdit_2.text():
                try:
                    int(self.lineEdit_2.text())
                except ValueError:
                    message = ErrorDialog()
                    message.label_2.setText("Year must be a digit!.")
                    message.exec_()
                    valid = False
            if valid:
                this_author.set_name(self.lineEdit.text())
                if self.textEdit.toPlainText():
                    this_author.set_description(self.textEdit.toPlainText())
                else:
                    this_author.set_description("Description unknown.")
                if self.lineEdit_2.text():
                    this_author.set_birth_year(self.lineEdit_2.text())
                else:
                    this_author.set_birth_year(0)
                if self.lineEdit_3.text():
                    this_author.set_death_year(self.lineEdit_3.text())
                else:
                    this_author.set_death_year(0)
                if not appInfo.library.add_author_object(this_author):
                    message = ErrorDialog()
                    message.label_2.setText("This author already exists.")
                    message.exec_()
                else:
                    appInfo.authors_database.update({"name": author_name}, {"name": this_author.name, "birth_year": this_author.birth_year,
                                                       "death_year": this_author.death_year,
                                                       "description": this_author.description,
                                                       "books": this_author.book_list, "genres": this_author.genre_list})
                    self.close()


# CREATE A BOOK DIALOG  CREATE A BOOK DIALOG  CREATE A BOOK DIALOG  CREATE A BOOK DIALOG  CREATE A BOOK DIALOG
class CreateABook(QtWidgets.QDialog):
    def __init__(self, appInfo, book):
        super(CreateABook, self).__init__()
        loadUi('add_more_info.ui', self)
        self.pushButton_2.clicked.connect(self.later)
        self.pushButton.clicked.connect(lambda: self.add_new_book(appInfo, book))

    @pyqtSlot()
    def later(self):
        self.close()

    @pyqtSlot()
    def add_new_book(self, appInfo, book):
        new_window = EditingBookMenu(appInfo, book)
        new_window.exec_()
        self.close()


# CREATE AN AUTHOR  CREATE AN AUTHOR  CREATE AN AUTHOR  CREATE AN AUTHOR  CREATE AN AUTHOR  CREATE AN AUTHOR
class CreateAnAuthor(QtWidgets.QDialog):
    def __init__(self, appInfo, book):
        super(CreateAnAuthor, self).__init__()
        loadUi('add_more_info.ui', self)
        self.label.setText("It's a new author in our library!")
        self.pushButton_2.clicked.connect(self.later)
        self.pushButton.clicked.connect(lambda: self.add_new_author(appInfo, book))

    @pyqtSlot()
    def later(self):
        self.close()

    @pyqtSlot()
    def add_new_author(self, appInfo, book):
        author = Author(book.author)
        book_list = [book.name]
        appInfo.authors_database.insert_one({"name": book.author, "birth_year": 0,
                                             "death_year": 0,
                                             "description": '',
                                             "books": book_list, "genres": book.genre_list})
        author.add_book(book.name)
        new_window = EditingAuthorMenu(appInfo, author)
        new_window.exec_()
        self.close()


# GENRES  GENRES  GENRES  GENRES  GENRES  GENRES  GENRES  GENRES  GENRES  GENRES  GENRES  GENRES  GENRES  GENRES
class GenresMenu(QtWidgets.QDialog):
    def __init__(self, appInfo):
        super(GenresMenu, self).__init__()
        loadUi('genres.ui', self)
        genre_list = appInfo.library.genre_list()
        self.listWidget.addItems(genre_list)
        self.pushButton_11.clicked.connect(lambda: self.add_to_fav(appInfo))

    @pyqtSlot()
    def add_to_fav(self, appInfo):
        if self.listWidget.currentItem():
            if self.listWidget.currentItem().text() not in appInfo.find_user_by_name(appInfo.current_user).genres:
                appInfo.find_user_by_name(appInfo.current_user).genres.append(self.listWidget.currentItem().text())
                this_user = appInfo.find_user_by_name(appInfo.current_user)
                books = appInfo.users_database.find_one({"name": appInfo.current_user})["books"]
                authors = appInfo.users_database.find_one({"name": appInfo.current_user})["authors"]
                tags = appInfo.users_database.find_one({"name": appInfo.current_user})["tags"]
                genres = appInfo.users_database.find_one({"name": appInfo.current_user})["genres"]
                genres.append(self.listWidget.currentItem().text())
                appInfo.users_database.update({"name": appInfo.current_user}, {"name": appInfo.current_user,
                                                                               "password": this_user.password,
                                                                               "moderation": this_user.moderation,
                                                                               "books": books, "authors": authors,
                                                                               "tags": tags, "genres": genres})


# TAGS TAGS TAGS TAGS
class TagsMenu(QtWidgets.QDialog):
    def __init__(self, appInfo):
        super(TagsMenu, self).__init__()
        loadUi('genres.ui', self)
        self.label_6.setText("Tags")
        tag_list = appInfo.library.tag_list()
        self.listWidget.addItems(tag_list)
        self.pushButton_11.clicked.connect(lambda: self.add_to_fav(appInfo))

    @pyqtSlot()
    def add_to_fav(self, appInfo):
        if self.listWidget.currentItem():
            if self.listWidget.currentItem().text() not in appInfo.find_user_by_name(appInfo.current_user).tags:
                appInfo.find_user_by_name(appInfo.current_user).tags.append(self.listWidget.currentItem().text())
                this_user = appInfo.find_user_by_name(appInfo.current_user)
                books = appInfo.users_database.find_one({"name": appInfo.current_user})["books"]
                authors = appInfo.users_database.find_one({"name": appInfo.current_user})["authors"]
                tags = appInfo.users_database.find_one({"name": appInfo.current_user})["tags"]
                genres = appInfo.users_database.find_one({"name": appInfo.current_user})["genres"]
                tags.append(self.listWidget.currentItem().text())
                appInfo.users_database.update({"name": appInfo.current_user}, {"name": appInfo.current_user,
                                                                               "password": this_user.password,
                                                                               "moderation": this_user.moderation,
                                                                               "books": books, "authors": authors,
                                                                               "tags": tags, "genres": genres})








