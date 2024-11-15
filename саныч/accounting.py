import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import matplotlib.pyplot as plt


# Создаем базу данных
def create_db():
    connection = sqlite3.connect('expenses.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            type TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()


# Функция для добавления нового дохода или расхода
def add_transaction():
    amount = entry_amount.get()
    category = entry_category.get()
    date = entry_date.get()
    description = entry_description.get()
    transaction_type = combo_type.get()

    if not amount or not category or not date or not transaction_type:
        messagebox.showwarning("Поле не заполнено", "Пожалуйста, заполните все поля.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Ошибка", "Сумма должна быть числом.")
        return

    connection = sqlite3.connect('expenses.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO transactions (amount, category, date, description, type) 
        VALUES (?, ?, ?, ?, ?)
    ''', (amount, category, date, description, transaction_type))
    connection.commit()
    connection.close()
    load_transactions()
    clear_entries()


# Функция для загрузки транзакций в список
def load_transactions():
    for row in tree.get_children():
        tree.delete(row)

    connection = sqlite3.connect('expenses.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    for transaction in transactions:
        tree.insert("", "end", values=transaction)
    connection.close()


# Функция для отображения статистики по категориям
def show_statistics():
    connection = sqlite3.connect('expenses.db')
    cursor = connection.cursor()
    cursor.execute('SELECT category, SUM(amount), type FROM transactions GROUP BY category, type')
    data = cursor.fetchall()
    connection.close()

    income = {}
    expenses = {}

    for category, amount, type in data:
        if type == 'доход':
            income[category] = amount
        else:
            expenses[category] = amount

    # Построение графика
    categories = list(set(income.keys()).union(set(expenses.keys())))
    income_values = [income.get(cat, 0) for cat in categories]
    expenses_values = [expenses.get(cat, 0) for cat in categories]

    x = range(len(categories))

    fig, ax = plt.subplots()
    ax.bar(x, income_values, width=0.4, label='Доход', color='g', align='center')
    ax.bar(x, expenses_values, width=0.4, label='Расход', color='r', align='edge')

    ax.set_ylabel('Сумма')
    ax.set_title('Статистика доходов и расходов по категориям')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()

    plt.show()


# Очищаем поля ввода
def clear_entries():
    entry_amount.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    combo_type.set('')


# Создание основного интерфейса
app = tk.Tk()
app.title("Учёт расходов")
app.geometry("600x400")

# Создание базы данных
create_db()

# Поля ввода
entry_amount = tk.Entry(app, width=20)
entry_amount.grid(row=0, column=1)
tk.Label(app, text="Сумма:").grid(row=0, column=0)

entry_category = tk.Entry(app, width=20)
entry_category.grid(row=1, column=1)
tk.Label(app, text="Категория:").grid(row=1, column=0)

entry_date = tk.Entry(app, width=20)
entry_date.grid(row=2, column=1)
tk.Label(app, text="Дата (YYYY-MM-DD):").grid(row=2, column=0)

entry_description = tk.Entry(app, width=20)
entry_description.grid(row=3, column=1)
tk.Label(app, text="Описание:").grid(row=3, column=0)

combo_type = ttk.Combobox(app, values=["доход", "расход"], state="readonly")
combo_type.grid(row=4, column=1)
tk.Label(app, text="Тип:").grid(row=4, column=0)

# Кнопки
btn_add = tk.Button(app, text="Добавить", command=add_transaction)
btn_add.grid(row=5, columnspan=2)

btn_statistics = tk.Button(app, text="Показать статистику", command=show_statistics)
btn_statistics.grid(row=6, columnspan=2)

# Список транзакций
columns = ("id", "amount", "category", "date", "description", "type")
tree = ttk.Treeview(app, columns=columns, show='headings')
tree.heading("id", text="ID")
tree.heading("amount", text="Сумма")
tree.heading("category", text="Категория")
tree.heading("date", text="Дата")
tree.heading("description", text="Описание")
tree.heading("type", text="Тип")

tree.grid(row=7, columnspan=2, sticky='nsew')

# Настройка размера окна
app.grid_rowconfigure(7, weight=1)
app.grid_columnconfigure(1, weight=1)

load_transactions()
app.mainloop()