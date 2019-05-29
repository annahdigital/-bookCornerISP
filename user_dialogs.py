from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore


class FavAuthors(QtWidgets.QDialog):
    def __init__(self, appInfo):
        super(FavAuthors, self).__init__()
        loadUi('add_fav_authors.ui', self)
        self.initialize(appInfo)
        self.pushButton_5.clicked.connect(lambda: self.add(appInfo))

    @pyqtSlot()
    def add(self, appInfo):
        if self.listWidget.currentItem():
            author = appInfo.library.return_author_by_name(self.listWidget.currentItem().text())
            if author not in appInfo.find_user_by_name(appInfo.current_user).library.author_list:
                appInfo.find_user_by_name(appInfo.current_user).library.author_list.append(author)
                this_user = appInfo.find_user_by_name(appInfo.current_user)
                books = appInfo.users_database.find_one({"name": appInfo.current_user})["books"]
                authors = appInfo.users_database.find_one({"name": appInfo.current_user})["authors"]
                authors.append(self.listWidget.currentItem().text())
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
        self.listWidget.clear()
        for author in appInfo.library.author_list:
            if author not in appInfo.find_user_by_name(appInfo.current_user).library.author_list:
                self.listWidget.addItem(author.name)


class FavBook(QtWidgets.QDialog):
    def __init__(self, appInfo):
        super(FavBook, self).__init__()
        loadUi('add_fav_books.ui', self)
        self.tableWidget.setColumnCount(2)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.initialize(appInfo)

        self.pushButton_5.clicked.connect(lambda: self.add(appInfo))

    @pyqtSlot()
    def initialize(self, appInfo):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(("Name", "Author"))
        counter = 0
        for book in appInfo.library.book_list:
            if book not in appInfo.find_user_by_name(appInfo.current_user).library.book_list:
                counter += 1
        self.tableWidget.setRowCount(counter)
        row = 0
        for book in appInfo.library.book_list:
            if book not in appInfo.find_user_by_name(appInfo.current_user).library.book_list:
                item = QtWidgets.QTableWidgetItem(book.name)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row, 0, item)
                item = QtWidgets.QTableWidgetItem(book.author)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row, 1, item)
                row += 1

    @pyqtSlot()
    def add(self, appInfo):
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
                self.initialize(appInfo)


class FavTags(QtWidgets.QDialog):
    def __init__(self, appInfo):
        super(FavTags, self).__init__()
        loadUi('add_fav_authors.ui', self)
        self.label.setText("Tags")
        self.initialize(appInfo)
        self.pushButton_5.clicked.connect(lambda: self.add(appInfo))

    @pyqtSlot()
    def initialize(self, appInfo):
        self.listWidget.clear()
        for tag in appInfo.library.tag_list():
            if tag not in  appInfo.find_user_by_name(appInfo.current_user).tags:
                self.listWidget.addItem(tag)

    @pyqtSlot()
    def add(self, appInfo):
        if self.listWidget.currentItem():
            if self.listWidget.currentItem().text() not in appInfo.find_user_by_name(appInfo.current_user).tags:
                appInfo.find_user_by_name(appInfo.current_user).tags.append(self.listWidget.currentItem().text())
                this_user = appInfo.find_user_by_name(appInfo.current_user)
                books = appInfo.users_database.find_one({"name": appInfo.current_user})["books"]
                authors = appInfo.users_database.find_one({"name": appInfo.current_user})["authors"]
                tags = appInfo.users_database.find_one({"name": appInfo.current_user})["tags"]
                tags.append(self.listWidget.currentItem().text())
                genres = appInfo.users_database.find_one({"name": appInfo.current_user})["genres"]
                appInfo.users_database.update({"name": appInfo.current_user}, {"name": appInfo.current_user,
                                                                               "password": this_user.password,
                                                                               "moderation": this_user.moderation,
                                                                               "books": books, "authors": authors,
                                                                               "tags": tags, "genres": genres})
                self.initialize(appInfo)


class FavGenres(QtWidgets.QDialog):
    def __init__(self, appInfo):
        super(FavGenres, self).__init__()
        loadUi('add_fav_authors.ui', self)
        self.label.setText("Genres")
        self.initialize(appInfo)
        self.pushButton_5.clicked.connect(lambda: self.add(appInfo))

    @pyqtSlot()
    def initialize(self, appInfo):
        self.listWidget.clear()
        for genre in appInfo.library.genre_list():
            if genre not in appInfo.find_user_by_name(appInfo.current_user).genres:
                self.listWidget.addItem(genre)

    @pyqtSlot()
    def add(self, appInfo):
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
                self.initialize(appInfo)


class MyGenres(QtWidgets.QDialog):
    def __init__(self, appInfo):
        super(MyGenres, self).__init__()
        loadUi('add_fav_authors1.ui', self)
        self.label.setText("Genres")
        self.listWidget.addItems(appInfo.find_user_by_name(appInfo.current_user).genres)
        self.pushButton_5.clicked.connect(lambda: self.add(appInfo))
        self.pushButton_6.clicked.connect(lambda: self.delete(appInfo))

    @pyqtSlot()
    def delete(self, appInfo):
        if self.listWidget.currentItem():
            appInfo.find_user_by_name(appInfo.current_user).genres.remove(self.listWidget.currentItem().text())
            this_user = appInfo.find_user_by_name(appInfo.current_user)
            books = appInfo.users_database.find_one({"name": appInfo.current_user})["books"]
            authors = appInfo.users_database.find_one({"name": appInfo.current_user})["authors"]
            tags = appInfo.users_database.find_one({"name": appInfo.current_user})["tags"]
            genres = appInfo.users_database.find_one({"name": appInfo.current_user})["genres"]
            genres.remove(self.listWidget.currentItem().text())
            appInfo.users_database.update({"name": appInfo.current_user}, {"name": appInfo.current_user,
                                                                           "password": this_user.password,
                                                                           "moderation": this_user.moderation,
                                                                           "books": books, "authors": authors,
                                                                           "tags": tags, "genres": genres})
            self.listWidget.clear()
            self.listWidget.addItems(appInfo.find_user_by_name(appInfo.current_user).genres)

    @pyqtSlot()
    def add(self, appInfo):
        dialog = FavGenres(appInfo)
        dialog.exec_()
        self.listWidget.clear()
        self.listWidget.addItems(appInfo.find_user_by_name(appInfo.current_user).genres)


class MyTags(QtWidgets.QDialog):
    def __init__(self, appInfo):
        super(MyTags, self).__init__()
        loadUi('add_fav_authors1.ui', self)
        self.label.setText("Tags")
        self.listWidget.addItems(appInfo.find_user_by_name(appInfo.current_user).tags)
        self.pushButton_5.clicked.connect(lambda: self.add(appInfo))
        self.pushButton_6.clicked.connect(lambda: self.delete(appInfo))

    @pyqtSlot()
    def delete(self, appInfo):
        if self.listWidget.currentItem():
            appInfo.find_user_by_name(appInfo.current_user).tags.remove(self.listWidget.currentItem().text())
            this_user = appInfo.find_user_by_name(appInfo.current_user)
            books = appInfo.users_database.find_one({"name": appInfo.current_user})["books"]
            authors = appInfo.users_database.find_one({"name": appInfo.current_user})["authors"]
            tags = appInfo.users_database.find_one({"name": appInfo.current_user})["tags"]
            genres = appInfo.users_database.find_one({"name": appInfo.current_user})["genres"]
            tags.remove(self.listWidget.currentItem().text())
            appInfo.users_database.update({"name": appInfo.current_user}, {"name": appInfo.current_user,
                                                                           "password": this_user.password,
                                                                           "moderation": this_user.moderation,
                                                                           "books": books, "authors": authors,
                                                                           "tags": tags, "genres": genres})
            self.listWidget.clear()
            self.listWidget.addItems(appInfo.find_user_by_name(appInfo.current_user).tags)

    @pyqtSlot()
    def add(self, appInfo):
        dialog = FavTags(appInfo)
        dialog.exec_()
        self.listWidget.clear()
        self.listWidget.addItems(appInfo.find_user_by_name(appInfo.current_user).tags)


class UserModeration(QtWidgets.QDialog):
    def __init__(self, appInfo):
        super(UserModeration, self).__init__()
        loadUi('user_moderation.ui', self)
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(("Name", "Moderation"))
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.setRowCount(len(appInfo.users))
        row = 0
        for user in appInfo.users:
            item = QtWidgets.QTableWidgetItem(user.name)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(row, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            if user.moderation:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget.setItem(row, 1, item)
            row += 1
        self.pushButton_4.clicked.connect(lambda: self.save(appInfo))

    @pyqtSlot()
    def save(self, appInfo):
        all_rows = self.tableWidget.rowCount()
        for row in range(all_rows):
            if self.tableWidget.item(row, 0):
                name = self.tableWidget.item(row, 0).text()
                if self.tableWidget.item(row, 1).checkState() == QtCore.Qt.Checked:
                    moderation = True
                else:
                    moderation = False
                appInfo.find_user_by_name(name).change_status(moderation)
                books = appInfo.users_database.find_one({"name": name})["books"]
                authors = appInfo.users_database.find_one({"name": name})["authors"]
                tags = appInfo.users_database.find_one({"name": name})["tags"]
                genres = appInfo.users_database.find_one({"name": name})["genres"]
                appInfo.users_database.update({"name": name}, {"name": name,
                                                                               "password": appInfo.find_user_by_name(name).password,
                                                                               "moderation": moderation,
                                                                               "books": books, "authors": authors,
                                                                               "tags": tags, "genres": genres})


class DescriptionDialog(QtWidgets.QDialog):
    def __init__(self, description):
        super(DescriptionDialog, self).__init__()
        loadUi('description.ui', self)
        self.plainTextEdit.setPlainText(description)
        self.plainTextEdit.setWordWrapMode(True)
        self.pushButton_5.clicked.connect(lambda: self.close())

