import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from database import get_connection
from book_management import open_book_management
from issue_return import open_issue_return
from reports import open_reports


def open_search():

    window = tk.Toplevel(root)
    window.title("Search Book")
    window.geometry("850x550")
    window.configure(bg="#f4f6f8")

    # Header
    header = tk.Label(
        window,
        text="Search Book",
        font=("Arial", 22, "bold"),
        bg="#243447",
        fg="white",
        pady=15
    )
    header.pack(fill="x")

    # Search Area
    search_frame = tk.Frame(
        window,
        bg="#f4f6f8"
    )
    search_frame.pack(pady=25)

    tk.Label(
        search_frame,
        text="Enter Book ID, Book Name or Author:",
        font=("Arial", 11, "bold"),
        bg="#f4f6f8"
    ).pack(side="left", padx=10)

    search_entry = tk.Entry(
        search_frame,
        width=30
    )
    search_entry.pack(side="left", padx=10)

    # Table
    table_frame = tk.Frame(window)
    table_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=10
    )

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
        height=15
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=190)

    table.pack(
        fill="both",
        expand=True
    )

    def search_book():

        keyword = search_entry.get().strip()

        for item in table.get_children():
            table.delete(item)

        if not keyword:
            messagebox.showwarning(
                "Validation",
                "Please enter something to search."
            )
            return

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
                table.insert(
                    "",
                    tk.END,
                    values=record
                )

            cursor.close()
            db.close()

            if not records:
                messagebox.showinfo(
                    "Search",
                    "No matching book found."
                )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    tk.Button(
        search_frame,
        text="Search",
        command=search_book,
        width=12
    ).pack(side="left", padx=5)

    tk.Button(
        search_frame,
        text="Clear",
        command=lambda: [
            search_entry.delete(0, tk.END),
            [table.delete(item) for item in table.get_children()]
        ],
        width=12
    ).pack(side="left", padx=5)


def exit_application():
    if messagebox.askyesno("Exit", "Do you want to exit?"):
        root.destroy()


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Library Management System")
root.geometry("900x600")
root.resizable(False, False)
root.configure(bg="#f4f6f8")


# ---------------- HEADER ----------------

header = tk.Frame(root, bg="#243447", height=100)
header.pack(fill="x")

title = tk.Label(
    header,
    text="LIBRARY MANAGEMENT SYSTEM",
    font=("Arial", 24, "bold"),
    bg="#243447",
    fg="white"
)
title.pack(pady=(20, 5))

subtitle = tk.Label(
    header,
    text="Book Management • Issue & Return • Search • Reports",
    font=("Arial", 11),
    bg="#243447",
    fg="white"
)
subtitle.pack()


# ---------------- DASHBOARD ----------------

welcome = tk.Label(
    root,
    text="Library Dashboard",
    font=("Arial", 20, "bold"),
    bg="#f4f6f8",
    fg="#243447"
)
welcome.pack(pady=30)


button_frame = tk.Frame(root, bg="#f4f6f8")
button_frame.pack()


def create_button(text, command, row, column):
    button = tk.Button(
        button_frame,
        text=text,
        command=command,
        width=24,
        height=3,
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#243447",
        relief="raised",
        cursor="hand2"
    )
    button.grid(row=row, column=column, padx=20, pady=15)


create_button(
    "📚  Book Management",
    lambda: open_book_management(root),
    0,
    0
)

create_button(
    "📤  Issue / Return Book",
    lambda: open_issue_return(root),
    0,
    1
)

create_button(
    "🔍  Search Book",
    open_search,
    1,
    0
)

create_button(
    "📊  Reports",
    lambda: open_reports(root),
    1,
    1
)

create_button(
    "❌  Exit",
    exit_application,
    2,
    0
)


# ---------------- FOOTER ----------------

footer = tk.Label(
    root,
    text="Python + Tkinter + MySQL",
    font=("Arial", 10),
    bg="#f4f6f8",
    fg="gray"
)
footer.pack(side="bottom", pady=20)


root.mainloop()