import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection


def open_reports(parent):

    window = tk.Toplevel(parent)
    window.title("Library Reports")
    window.geometry("1050x650")
    window.configure(bg="#f4f6f8")

    # ---------- Header ----------

    header = tk.Label(
        window,
        text="Library Reports",
        font=("Arial", 22, "bold"),
        bg="#243447",
        fg="white",
        pady=15
    )
    header.pack(fill="x")

    # ---------- Buttons ----------

    button_frame = tk.Frame(
        window,
        bg="#f4f6f8"
    )
    button_frame.pack(pady=20)

    # ---------- Table ----------

    table_frame = tk.Frame(window)
    table_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=10
    )

    columns = (
        "Transaction ID",
        "Book Name",
        "Student",
        "Issue Date",
        "Return Date",
        "Status"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=160)

    table.pack(
        fill="both",
        expand=True
    )

    # ---------- Clear Table ----------

    def clear_table():

        for item in table.get_children():
            table.delete(item)

    # ---------- Available Books ----------

    def available_books():

        clear_table()

        try:
            db = get_connection()
            cursor = db.cursor()

            cursor.execute(
                """
                SELECT book_id, book_name, author, quantity
                FROM books
                WHERE quantity > 0
                """
            )

            records = cursor.fetchall()

            # Change table headings
            table["columns"] = (
                "Book ID",
                "Book Name",
                "Author",
                "Available Quantity"
            )

            for column in table["columns"]:
                table.heading(column, text=column)
                table.column(column, width=220)

            for record in records:
                table.insert(
                    "",
                    tk.END,
                    values=record
                )

            if not records:
                messagebox.showinfo(
                    "Report",
                    "No books are currently available."
                )

            cursor.close()
            db.close()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # ---------- Issued Books ----------

    def issued_books():

        clear_table()

        try:
            db = get_connection()
            cursor = db.cursor()

            cursor.execute(
                """
                SELECT
                    t.transaction_id,
                    b.book_name,
                    t.student_name,
                    t.issue_date,
                    t.return_date,
                    t.status
                FROM transactions t
                JOIN books b
                ON t.book_id = b.book_id
                WHERE t.status='Issued'
                ORDER BY t.transaction_id DESC
                """
            )

            records = cursor.fetchall()

            table["columns"] = columns

            for column in columns:
                table.heading(column, text=column)
                table.column(column, width=160)

            for record in records:
                table.insert(
                    "",
                    tk.END,
                    values=record
                )

            if not records:
                messagebox.showinfo(
                    "Report",
                    "No books are currently issued."
                )

            cursor.close()
            db.close()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # ---------- Complete Transactions ----------

    def all_transactions():

        clear_table()

        try:
            db = get_connection()
            cursor = db.cursor()

            cursor.execute(
                """
                SELECT
                    t.transaction_id,
                    b.book_name,
                    t.student_name,
                    t.issue_date,
                    t.return_date,
                    t.status
                FROM transactions t
                JOIN books b
                ON t.book_id = b.book_id
                ORDER BY t.transaction_id DESC
                """
            )

            records = cursor.fetchall()

            table["columns"] = columns

            for column in columns:
                table.heading(column, text=column)
                table.column(column, width=160)

            for record in records:
                table.insert(
                    "",
                    tk.END,
                    values=record
                )

            if not records:
                messagebox.showinfo(
                    "Report",
                    "No transaction records found."
                )

            cursor.close()
            db.close()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # ---------- Buttons ----------

    tk.Button(
        button_frame,
        text="Available Books",
        command=available_books,
        width=20
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        button_frame,
        text="Issued Books",
        command=issued_books,
        width=20
    ).grid(row=0, column=1, padx=10)

    tk.Button(
        button_frame,
        text="All Transactions",
        command=all_transactions,
        width=20
    ).grid(row=0, column=2, padx=10)

    tk.Button(
        button_frame,
        text="Clear",
        command=clear_table,
        width=15
    ).grid(row=0, column=3, padx=10)