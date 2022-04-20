import sqlite3

class UserDatabase(object):

    def __init__(self):
        '''initialize db class variables'''
        self.connection = sqlite3.connect("users.db")
        self.cur = self.connection.cursor()
        self.create_table


    def close(self):
        '''close sqlite3 connection'''
        self.connection.close()


    def execute(self, new_data):
        '''execute a row of data to current cursor'''
        self.cur.execute(new_data)


    def executemany(self, many_new_data):
        '''add many new data to database in one go. only to be used internally
           to update existing entries'''
        self.create_table()
        self.cur.executemany('REPLACE INTO users VALUES(?, ?, ?, ?, ?)', \
                            (many_new_data,))
    

    def add_user(self,data):
        '''attempt to add a single user to the database'''
        username, pswd = data
        if (self.in_table(data) == False):
            self.cur.execute("INSERT INTO users (username, password) VALUES \
                              (?,?)", (username, pswd))
            print("user added!")
        else:
            print("already in table!")
    

    def in_table(self, username):
        '''check for username match in database'''
        
        self.cur.execute('SELECT * from users WHERE \
                                   username="%s"'\
                                   %(username,))
        result = self.cur.fetchall()
        if(len(result) > 0):
            return True, result
        else:
            print("user '" + str(username) + "' not in table")
            return False, "None"

    def create_table(self):
        '''create a database table if it does not exist already'''
        # this isn't ideal in terms of storing inventory
        # must be stored as a single string with words separated by 
        # commas... sqlite3 doesnt have ability to store lists/tuples 
        # in a column
        self.cur.execute("CREATE TABLE IF NOT EXISTS users \
                                            (username TEXT PRIMARY KEY, \
                                            password TEXT, \
                                            location TEXT, \
                                            inventory TEXT, \
                                            hp INT)")
    

    def parse_inventory(self, username):
        '''returns inventory string in tuple format for easier access
           to individual elements'''
        print("in parse inventory")
        exists,result = self.in_table(username) 
        if (exists == True):
            items = result[0][3].split(", ")
            return items
        else:
            print("no items in inventory because user doesnt exist")
            return None


    def commit(self):
        '''commit changes to database'''
        self.connection.commit()

    #########   Log in code to potentially be reworked later #########

# def connect():
#     # connect to database
#     conn = sqlite3.connect("users.db")

#     # create cursor object to send SQL statements to db
#     cursor = conn.cursor()

#     cursor.execute("CREATE TABLE IF NOT EXISTS users \
#                     (username TEXT PRIMARY KEY, \
#                     password TEXT, \
#                     location TEXT, \
#                     inventory TEXT, \
#                     hp INT)")

#     # prompt(conn, cursor)
#     conn.commit()
#     conn.close()

# def add_character(Character person):
#     print("in add char")
#     print(person.name)
    


# def login(conn, cursor):
#     # get username and password from client
#     cursor, username, password = exists(cursor)

#     ta_key = True
#     # if this call to db returns something
#     if cursor.fetchall():
#         print("Log in successful")
#     else:
#         print("Log in failed.")
#         while ta_key == True:
#             attempt = input("Type T to try again, Q to quit: ")
#             if attempt == "T" or attempt == "t":
#                 login(conn, cursor)
#             elif attempt == "Q" or attempt == "q":
#                 ta_key = False
#                 exit(0)
#             else:
#                 print("Unknown response. Try again.")


# # opening prompt           
# def prompt(conn, cursor):
#     user_status = input("Are you a returning user? Type Y or N: ")
#     if user_status == "Y" or user_status == "y":
#         login(conn, cursor)
#     elif user_status == "N" or user_status == "n":
#         create_new_user(conn, cursor)
#     else:
#         print("Unknown response. Try again.")
#         prompt(conn, cursor)
        

# def create_new_user(conn, cursor):
#     cursor, uname, pswd = exists(cursor)
#     print("username: " + str(uname))
#     try:
#         cursor.execute("INSERT INTO users VALUES (?, ?)", (uname, pswd))
#     except:
#         print("Username already taken. Try again.")
#         create_new_user(conn, cursor)


# def exists(cursor):
#     username = input("Enter Username: ")
#     password = input("Enter Password: ")

#     cursor.execute('SELECT * from users WHERE username="%s" AND password="%s"'\
#                    %(username,password))
#     return cursor, username, password

# connect()
