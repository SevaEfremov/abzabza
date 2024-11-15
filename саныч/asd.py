import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление библиотекой")

        self.conn = sqlite3.connect("library.db")
        self.create_table()

        self.books = []

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.title_label = tk.Label(self.frame, text="Название книги:")
        self.title_label.grid(row=0, column=0)

        self.title_entry = tk.Entry(self.frame)
        self.title_entry.grid(row=0, column=1)

        self.author_label = tk.Label(self.frame, text="Автор:")
        self.author_label.grid(row=1, column=0)

        self.author_entry = tk.Entry(self.frame)
        self.author_entry.grid(row=1, column=1)

        self.add_button = tk.Button(self.frame, text="Добавить книгу", command=self.add_book)
        self.add_button.grid(row=2, column=0, columnspan=2)

        self.view_button = tk.Button(self.frame, text="Показать книги", command=self.view_books)
        self.view_button.grid(row=3, column=0, columnspan=2)

        self.delete_button = tk.Button(self.frame, text="Удалить книгу", command=self.delete_book)
        self.delete_button.grid(row=4, column=0, columnspan=2)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        if title and author:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO books (title, author) VALUES (?, ?)', (title, author))
            self.conn.commit()
            messagebox.showinfo("Успех", "Книга добавлена!")
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите название и автора книги.")

    def view_books(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()

        if books:
            book_list = "\n".join([f"{id}: {title} - {author}" for id, title, author in books])
            messagebox.showinfo("Список книг", book_list)
        else:
            messagebox.showinfo("Список книг", "Библиотека пуста.")

    def delete_book(self):
        id_to_delete = simpledialog.askinteger("Удаление книги", "Введите ID книги для удаления:")
        if id_to_delete:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM books WHERE id = ?', (id_to_delete,))
            self.conn.commit()
            messagebox.showinfo("Успех", "Книга удалена!")
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите корректный ID книги.")

    def on_closing(self):
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()