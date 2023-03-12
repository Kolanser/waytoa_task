import psycopg2


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
                CREATE TABLE tasks(
                    id serial PRIMARY KEY,
                    number_task varchar(16) NOT NULL,
                    url_task varchar(512) NOT NULL,
                    name_task varchar(64) NOT NULL,
                    complexity integer,
                    resolved integer
                );
                """
            )

            connection.commit()
            print("[INFO] Table tasks created successfully")

        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE tags(
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
            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT id FROM tasks WHERE number_task = '{values[0]}';"
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
                print("[INFO] Data was succefully inserted") 
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def main():
    host = '127.0.0.1'
    user = 'postgres'
    password = 'postgres'
    db_name = 'scrap'
    create_tables(host, user, password, db_name)


if __name__ == '__main__':
    main()
