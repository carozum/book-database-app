"""
A console program : 

"""

from models import (Base, session,
                    Book, engine)
import csv
import datetime
import time

# *************** Functions to display the different menus


def main_menu():
    while True:
        print("""
            \nPROGRAMMING BOOKS
            \r1) Add book
            \r2) View all books
            \r3) Search for a book by id
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


def submenu():
    while True:
        print("""
            \n1) Edit book
            \r2) Delete book
            \r3) Return to main menu
            """)
        choice = input("What would you like to do ? ")
        if choice in ['1', '2', '3']:
            return choice
        else:
            choice = input("""
                        \rPlease choose one of the options above.
                        \rA number from 1 to 3.
                        \rPress enter to try again. """)


# ******************* Functions to clean the user's inputs

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
            \rPress enter to try again''')
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
            \rPress enter to try again''')
        return
    else:
        return int(price_float * 100)


def clean_id(id_str, id_list):
    try:
        book_id = int(id_str)
    except ValueError as e:
        input('''
            \n******* ID ERROR *****
            \rThe id should be a number. 
            \rPress enter to try again''')
        return
    else:
        if book_id in id_list:
            return book_id
        else:
            input(f'''
            \n******* ID ERROR *****
            \rOptions {id_list} 
            \rPress enter to try again''')
            return


# ************* Function to feed the database

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


# ************** Functions relating to CRUD operations

# Add entries

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


# Read entries

def view_books():
    for book in session.query(Book):
        print(f"{book.id} | {book.title} | {book.author} | {book.published_date.strftime('%B %d, %Y')} | ${book.price /100}")
    input('\nPress enter to return to the main menu.')


# Update and delete an entry

def update_book(the_book):

    print("\n******** EDIT TITLE *********")
    print(f"Current Value: {the_book.title}")
    the_book.title = input("What would you like to change the value to? ")

    print("\n******** EDIT AUTHOR *********")
    print(f"Current Value: {the_book.author}")
    the_book.author = input("What would you like to change the value to? ")

    print("\n******** EDIT DATE *********")
    print(f"Current Value: {the_book.published_date.strftime('%B %d, %Y')}")
    while True:
        change = clean_date(
            input("What would you like to change the value to? "))
        if type(change) == datetime.date:
            the_book.published_date = change
            break

    print("\n******** EDIT PRICE *********")
    print(f"Current Value: {the_book.price/100}")
    while True:
        change = clean_price(
            input("What would you like to change the value to? "))
        if type(change) == int:
            the_book.price = change
            break

    session.commit()


def search_book():
    """
    Search on id. 
    TODO :Add other options to search on author or title or part of the title. Improvement to consider 
    Includes Update and Delete operations
    """
    id_options = []
    for book in session.query(Book):
        id_options.append(book.id)

    id_error = True
    while id_error:
        id_chosen = input(f"""
                    \nId options :{id_options}
                    \rWhat is the book's id? """)
        id_chosen = clean_id(id_chosen, id_options)
        if type(id_chosen) == int:
            id_error = False

    the_book = session.query(Book).filter(Book.id == id_chosen).first()
    print(f"""
        \n{the_book.title} by {the_book.author}
        \rPublished: {the_book.published_date}
        \rPrice: ${the_book.price /100}""")

    sub_choice = submenu()

    if sub_choice == '1':
        update_book(the_book)
    elif sub_choice == '2':
        session.delete(the_book)
        pass
    # else not needed due to the loop in the submenu() function.


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
                search_book()
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

    # for book in session.query(Book):
    #    print(book)
"""
    %d is the day number (2 digits, prefixed with leading zero's if necessary)
    %m is the month number (2 digits, prefixed with leading zero's if necessary)
    %b is the month abbreviation (3 letters)
    %B is the month name in full (letters)
    %y is the year number abbreviated (last 2 digits)
    %Y is the year number full (4 digits)"""
