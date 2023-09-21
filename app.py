"""
A console program : 

"""

from models import (Base, session,
                    Book, engine)
import csv
import datetime
import time


def main_menu():
    while True:

        print("""
            
            \nPROGRAMMING BOOKS
            \r1) Add book
            \r2) View all books
            \r3) Search for a book
            \r4) Book Analysis
            \r5) Exit

            """)
        choice = input("What would you like to do ? ")
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            choice = input("""
                        \rPlease choose one of the options above.
                        \rA number from 1 to 5.
                        \rPress enter to try again. """)


def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')

    try:
        month = months.index(split_date[0]) + 1
        day = int(split_date[1][:-1])
        year = int(split_date[2])
        date = datetime.date(year, month, day)
    except ValueError:
        input('''
            \n******* DATE ERROR *********
            \rThe date format should include a valid Month Day, Year from the past. 
            \rEx: January 13, 2003
            \rPress enter to try again
            \r************************''')
        return
    else:
        return date


def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        input('''
            \n******* PRICE ERROR *****
            \rThe price should be a number without a currency symbol. 
            \rEx: 10.99
            \rPress enter to try again
            \r*********************''')
        return
    else:
        return int(price_float * 100)


def add_csv():
    # open file
    with open('./suggested_books.csv') as csv_file:
        # Create reader object by passing the file object to reader method
        data = csv.reader(csv_file)
        # Iterate over each row in the csv
        # file using reader object
        for row in data:
            # avoid duplicate books
            book_in_db = session.query(Book).filter(
                Book.title == row[0]).one_or_none()
            if book_in_db == None:
                new_book = Book(
                    title=row[0],
                    author=row[1],
                    published_date=clean_date(row[2]),
                    price=clean_price(row[3]))
                session.add(new_book)
        session.commit()


def add_book():
    print("Add a New Book")
    title = input("Book title: ")
    author = input("Author: ")

    date_error = True
    while date_error:
        date = input("Published Date (Example: January 13, 2023): ")
        date = clean_date(date)
        if type(date) == datetime.date:
            date_error = False

    price_error = True
    while price_error:
        price = clean_price(input("Price (Example: 10.99): "))
        if type(price) == int:
            price_error = False

    new_book = Book(title=title,
                    author=author,
                    published_date=date,
                    price=price)
    session.add(new_book)
    session.commit()
    print("Book added!")
    time.sleep(1.5)


def view_books():
    for book in session.query(Book):
        print(f"{book.id} | {book.title} | {book.author}")
    input('\nPress enter to return to the main menu.')


def app():
    app_running = True
    while app_running:
        choice = main_menu()
        match choice:
            case '1':
                add_book()
            case '2':
                view_books()
            case '3':
                # search book
                pass
            case '4':
                # analysis
                pass
            case _:
                print("GOODBYE")
                app_running = False


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv()
    app()

    for book in session.query(Book):
        print(book)


# display the menu inside the search module
def search_menu():
    print("""
        
        
        1) Edit entry
        2) Delete entry
        3) Return to main menu
        
        """)
    choice = input("What would you like to do? ")
    try:
        choice = int(choice)
        if choice not in [1, 2, 3]:
            raise ValueError("You did not enter 1, 2 or 3")
    except ValueError as e:
        print("Enter 1, 2 or 3")
    else:
        if choice == 1:
            edit_book()
        if choice == 2:
            delete_book()
        if choice == 3:
            main_menu()


# *************** function to edit a book
def edit_book():
    print("edit_book function")


# ************** function to delete a book
def delete_book():
    print("delete_book function")


# ************* function that search for a book
def search_book():
    # print possible book ids
    list_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Options : {list_id}")
    choice = input("What is the book's id? ")
    try:
        choice = int(choice)
        if choice not in list_ids:
            raise ValueError("You have not entered a correct ID")
    except ValueError as e:
        print("You have to enter an integer")
    else:
        print("book_title")
        print("Published: date_published ")
        print("Current Price: $ price")
        search_menu()


# function that displays books analysis
def book_analysis():
    print("Newest book: book")
    print("Oldest book: book")
    print("Total Number of Books: 14")
    print("Total Number of Python books: 8")
    main_menu()
