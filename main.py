import psycopg2


class DatabaseManager:
    def __init__(self):
        self.database = psycopg2.connect(
            dbname="test",
            user="postgres",
            host="localhost",
            password="1"
        )

    def manager(self, sql, *args, commit=False, fetchone=False, fetchall=False):
        with self.database as db:
            with db.cursor() as cursor:
                cursor.execute(sql, args)
                result = None
                if commit:
                    db.commit()
                elif fetchone:
                    result = cursor.fetchone()
                elif fetchall:
                    result = cursor.fetchall()
                return result

    def create_tables(self):
        queries = [
            '''
            CREATE TABLE IF NOT EXISTS departments(
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS employee(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50),
                position TEXT,
                salary INTEGER,
                hire_date DATE,
                department_id INTEGER NOT NULL REFERENCES departments ON DELETE CASCADE
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS projects(
                id SERIAL PRIMARY KEY,
                project_name VARCHAR(100) NOT NULL,
                start_date DATE,
                end_date DATE DEFAULT CURRENT_DATE,
                budget NUMERIC(7, 2)
            );
            '''
        ]
        for query in queries:
            self.manager(query, commit=True)

    def inserts(self):
        queries = [
            '''
            INSERT INTO employee(first_name, last_name, position, salary, hire_date, department_id) VALUES
                ('Ali', 'Karimov', 'Manager', 3000, '2020-03-15', 1),
                ('Nodira', 'Toirova', 'Developer', 2500, '2021-05-10', 2),
                ('Shoxrux', 'Abdullayev', 'Designer', 2200, '2022-01-22', 3),
                ('Zarina', 'Abdullayeva', 'HR Specialist', 1800, '2019-11-11', 1),
                ('Jasur', 'Aliyev', 'Developer', 2400, '2023-02-01', 2);
            ''',
            '''
            INSERT INTO projects(project_name, start_date, end_date, budget) VALUES
                ('New Website', '2023-01-10', '2023-06-30', 50000),
                ('Mobile App', '2022-08-15', '2023-03-20', 30000),
                ('CRM System', '2024-02-01', NULL, 60000);
            '''
        ]
        for query in queries:
            self.manager(query, commit=True)

    def changes(self):
        queries = [
            '''
            SELECT first_name || ' ' || last_name AS full_name FROM employee;
            ''',
            '''
            SELECT * FROM employee ORDER BY salary DESC;
            ''',
            '''
            SELECT * FROM employee WHERE salary >= 2500 ORDER BY salary;
            ''',
            '''
            SELECT * FROM employee ORDER BY salary DESC LIMIT 3;
            ''',
            '''
            SELECT * FROM employee WHERE salary IN (2400, 3000);
            ''',
            '''
            SELECT * FROM employee WHERE salary BETWEEN 2000 AND 3000;
            ''',
            '''
            SELECT * FROM employee WHERE first_name LIKE '%a%';
            ''',
            '''
            SELECT * FROM projects WHERE end_date IS NULL;
            ''',
            '''
            SELECT department_id, AVG(salary) AS avg_salary FROM employee GROUP BY department_id;
            '''
        ]
        for query in queries:
            result = self.manager(query, fetchall=True)
            print(result)


if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.create_tables()
    db_manager.inserts()
    db_manager.changes()
