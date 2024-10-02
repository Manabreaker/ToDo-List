import psycopg2

host = "YOURHOSTNAME"  # Хост базы данных
user = "YOURUSERNAME"  # Пользователь PostgreSQL
password = "YOURPASSWORD"  # Пароль пользователя PostgreSQL
db_name = "tasks"  # Название базы данных

def get_connection():
    """Установка соединения с базой данных"""
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        return connection
    except Exception as e:
        print("Error while connecting to PostgreSQL:", e)
        return None

def create_tasks_table():
    """Создание таблицы tasks, если её нет"""
    try:
        connection = get_connection()
        if connection is None:
            print("Could not establish a connection.")
            return False

        cursor = connection.cursor()
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {db_name} (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            is_completed BOOLEAN DEFAULT FALSE
        );
        """)
        connection.commit()
        print('Table tasks created successfully')
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print("Error while creating tasks table:", e)
        return False


create_tasks_table()
