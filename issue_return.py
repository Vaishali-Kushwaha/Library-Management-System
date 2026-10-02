import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from database import get_connection


def open_issue_return(parent):

    window = tk.Toplevel(parent)
    window.title("Issue & Return Book")
    window.geometry("1000x650")
    window.configure(bg="#f4f6f8")

    # ---------- Header ----------

    header = tk.Label(
        window,
        text="Issue & Return Book",
        font=("Arial", 22, "bold"),
        bg="#243447",
        fg="white",
        pady=15
    )
    header.pack(fill="x")

    # ---------- Issue Section ----------

    issue_frame = tk.LabelFrame(
        window,
        text="Issue Book",
        font=("Arial", 12, "bold"),
        bg="#f4f6f8",
        padx=20,
        pady=15
    )
    issue_frame.pack(fill="x", padx=30, pady=20)

    tk.Label(
        issue_frame,
        text="Book ID:",
        font=("Arial", 11, "bold"),
        bg="#f4f6f8"
    ).grid(row=0, column=0, padx=10, pady=10)

    book_id_entry = tk.Entry(issue_frame, width=30)
    book_id_entry.grid(row=0, column=1, padx=10)

    tk.Label(
        issue_frame,
        text="Student Name:",
        font=("Arial", 11, "bold"),
        bg="#f4f6f8"
    ).grid(row=1, column=0, padx=10, pady=10)

    student_entry = tk.Entry(issue_frame, width=30)
    student_entry.grid(row=1, column=1, padx=10)

    def issue_book():

        book_id = book_id_entry.get().strip()
        student_name = student_entry.get().strip()

        if not book_id or not student_name:
            messagebox.showwarning(
                "Validation",
                "Please fill all fields."
            )
            return

        try:
            book_id = int(book_id)

            db = get_connection()
            cursor = db.cursor()

            cursor.execute(
                """
                SELECT book_id, book_name, quantity
                FROM books
                WHERE book_id=%s
                """,
                (book_id,)
            )

            book = cursor.fetchone()

            if not book:
                messagebox.showwarning(
                    "Not Found",
                    "Book ID not found."
                )
                cursor.close()
                db.close()
                return

            if book[2] <= 0:
                messagebox.showwarning(
                    "Unavailable",
                    "This book is currently unavailable."
                )
                cursor.close()
                db.close()
                return

            cursor.execute(
                """
                INSERT INTO transactions
                (book_id, student_name, issue_date, return_date, status)
                VALUES (%s, %s, %s, NULL, 'Issued')
                """,
                (book_id, student_name, date.today())
            )

            cursor.execute(
                """
                UPDATE books
                SET quantity = quantity - 1
                WHERE book_id=%s
                """,
                (book_id,)
            )

            db.commit()

            cursor.close()
            db.close()

            messagebox.showinfo(
                "Success",
                "Book issued successfully!"
            )

            book_id_entry.delete(0, tk.END)
            student_entry.delete(0, tk.END)

            load_transactions()

        except ValueError:
            messagebox.showwarning(
                "Validation",
                "Book ID must be a number."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    tk.Button(
        issue_frame,
        text="Issue Book",
        command=issue_book,
        width=18
    ).grid(row=2, column=0, columnspan=2, pady=10)

    # ---------- Return Section ----------

    return_frame = tk.LabelFrame(
        window,
        text="Return Book",
        font=("Arial", 12, "bold"),
        bg="#f4f6f8",
        padx=20,
        pady=15
    )
    return_frame.pack(fill="x", padx=30, pady=10)

    tk.Label(
        return_frame,
        text="Transaction ID:",
        font=("Arial", 11, "bold"),
        bg="#f4f6f8"
    ).grid(row=0, column=0, padx=10, pady=10)

    transaction_entry = tk.Entry(
        return_frame,
        width=30
    )
    transaction_entry.grid(row=0, column=1, padx=10)

    def return_book():

        transaction_id = transaction_entry.get().strip()

        if not transaction_id:
            messagebox.showwarning(
                "Validation",
                "Please enter Transaction ID."
            )
            return

        try:
            transaction_id = int(transaction_id)

            db = get_connection()
            cursor = db.cursor()

            cursor.execute(
                """
                SELECT transaction_id, book_id
                FROM transactions
                WHERE transaction_id=%s
                AND status='Issued'
                """,
                (transaction_id,)
            )

            transaction = cursor.fetchone()

            if not transaction:
                messagebox.showwarning(
                    "Not Found",
                    "Active transaction not found."
                )
                cursor.close()
                db.close()
                return

            book_id = transaction[1]

            cursor.execute(
                """
                UPDATE transactions
                SET return_date=%s, status='Returned'
                WHERE transaction_id=%s
                """,
                (date.today(), transaction_id)
            )

            cursor.execute(
                """
                UPDATE books
                SET quantity=quantity+1
                WHERE book_id=%s
                """,
                (book_id,)
            )

            db.commit()

            cursor.close()
            db.close()

            messagebox.showinfo(
                "Success",
                "Book returned successfully!"
            )

            transaction_entry.delete(0, tk.END)

            load_transactions()

        except ValueError:
            messagebox.showwarning(
                "Validation",
                "Transaction ID must be a number."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    tk.Button(
        return_frame,
        text="Return Book",
        command=return_book,
        width=18
    ).grid(row=1, column=0, columnspan=2, pady=10)

    # ---------- Transaction Table ----------

    table_frame = tk.Frame(window)
    table_frame.pack(fill="both", expand=True, padx=30, pady=15)

    columns = (
        "Transaction ID",
        "Book ID",
        "Student",
        "Issue Date",
        "Return Date",
        "Status"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=8
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=145)

    table.pack(fill="both", expand=True)

    def load_transactions():

        for item in table.get_children():
            table.delete(item)

        try:
            db = get_connection()
            cursor = db.cursor()

            cursor.execute(
                """
                SELECT
                    transaction_id,
                    book_id,
                    student_name,
                    issue_date,
                    return_date,
                    status
                FROM transactions
                ORDER BY transaction_id DESC
                """
            )

            records = cursor.fetchall()

            for record in records:
                table.insert(
                    "",
                    tk.END,
                    values=record
                )

            cursor.close()
            db.close()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    load_transactions()