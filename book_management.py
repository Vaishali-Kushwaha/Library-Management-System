import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection


def open_book_management(parent):

    window = tk.Toplevel(parent)
    window.title("Book Management")
    window.geometry("1000x650")
    window.configure(bg="#f4f6f8")

    # ---------- Title ----------

    title = tk.Label(
        window,
        text="Book Management",
        font=("Arial", 22, "bold"),
        bg="#243447",
        fg="white",
        pady=15
    )
    title.pack(fill="x")

    # ---------- Form ----------

    form = tk.Frame(window, bg="#f4f6f8")
    form.pack(pady=20)

    tk.Label(
        form,
        text="Book ID",
        font=("Arial", 11, "bold"),
        bg="#f4f6f8"
    ).grid(row=0, column=0, padx=10, pady=8)

    book_id_entry = tk.Entry(form, width=30)
    book_id_entry.grid(row=0, column=1, padx=10)

    tk.Label(
        form,
        text="Book Name",
        font=("Arial", 11, "bold"),
        bg="#f4f6f8"
    ).grid(row=1, column=0, padx=10, pady=8)

    book_name_entry = tk.Entry(form, width=30)
    book_name_entry.grid(row=1, column=1, padx=10)

    tk.Label(
        form,
        text="Author",
        font=("Arial", 11, "bold"),
        bg="#f4f6f8"
    ).grid(row=2, column=0, padx=10, pady=8)

    author_entry = tk.Entry(form, width=30)
    author_entry.grid(row=2, column=1, padx=10)

    tk.Label(
        form,
        text="Quantity",
        font=("Arial", 11, "bold"),
        bg="#f4f6f8"
    ).grid(row=3, column=0, padx=10, pady=8)

    quantity_entry = tk.Entry(form, width=30)
    quantity_entry.grid(row=3, column=1, padx=10)

    # ---------- Clear Fields ----------

    def clear_fields():
        book_id_entry.delete(0, tk.END)
        book_name_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)

    # ---------- Load Books ----------

    def load_books():
        for item in table.get_children():
            table.delete(item)

        try:
            db = get_connection()
            cursor = db.cursor()

            cursor.execute(
                "SELECT book_id, book_name, author, quantity FROM books"
            )

            records = cursor.fetchall()

            for record in records:
                table.insert("", tk.END, values=record)

            cursor.close()
            db.close()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # ---------- Add Book ----------

    def add_book():

        name = book_name_entry.get().strip()
        author = author_entry.get().strip()
        quantity = quantity_entry.get().strip()

        if not name or not author or not quantity:
            messagebox.showwarning(
                "Validation",
                "Please fill all fields."
            )
            return

        try:
            quantity = int(quantity)

            if quantity <= 0:
                messagebox.showwarning(
                    "Validation",
                    "Quantity must be greater than 0."
                )
                return

            db = get_connection()
            cursor = db.cursor()

            cursor.execute(
                """
                INSERT INTO books (book_name, author, quantity)
                VALUES (%s, %s, %s)
                """,
                (name, author, quantity)
            )

            db.commit()

            cursor.close()
            db.close()

            messagebox.showinfo(
                "Success",
                "Book added successfully!"
            )

            clear_fields()
            load_books()

        except ValueError:
            messagebox.showwarning(
                "Validation",
                "Quantity must be a number."
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- Update Book ----------

    def update_book():

        book_id = book_id_entry.get().strip()
        name = book_name_entry.get().strip()
        author = author_entry.get().strip()
        quantity = quantity_entry.get().strip()

        if not book_id or not name or not author or not quantity:
            messagebox.showwarning(
                "Validation",
                "Please fill all fields."
            )
            return

        try:
            book_id = int(book_id)
            quantity = int(quantity)

            if quantity < 0:
                messagebox.showwarning(
                    "Validation",
                    "Quantity cannot be negative."
                )
                return

            db = get_connection()
            cursor = db.cursor()

            cursor.execute(
                """
                UPDATE books
                SET book_name=%s, author=%s, quantity=%s
                WHERE book_id=%s
                """,
                (name, author, quantity, book_id)
            )

            if cursor.rowcount == 0:
                messagebox.showwarning(
                    "Not Found",
                    "Book ID not found."
                )
            else:
                db.commit()

                messagebox.showinfo(
                    "Success",
                    "Book updated successfully!"
                )

            cursor.close()
            db.close()

            clear_fields()
            load_books()

        except ValueError:
            messagebox.showwarning(
                "Validation",
                "Book ID and quantity must be numbers."
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- Delete Book ----------

    def delete_book():

        book_id = book_id_entry.get().strip()

        if not book_id:
            messagebox.showwarning(
                "Validation",
                "Enter Book ID."
            )
            return

        try:
            book_id = int(book_id)

            confirm = messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this book?"
            )

            if not confirm:
                return

            db = get_connection()
            cursor = db.cursor()

            cursor.execute(
                "DELETE FROM books WHERE book_id=%s",
                (book_id,)
            )

            if cursor.rowcount == 0:
                messagebox.showwarning(
                    "Not Found",
                    "Book ID not found."
                )
            else:
                db.commit()

                messagebox.showinfo(
                    "Success",
                    "Book deleted successfully!"
                )

            cursor.close()
            db.close()

            clear_fields()
            load_books()

        except ValueError:
            messagebox.showwarning(
                "Validation",
                "Book ID must be a number."
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- Search Book ----------

    def search_book():

        keyword = search_entry.get().strip()

        if not keyword:
            load_books()
            return

        for item in table.get_children():
            table.delete(item)

        try:
            db = get_connection()
            cursor = db.cursor()

            if keyword.isdigit():

                cursor.execute(
                    """
                    SELECT book_id, book_name, author, quantity
                    FROM books
                    WHERE book_id=%s
                    """,
                    (int(keyword),)
                )

            else:

                search_value = "%" + keyword + "%"

                cursor.execute(
                    """
                    SELECT book_id, book_name, author, quantity
                    FROM books
                    WHERE book_name LIKE %s
                    OR author LIKE %s
                    """,
                    (search_value, search_value)
                )

            records = cursor.fetchall()

            for record in records:
                table.insert("", tk.END, values=record)

            if not records:
                messagebox.showinfo(
                    "Search",
                    "No matching book found."
                )

            cursor.close()
            db.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- Buttons ----------

    button_frame = tk.Frame(window, bg="#f4f6f8")
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Add Book",
        command=add_book,
        width=15
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        button_frame,
        text="Update",
        command=update_book,
        width=15
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        button_frame,
        text="Delete",
        command=delete_book,
        width=15
    ).grid(row=0, column=2, padx=5)

    tk.Button(
        button_frame,
        text="Clear",
        command=clear_fields,
        width=15
    ).grid(row=0, column=3, padx=5)

    # ---------- Search ----------

    search_frame = tk.Frame(window, bg="#f4f6f8")
    search_frame.pack(pady=15)

    tk.Label(
        search_frame,
        text="Search:",
        font=("Arial", 11, "bold"),
        bg="#f4f6f8"
    ).pack(side="left", padx=5)

    search_entry = tk.Entry(search_frame, width=35)
    search_entry.pack(side="left", padx=5)

    tk.Button(
        search_frame,
        text="Search",
        command=search_book,
        width=12
    ).pack(side="left", padx=5)

    tk.Button(
        search_frame,
        text="Show All",
        command=load_books,
        width=12
    ).pack(side="left", padx=5)

    # ---------- Table ----------

    table_frame = tk.Frame(window)
    table_frame.pack(fill="both", expand=True, padx=25, pady=10)

    columns = (
        "Book ID",
        "Book Name",
        "Author",
        "Quantity"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=12
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=200)

    table.pack(fill="both", expand=True)

    # ---------- Select Row ----------

    def select_book(event):

        selected = table.focus()

        if not selected:
            return

        values = table.item(selected, "values")

        clear_fields()

        book_id_entry.insert(0, values[0])
        book_name_entry.insert(0, values[1])
        author_entry.insert(0, values[2])
        quantity_entry.insert(0, values[3])

    table.bind("<ButtonRelease-1>", select_book)

    load_books()