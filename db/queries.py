# tasks
# id, task 


CREATE_TABLE_TASKS = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL
    )
"""


# INSERT INTO tasks (task) VALUES (?)

INSERT_TASK = "INSERT INTO tasks (task) VALUES (?)"

# SELECT id, task FROM tasks 

SELECT_TASKS = "SELECT id, task FROM tasks"

# DELETE FROM tasks WHERE id = ?

DELETE_TASK = "DELETE FROM tasks WHERE id = ?"

# UPDATE tasks SET task = ? WHERE id = ?

UPDATE_TASK = "UPDATE tasks SET task = ? WHERE id = ?"