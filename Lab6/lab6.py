'''
Лабораторная работа номер 6
Многострочный комментарий
'''

# Импорт библиотеки, отвечающей за связь с SQL
import psycopg2
from psycopg2 import OperationalError

# Соединение с базой данных
def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            # Имя базы данных
            database=db_name,
            # Логин
            user=db_user,
            # Пароль
            password=db_password,
            # Хост
            host=db_host,
            # Порт сервера
            port=db_port,
        )
        # Отобразить приветствие при успешном соединении
        print("Добро пожаловать,", db_user, "!")
    # Если случилась ошибка, выдать сообщение
    except OperationalError as e:
        print(f"Что-то пошло не так...")
    return connection

# Выполнение запроса SQL. На вход подаётся нужная база данных и сам запрос в текстовом виде
def execute_query(connection, query):
    # Связь с курсором базы данных
    cursor = connection.cursor()
    try:
        # Выполнение запроса
        cursor.execute(query)
        print("Запрос выполнен!")
    # Уведомление об ошибке
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    # Обновление базы данных после выполнения запроса
    connection.commit()

# Выполнение запроса для чтения информации из базы данных
def execute_read_query(connection, query):
    # Связь с курсором базы данных
    cursor = connection.cursor()
    result = None
    try:
        # Выполнение запроса и сохранение информации
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        # Уведомление об ошибке
        print(f"The error '{e}' occurred")

print("Введите логин:")
# Ввод логина 
login = input()
# Если логин "guest" - вход без пароля
if (login == "guest"):
    password = "guest"
else:
    print("Введите пароль:")
    # Ввод пароля
    password = input()
# Связь с базой данных с полученными вводными данными
connection = create_connection(
    "list1", login, password, "127.0.0.1", "5432"
)

# Выполнение запроса для чтения таблицы workers из базы данных
select_users = "SELECT * FROM workers"
workers = execute_read_query(connection, select_users)

# Построение визуального отображения таблицы
s = ""
# Для гостя таблица строится без нескольких колонок
if (login == "guest"):
    for worker in workers:
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

# Вывод возможных действий
print("Выберите действие:")
print("1 - Добавить пользователя")
print("2 - Удалить пользователя")
print("3 - Изменить пользователя")
print("Любое другое число - Выход")

# Ввод номера действия
num = int(input())
# Добавление работника в таблицу
if (num == 1):
    # Проверка пользователя
    if (login == "director"):
        try:
            # Ввод данных работника
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
            # Объединение полученного списка в строку
            post_records = ", ".join(["%s"] * len(post))
            # Выполнение запроса на добавление
            insert_query = (
            f"INSERT INTO workers (Фамилия, Имя_Отчество, Должность, Адрес, Личный_телефон, Рабочий_телефон) VALUES ({post_records})"
            )
            cursor = connection.cursor()
            cursor.execute(insert_query, post)
            # Обновление базы данных после выполнения запроса
            connection.commit()
        except OperationalError as e:
            # Вывод уведомления об ошибке
            print(f"The error '{e}' occurred")
    else:
        # Если пользователь не допущен к действию - вывод уведомления
        print("Нет доступа: свяжитесь с администратором")
# Удалить работника из таблицы
elif (num == 2):
    # Проверка пользователя
    if (login == "director"):
        try:
            print("Введите id пользователя, которого вы хотите удалить:")
            # Ввод номера удаляемого работника
            id = int(input())
            # Выполнение запроса
            delete_comment = f"DELETE FROM workers WHERE id = {id}"
            execute_query(connection, delete_comment)
        except OperationalError as e:
            # Уведомление об ошибке
            print(f"The error '{e}' occurred")
    else:
        # Если пользователь не допущен к действию - вывод уведомления
        print("Нет доступа: свяжитесь с администратором")
# Изменение пользователя
elif(num == 3):
    # Проверка пользователя
    if (login == "director" or login == "zamDirector"):
        try:
            print("Введите id пользователя, которого вы хотите отредактировать:")
            # Ввод номера изменяемого работника
            id = int(input())
            print("Введите поле, которое вы хотите отредактировать:")
            # Ввод имени изменяемого поля
            field = input()
            print("Введите новые данные:")
            # Ввод новых данных
            newField = input()
            # Выполнение запроса на изменение работника
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
            # Уведомление об ошибке
            print(f"The error '{e}' occurred")
    else:
        # Если пользователь не допущен к действию - вывод уведомления
        print("Нет доступа: свяжитесь с администратором")