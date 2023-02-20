import sqlite3
from prettytable import from_db_cursor


db=sqlite3.connect('books')
cursor=db.cursor()
#create table and columns with id as primary key
try:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books
        (id INTEGER PRIMARY KEY, 
        title TEXT,
        author TEXT, 
        qty INTEGER)
        ''')
    db.commit()
except Exception as e:
    db.rollback()
    print('Invalid selection:\t',e)
    

books_=[
    (3001,'''A Tale of Two Cities''','''Charles Dickens''',30),
    (3002,'''Harry Potter and the Philosopher's stone''','''J.K. Rowling''',40),
    (3003,'''The Lion, the Witch and the Wardrobe''','''C.S. Lewis''',25),
    (3004,'''The Lord of the Rings''','''J.R.R. Tolkien''',37),
    (3005,'''Alice in Wonderland''','''Lewis Carroll''',12)
    ]

def make_list():
    try:
        cursor.executemany('''
        INSERT OR IGNORE INTO books 
        VALUES(?,?,?,?)''',
        books_)
        db.commit()
        return
    except Exception as e:
        print('Invalid selection:\t',e)

def show_table():
    try:
        cursor.execute('''
        SELECT * FROM books
        ''')
        db.commit()
        table = from_db_cursor(cursor)
        print(table,'\n')
    except Exception as e:
        print('Invalid selection:\t',e)


def format(book):
    print(f'''
id:\t{book[0]}
Title:\t{book[1]}
Author:\t{book[2]}
Qty:\t{book[3]}
''')
    return
            

def enter_book():
    while True:   
        query=input('Enter new book? (Y/N) ').lower()
        if query=='n':
            return
        if query=='y':
            enter_book_2()
        else:
            print("Invalid Selection")


def enter_book_2():
    while True:
        try:
            id=int(input('Enter a unique book id number: '))  
            cursor.execute('''
            SELECT * FROM books 
            WHERE id=?''',(id,)) 
            db.commit()   
            if cursor.fetchone():
                print("ID already exists, please enter a different ID")
            else:      
                title=input('Enter book title: ')
                author=input('Enter book author: ')
                qty=int(input('Enter number of available books: '))
            new_book=(id,title,author,qty)
            books_.append(new_book)
            format(new_book)
            print('\nBook entered')
            make_list()
            show_table()
            return
        except Exception as e:
            print('Invalid selection:\t',e)


def search_book():
    while True:
        try:
            search=input('Enter id number to search for: ')
            cursor.execute(f'''
            SELECT * FROM books 
            WHERE id={search}''')
            book=(cursor.fetchone())
            db.commit()
            format(book)
            return(book)
        except Exception as e:
            print('Invalid selection:\t',e)

def update_book():
    while True:
            selected_book=search_book()
            query=input('Update book? (Y/N)').lower()
            if query=='n':
                return
            if query=='y':
                update_book_2(selected_book)
                show_table()
                query=input('Update another book? (Y/N)').lower()
                if query=='n':
                    break
                if query=='y':
                    continue
            else:
                print("Invalid Selection")
            


def update_book_2(selected_book):
    id=selected_book[0]
    while True:
        try:
            query=input('What would you like to update? (title/author,qty)').lower()
            if query=='title':
                new_title = input("Enter the new title: ")
                cursor.execute("UPDATE books SET title=? WHERE id=?", (new_title, id))
            elif query=='author':
                new_author = input("Enter the new author: ")
                cursor.execute("UPDATE books SET author=? WHERE id=?", (new_author, id))
            elif query=='qty':
                new_quantity = int(input("Enter the new quantity: "))
                cursor.execute("UPDATE books SET qty=? WHERE id=?", (new_quantity, id))
            else:
                print('Invalid selection')
                continue
            print('Book entry updated.')
            break
        except Exception as e:
            print('Invalid selection:\t',e)

def delete_book():
    while True:
        try:
            book_id=search_book()[0]
            query=input('Are you sure you want to delete this book? (Y/N) ')
            if query=='n':
                continue  
            if query=='y':
                cursor.execute(f'''
                DELETE FROM books 
                WHERE id = {book_id}
                ''')
                db.commit()
                print('Book deleted from database')
                show_table()
                query=input('Delete another book? (Y/N)').lower()
                if query=='n':
                    break
                if query=='y':
                    continue
        except Exception as e:
            print('Invalid selection:\t',e)

make_list()

while True:
    try:
        show_table()
        menu=int(input('''Select one of the following Options below:
        1. Enter book
        2. Update book
        3. Delete book
        4. Search book
        0. Exit
        '''))

        if menu==1:
            enter_book()
        elif menu==2:
            update_book()
        elif menu==3:
            delete_book()
        elif menu==4:
            print(search_book())
        elif menu==0:
            print('Goodbye!!!')
            db.close()
            exit()
        else:
            print("You have made a wrong choice, Please Try again")
    except Exception as e:
        print('Invalid selection:\t',e)


