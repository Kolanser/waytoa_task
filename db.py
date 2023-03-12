import psycopg2
from os import getenv
from dotenv import load_dotenv


load_dotenv()


def create_tables(host, user, password, db_name):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE if not exists tasks(
                    id serial PRIMARY KEY,
                    number_task varchar(16) NOT NULL,
                    url_task varchar(512) NOT NULL,
                    name_task varchar(64) NOT NULL,
                    complexity integer,
                    resolved integer,
                    kontest integer DEFAULT 0
                );
                """
            )

            connection.commit()
            print("[INFO] Table tasks created successfully")

        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE if not exists tags(
                    id serial PRIMARY KEY,
                    task_id integer,
                    tag varchar(64) NOT NULL,
                    FOREIGN KEY (task_id) REFERENCES tasks (id)
                );
                """
            )

            connection.commit()
            print("[INFO] Table tags created successfully")
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def insert_data(host, user, password, db_name, one_scrap):
    try:
        connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
        connection.autocommit = True
        for values in one_scrap:
            task_id = None
            with connection.cursor() as cursor:
                cursor.execute(
                    (
                        "SELECT id FROM tasks"
                        f" WHERE number_task = '{values[0]}'"
                    )
                )
                task_id = cursor.fetchone()
            if not task_id:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO tasks (
                            number_task,
                            url_task,
                            name_task,
                            complexity,
                            resolved) VALUES
                        (%s, %s, %s, %s, %s)""",
                        values[:5]
                    )
                print("[INFO] Data was succefully inserted in tasks")
                with connection.cursor() as cursor:
                    cursor.execute(
                        (
                            "SELECT id FROM tasks"
                            f" WHERE number_task = '{values[0]}'"
                        )
                    )
                    task_id = cursor.fetchone()[0]
                for elem in values[5]:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO tags (
                                task_id,
                                tag) VALUES
                            (%s, %s)""",
                            (task_id, elem)
                        )
                print("[INFO] Data was succefully inserted in tags")
    except Exception as _ex:
        print("[ERROR] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def select_tasks(host, user, password, db_name, tag, complexity):
    try:
        select = (('Задач нет',),)
        connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                (
                    'SELECT url_task FROM tasks'
                    ' WHERE id IN'
		            f' (SELECT task_id FROM tags WHERE tag = \'{tag}\')'
                    f' AND complexity = {complexity}'
                )
            )
            select = cursor.fetchall()
            if not select:
                select = (('Задач нет',),)
    except Exception as _ex:
        print("[ERROR] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")
        return select


def create_kontest(host, user, password, db_name):
    try:
        connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
        connection.autocommit = True

        complexities = []
        with connection.cursor() as cursor:
            cursor.execute(
                (
                    'SELECT DISTINCT complexity FROM tasks'
                    ' WHERE complexity > 0'
                    ' AND kontest_2 = 0'
                )
            )
            complexities = cursor.fetchall()
        tags = []
        with connection.cursor() as cursor:
            cursor.execute(
                (
                    'SELECT DISTINCT tag FROM tags'
                )
            )
            tags = cursor.fetchall()
        count_task = 10
        for complexity in complexities:
            for tag in tags:
                pass
    except Exception as _ex:
        print("[ERROR] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")
def main():
    host = getenv('HOST')
    user = getenv('USER')
    password = getenv('PASSWORD')
    db_name = getenv('DB_NAME')
    create_tables(host, user, password, db_name)


if __name__ == '__main__':
    main()
