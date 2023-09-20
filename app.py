"""
A console program : 

"""

import sys
from models import (Base, session, 
                    Book, engine)

# ********** function for data cleaning in the database

# ************ Function to display main menu
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
        else :
            choice = input("""
                        \rPlease choose one of the options above.
                        \rA number from 1 to 5.
                        \rPress enter to try again. """)
        

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
        if choice == 2 :
            delete_book()
        if choice==3:
            main_menu()


# **************** Function to add book to the database
def add_book():
    print("Add a New Book")
    title = input("Book title: ")
    author = input("Author: ")
    date_published = input("Published (Example: January 13, 2023): ")
    price = input("Price (Example: 10.99): ")
    
    print("Book added!")
    main_menu()

def all_books():
    print("all_books function")


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
    
    
def app():
    app_running = True
    while app_running:
        choice = main_menu()
        match choice:
            case '1':
                # add_book()
                pass
            case '2':
                # search book
                pass
            case '3':
                # view book
                pass
            case '4':
                # analysis
                pass
            case _:
                print("GOODBYE")
                app_running = False

if __name__ == "__main__":
    Base.metadata.create_all(engine) 
    app()
    
