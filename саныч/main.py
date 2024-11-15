import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from datetime import datetime


# Создаем базу данных
def create_db():
    connection = sqlite3.connect('todo_list.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            priority INTEGER NOT NULL,
            deadline DATE,
            status BOOLEAN NOT NULL
        )
    ''')
    connection.commit()
    connection.close()


# Добавление задачи
def add_task():
    task = simpledialog.askstring("Новая задача", "Введите описание задачи:")
    priority = simpledialog.askinteger("Приоритет", "Введите приоритет (1-5):")
    deadline = simpledialog.askstring("Дедлайн", "Введите дедлайн (YYYY-MM-DD):")

    if task and priority is not None:
        connection = sqlite3.connect('todo_list.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tasks (task, priority, deadline, status) VALUES (?, ?, ?, ?)",
                       (task, priority, deadline, False))
        connection.commit()
        connection.close()
        load_tasks()


# Отметка задачи как выполненной
def toggle_status(task_id):
    connection = sqlite3.connect('todo_list.db')
    cursor = connection.cursor()
    cursor.execute("SELECT status FROM tasks WHERE id=?", (task_id,))
    current_status = cursor.fetchone()[0]
    new_status = not current_status
    cursor.execute("UPDATE tasks SET status=? WHERE id=?", (new_status, task_id))
    connection.commit()
    connection.close()
    load_tasks()


# Удаление задачи
def delete_task(task_id):
    connection = sqlite3.connect('todo_list.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    connection.commit()
    connection.close()
    load_tasks()


# Загрузка задач
def load_tasks(status_filter='all'):
    for widget in task_frame.winfo_children():
        widget.destroy()

    connection = sqlite3.connect('todo_list.db')
    cursor = connection.cursor()
    if status_filter == 'completed':
        cursor.execute("SELECT * FROM tasks WHERE status=1")
    elif status_filter == 'incomplete':
        cursor.execute("SELECT * FROM tasks WHERE status=0")
    else:
        cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()
    for task in tasks:
        task_id, task_description, priority, deadline, status = task
        status_str = 'Выполнено' if status else 'Не выполнено'
        task_label = tk.Label(task_frame,
                              text=f"{task_description} (Приоритет: {priority}, Дедлайн: {deadline}, {status_str})")
        task_label.pack()

        toggle_btn = tk.Button(task_frame, text='Поменять статус', command=lambda tid=task_id: toggle_status(tid))
        toggle_btn.pack()

        delete_btn = tk.Button(task_frame, text='Удалить', command=lambda tid=task_id: delete_task(tid))
        delete_btn.pack()

    connection.close()


# Фильтрация задач
def filter_tasks(filter_option):
    load_tasks(filter_option)


# Главный интерфейс
root = tk.Tk()
root.title("Список дел")

# Создание базы данных
create_db()

# Кнопки
add_task_button = tk.Button(root, text="Добавить задачу", command=add_task)
add_task_button.pack()

# Фильтры
filter_frame = tk.Frame(root)
filter_frame.pack()
filter_all = tk.Button(filter_frame, text="Все", command=lambda: filter_tasks('all'))
filter_all.pack(side=tk.LEFT)
filter_completed = tk.Button(filter_frame, text="Выполненные", command=lambda: filter_tasks('completed'))
filter_completed.pack(side=tk.LEFT)
filter_incomplete = tk.Button(filter_frame, text="Не выполненные", command=lambda: filter_tasks('incomplete'))
filter_incomplete.pack(side=tk.LEFT)

# Список задач
task_frame = tk.Frame(root)
task_frame.pack()

# Загрузка задач
load_tasks()

# Основной цикл
root.mainloop()