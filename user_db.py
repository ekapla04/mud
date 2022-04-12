import sqlite3


def connect():
    # connect to database
    conn = sqlite3.connect("users.db")

    # create cursor object to send SQL statements to db
    cursor = conn.cursor()

    # i believe associating primary key with username means only one person 
        # can have any given username
    cursor.execute("CREATE TABLE IF NOT EXISTS users \
                    (username TEXT PRIMARY KEY, \
                     password TEXT)")

    prompt(conn, cursor)

    conn.commit()
    conn.close()


def login(conn, cursor):
    # get username and password from client
    cursor, username, password = exists(cursor)

    ta_key = True
    # if this call to db returns something
    if cursor.fetchall():
        print("Log in successful")
    else:
        print("Log in failed.")
        while ta_key == True:
            attempt = input("Type T to try again, Q to quit: ")
            if attempt == "T" or attempt == "t":
                login(conn, cursor)
            elif attempt == "Q" or attempt == "q":
                ta_key = False
                exit(0)
            else:
                print("Unknown response. Try again.")


# opening prompt           
def prompt(conn, cursor):
    user_status = input("Are you a returning user? Type Y or N: ")
    if user_status == "Y" or user_status == "y":
        login(conn, cursor)
    elif user_status == "N" or user_status == "n":
        create_new_user(conn, cursor)
    else:
        print("Unknown response. Try again.")
        prompt(conn, cursor)
        

def create_new_user(conn, cursor):
    cursor, uname, pswd = exists(cursor)
    print("username: " + str(uname))
    try:
        cursor.execute("INSERT INTO users VALUES (?, ?)", (uname, pswd))
    except:
        print("Username already taken. Try again.")
        create_new_user(conn, cursor)


def exists(cursor):
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    cursor.execute('SELECT * from users WHERE username="%s" AND password="%s"'\
                   %(username,password))
    return cursor, username, password

connect()
