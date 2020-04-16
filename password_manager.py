import mysql.connector
from mysql.connector import errorcode
import random
import string

# connection to the database
try:
    db = mysql.connector.connect(
        user='root',  password='1234', host='127.0.0.1', database='pw_manager', auth_plugin='mysql_native_password')
    cursor = db.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)


def generate_random_password():
    pw_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(pw_characters) for i in range(15))


def set_admin_password(pw):
    add_admin_pw_query = ("INSERT INTO passwords "
                          "(password_, service)"
                          "VALUES (%s, %s)")
    cursor.execute(add_admin_pw_query, (pw, 'ADMIN'))
    db.commit()


def get_admin_password():
    pw = ""
    select_admin_pw_query = ("SELECT password_, service FROM passwords "
                             "WHERE service = %(service)s")
    cursor.execute(select_admin_pw_query, {'service': 'ADMIN'})
    for (password_, service) in cursor:
        pw = password_
    return pw


def set_service_password(new_pw, new_service):

    new_password_query = ("INSERT INTO passwords "
                          "(password_, service)"
                          "VALUES(%s, %s)")
    cursor.execute(new_password_query, (new_pw, new_service))
    print('New password has been stored\n')
    db.commit()


def get_service_password(service_):
    pw = ""
    select_admin_pw_query = ("SELECT password_, service FROM passwords "
                             "WHERE service = %(service)s")
    cursor.execute(select_admin_pw_query, {'service': service_})
    for (password_, service) in cursor:
        pw = password_
    return pw


admin_pw = ""
isSet = input(
    "Have you already set up your password for the program (Y/N)?\n")
if isSet.lower().strip() == 'n':
    pw = input("Please enter your new admin password:\n")
    set_admin_password(pw)
    print('Your admin password has been created\n')

user_pw = input("Enter your admin password: \n")
admin_pw = get_admin_password()
while admin_pw != user_pw:
    user_pw = input("Wrong password. Please type again: \n")


while True:
    print('*'*20)
    print('What would you like to do today?\n')
    print('Commands:')
    print('q = quit program')
    print('s = store password')
    print('g = get password')
    print('*'*20)
    cmd = input(":")
    cmd = cmd.strip()

    if cmd == "q":
        break
    elif cmd == "s":
        new_service = input(
            "What is the name of the service you'd like to store? \n")
        new_pw = generate_random_password()
        set_service_password(new_pw, new_service)
        print("Your password for {} is {}\n".format(new_service, new_pw))
    elif cmd == "g":
        service_ = input("What is the name of the service? \n")
        service_ = service_.strip().lower()
        print("Your password for {} is {}\n".format(
            service_, get_service_password(service_)))

cursor.close()
db.close()
