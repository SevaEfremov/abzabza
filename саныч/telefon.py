import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3

# Создаем базу данных
def create_db():
    connection = sqlite3.connect('phone_book.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT
        )
    ''')
    connection.commit()
    connection.close()

# Функция для добавления нового контакта
def add_contact():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    address = entry_address.get()

    if not first_name or not phone:
        messagebox.showerror("Ошибка", "Имя и номер телефона обязательны.")
        return

    connection = sqlite3.connect('phone_book.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO contacts (first_name, last_name, phone, email, address) VALUES (?, ?, ?, ?, ?)',
                   (first_name, last_name, phone, email, address))
    connection.commit()
    connection.close()
    clear_entries()
    load_contacts()

# Функция для обновления списка контактов
def load_contacts():
    for row in tree.get_children():
        tree.delete(row)
    connection = sqlite3.connect('phone_book.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM contacts')
    for contact in cursor.fetchall():
        tree.insert('', 'end', values=contact)
    connection.close()

# Функция для редактирования выбранного контакта
def edit_contact():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите контакт для редактирования.")
        return

    contact_id = tree.item(selected_item)['values'][0]
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    address = entry_address.get()

    connection = sqlite3.connect('phone_book.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE contacts SET first_name=?, last_name=?, phone=?, email=?, address=? WHERE id=?',
                   (first_name, last_name, phone, email, address, contact_id))
    connection.commit()
    connection.close()
    clear_entries()
    load_contacts()

# Функция для удаления выбранного контакта
def delete_contact():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите контакт для удаления.")
        return

    contact_id = tree.item(selected_item)['values'][0]
    connection = sqlite3.connect('phone_book.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM contacts WHERE id=?', (contact_id,))
    connection.commit()
    connection.close()
    clear_entries()
    load_contacts()

# Функция для поиска контактов
def search_contacts():
    search_term = entry_search.get()
    for row in tree.get_children():
        tree.delete(row)
    connection = sqlite3.connect('phone_book.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM contacts WHERE first_name LIKE ? OR last_name LIKE ? OR phone LIKE ?',
                   (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
    for contact in cursor.fetchall():
        tree.insert('', 'end', values=contact)
    connection.close()

# Функция для очистки полей ввода
def clear_entries():
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_address.delete(0, tk.END)

# Инициализация интерфейса
root = tk.Tk()
root.title("Телефонный справочник")
create_db()

# Поля ввода
frame_entries = tk.Frame(root)
frame_entries.pack(pady=10)

tk.Label(frame_entries, text="Имя:").grid(row=0, column=0)
entry_first_name = tk.Entry(frame_entries)
entry_first_name.grid(row=0, column=1)

tk.Label(frame_entries, text="Фамилия:").grid(row=1, column=0)
entry_last_name = tk.Entry(frame_entries)
entry_last_name.grid(row=1, column=1)

tk.Label(frame_entries, text="Телефон:").grid(row=2, column=0)
entry_phone = tk.Entry(frame_entries)
entry_phone.grid(row=2, column=1)

tk.Label(frame_entries, text="Email:").grid(row=3, column=0)
entry_email = tk.Entry(frame_entries)
entry_email.grid(row=3, column=1)

tk.Label(frame_entries, text="Адрес:").grid(row=4, column=0)
entry_address = tk.Entry(frame_entries)
entry_address.grid(row=4, column=1)

# Кнопки
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

button_add = tk.Button(frame_buttons, text="Добавить", command=add_contact)
button_add.grid(row=0, column=0)

button_edit = tk.Button(frame_buttons, text="Редактировать", command=edit_contact)
button_edit.grid(row=0, column=1)

button_delete = tk.Button(frame_buttons, text="Удалить", command=delete_contact)
button_delete.grid(row=0, column=2)

# Поле поиска
entry_search = tk.Entry(root)
entry_search.pack(pady=10)
entry_search.bind("<KeyRelease>", lambda event: search_contacts())

# Список контактов
columns = ("id", "first_name", "last_name", "phone", "email", "address")
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading("id", text="ID")
tree.heading("first_name", text="Имя")
tree.heading("last_name", text="Фамилия")
tree.heading("phone", text="Телефон")
tree.heading("email", text="Email")
tree.heading("address", text="Адрес")
tree.pack()

load_contacts()

root.mainloop()