import psycopg2
from psycopg2 import OperationalError

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Добро пожаловать,", db_user, "!")
    except OperationalError as e:
        #print(f"The error '{e}' occurred")
        print(f"Что-то пошло не так...")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Запрос выполнен!")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    connection.commit()

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")

print("Введите логин:")
login = input()
if (login == "guest"):
    password = "guest"
else:
    print("Введите пароль:")
    password = input()
connection = create_connection(
    "list1", login, password, "127.0.0.1", "5432"
)

select_users = "SELECT * FROM workers"
workers = execute_read_query(connection, select_users)

s = ""
if (login == "guest"):
    for worker in workers:
        print(worker)
        for i in range(6):
            if(i != 4 and i != 5):
                s_temp = str(worker[i])
                while (len(s_temp) < 25):
                    s_temp += " "
                s += s_temp + "||"
        print(s)
        s = ""
else:
    for worker in workers:
        for i in range(6):
            s_temp = str(worker[i])
            while (len(s_temp) < 25):
                s_temp += " "
            s += s_temp + "||"
        print(s)
        s = ""

print("Выберите действие:")
print("1 - Добавить пользователя")
print("2 - Удалить пользователя")
print("3 - Изменить пользователя")
print("Любое другое число - Выход")

num = int(input())
if (num == 1):
    if (login == "director"):
        try:
            print("Введите фамилию:")
            lastName = input()
            print("Введите имя и отчество:")
            name = input()
            print("Введите должность:")
            dolzh = input()
            print("Введите адрес:")
            adress = input()
            print("Введите личный телефон:")
            myNumber = input()
            print("Введите рабочий телефон:")
            workNumber = input()
            post = (lastName, name, dolzh, adress, myNumber, workNumber)
            post_records = ", ".join(["%s"] * len(post))
            insert_query = (
            f"INSERT INTO workers (Фамилия, Имя_Отчество, Должность, Адрес, Личный_телефон, Рабочий_телефон) VALUES ({post_records})"
            )
            cursor = connection.cursor()
            cursor.execute(insert_query, post)
            connection.commit()
        except OperationalError as e:
            print(f"The error '{e}' occurred")
    else:
        print("Нет доступа: свяжитесь с администратором")
elif (num == 2):
    if (login == "director"):
        try:
            print("Введите id пользователя, которого вы хотите удалить:")
            id = int(input())
            delete_comment = f"DELETE FROM workers WHERE id = {id}"
            execute_query(connection, delete_comment)
        except OperationalError as e:
            print(f"The error '{e}' occurred")
    else:
        print("Нет доступа: свяжитесь с администратором")
elif(num == 3):
    if (login == "director" or login == "zamDirector"):
        try:
            print("Введите id пользователя, которого вы хотите отредактировать:")
            id = int(input())
            print("Введите поле, которое вы хотите отредактировать:")
            field = input()
            print("Введите новые данные:")
            newField = input()
            update_post_description = f"""
            UPDATE
                workers
            SET
                {field} = '{newField}'
            WHERE 
                id = {id}
            """
            execute_query(connection, update_post_description)
        except OperationalError as e:
            print(f"The error '{e}' occurred")
    else:
        print("Нет доступа: свяжитесь с администратором")