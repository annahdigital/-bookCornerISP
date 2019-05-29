#!/usr/bin/env python3
from consoleApp import ConsoleApp


if __name__ == "__main__":
    app = ConsoleApp()

    def printing():
        print(app.library)

    def exiting():
        exit(0)

    action_dictionary = {'1': app.adding_book_menu, "2": app.adding_author_menu,
                         "3": app.deleting_book_menu, "4": app.deleting_author_menu,
                         "5": app.editing_book_menu, "6": app.editing_author_menu,
                         "7": app.book_info_menu, "8": app.author_info_menu,
                         "9": printing, "10": app.tag_searching_menu,
                         "11": app.genre_searching_menu, "12": app.change_user,
                         "13": app.add_favourite_books, "14": app.add_favourite_authors, "15": app.add_favourite_tags,
                         "16": app.add_favourite_genres, "17": app.user_preferences,
                         "18": app.delete_user, "19": app.change_user_status, "20": exiting}
    s = "What do you wanna do? \n1. Add a book. \n2. Add an author. \n3. Delete a book. \n4. Delete an author. \n"
    s += "5. Edit a book. \n6. Edit an author. \n7. Get information about a book. \n"
    s += "8. Get information about an author.\n9. View all the information,\n10. Search by tag.\n"
    s += "11, Search by genre. \n12. Change user.\n13. Add favourite books.\n14. Add favourite authors.\n"
    s += "15. Add favourite tags.\n16. Add favourite genres.\n17. Get information about my preferences.\n"
    s += "18. Delete user. \n19. Change user status. \n20. Exit.\n"
    while True:
        char = input(s)
        try:
            action = action_dictionary[char]()
        except KeyError as e:
            raise ValueError('Undefined unit: {}'.format(e.args[0]))
            exit(1)
        print("_________________________________________________________________________")

#  машинное обучение: определение жанров и тегов по описанию книги
# заменить кей на пассворд
# уникальные айди книги, автора, айди для админа и для обычного юзера