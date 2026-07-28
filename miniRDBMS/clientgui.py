import tkinter as tk
import socket
import json
from tkinter import messagebox
from tkinter import simpledialog

SERVER_HOST = "localhost"
SERVER_PORT = 12345

def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST,SERVER_PORT))
        s.sendall(json.dumps(command).encode())

        # Olvasás chunks-ban
        chunks = []
        while True:
            chunk = s.recv(8192)
            if not chunk:
                break
            chunks.append(chunk)

        response_data = b''.join(chunks)
        return response_data.decode()


root = tk.Tk() 
root.title("Mini ABKR")
root.geometry("1920x1080+0+0")
root.configure(bg="#6DCE6D")
default_bg = "#95e793"
default_fg = "black"
highlight = "#007acc"

default_font = ("Segoe UI", 12)


valassz_label = tk.Label(root, text="Choose an operation!", font=("Arial", 18,"bold"), bg="#95e793", fg="black")
valassz_label.pack(pady=10)


dropdown_frame = tk.Frame(root)
dropdown_frame.pack(pady=5)
dropdown_frame.configure(bg="#95e793")

db_ops = ["CREATE_DATABASE", "DROP_DATABASE", "CREATE_TABLE", "DROP_TABLE", "CREATE_INDEX"]
selected_db_op = tk.StringVar(value=db_ops[0])

tk.Label(dropdown_frame, text="database/table:", bg=default_bg, fg=default_fg, font=default_font).grid(row=0, column=0, padx=10)

option = tk.OptionMenu(dropdown_frame, selected_db_op, *db_ops)
option.config(bg="white", fg="black", font=default_font, activebackground="#cce6ff")
option.grid(row=1, column=0, padx=10)

def handle_db_op_change(*args):
    selected = selected_db_op.get()
    if selected == "CREATE_DATABASE":
        open_create_database_window()
    elif selected == "CREATE_TABLE":
        open_create_table_window()
    elif selected == "CREATE_TABLE":
        open_create_table_window()
    elif selected == "DROP_TABLE":
        open_drop_table_window()
    elif selected == "DROP_DATABASE":
        open_drop_database_window()
    elif selected == "CREATE_INDEX":
        open_create_index_window()


selected_db_op.trace_add("write", handle_db_op_change) 

record_ops = ["INSERT", "DELETE", "SELECT", "JOIN_SELECT"]
selected_record_op = tk.StringVar(value=record_ops[0])

tk.Label(dropdown_frame, text="Record operation:", bg=default_bg, fg=default_fg, font=default_font).grid(row=0, column=1, padx=10)

record_option = tk.OptionMenu(dropdown_frame, selected_record_op, *record_ops)
record_option.config(bg="white", fg="black", font=default_font, activebackground="#cce6ff")
record_option.grid(row=1, column=1, padx=10)

def handle_record_op_change(*args):
    selected = selected_record_op.get()
    if selected == "INSERT":
        open_insert_window()
    elif selected == "DELETE":
        open_delete_window()
    elif selected == "SELECT":
        open_select_window()
    elif selected == "JOIN_SELECT":
        open_join_select_window()

selected_record_op.trace_add("write", handle_record_op_change) 

list_ops = ["LIST_DATABASES", "LIST_TABLES"]
selected_list_op = tk.StringVar(value=list_ops[0])
tk.Label(dropdown_frame, text="Listing:", bg=default_bg, fg=default_fg, font=default_font).grid(row=0, column=2, padx=10)

list_option = tk.OptionMenu(dropdown_frame, selected_list_op, *list_ops)
list_option.config(bg="white", fg="black", font=default_font, activebackground="#cce6ff")
list_option.grid(row=1, column=2, padx=10)

def handle_list_op_change(*args):
    selected = selected_list_op.get()
    if selected == "LIST_DATABASES":
        list_databases()
    elif selected == "LIST_TABLES":
        list_tables()

selected_list_op.trace_add("write", handle_list_op_change) 

def open_create_database_window():
    window = tk.Toplevel(root) 
    window.title("CREATE DATABASE")

    tk.Label(window, text="Database name:", font=default_font, bg=default_bg, fg=default_fg).pack(padx=10, pady=(15, 5))
    db_entry = tk.Entry(window, width=40, bg="white", fg="black", font=default_font)
    db_entry.pack(padx=10, pady=(0, 10))


    def submit_create_database():
        db_name = db_entry.get().strip()
        if not db_name:
            messagebox.showerror("Missing data", "Enter database name")
            return

        command = {
            "action": "CREATE_DATABASE",
            "db_name": db_name
        }

        handle_submit_command(command, window)

    tk.Button(window, text="Create", command=submit_create_database,
        bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack(pady=(5, 10))

#CREATE TABLE
def open_create_table_window():
    window = tk.Toplevel(root)
    window.title("CREATE TABLE")
    
    tk.Label(window, text="Database name", bg=default_bg, fg=default_fg, font=default_font).pack()
    db_entry = tk.Entry(window, width=40, bg="white", fg="black", font=default_font)
    db_entry.pack(pady=2)

    
    tk.Label(window, text="Table name:", bg=default_bg, fg=default_fg, font=default_font).pack()
    table_entry = tk.Entry(window, width=40, bg="white", fg="black", font=default_font)
    table_entry.pack(pady=2)

    
    column_entries = []

    columns_container = tk.Frame(window) 
    columns_container.pack(pady=(10, 5)) 

    tk.Label(columns_container, text="Columns (Type + Name)", bg=default_bg, fg=default_fg, font=default_font).grid(row=0, column=0, columnspan=3)

    def add_column_field():
        row = len(column_entries) + 1

        col_type = tk.Entry(columns_container, width=15, bg="white", fg="black", font=default_font)
        col_name = tk.Entry(columns_container, width=20, bg="white", fg="black", font=default_font)

        tk.Label(columns_container, text=f"column {row}:", bg=default_bg, fg=default_fg, font=default_font).grid(row=row, column=0, padx=5, pady=2)

        col_type.grid(row=row, column=1, padx=5)
        col_name.grid(row=row, column=2, padx=5)

        column_entries.append((col_name, col_type))

    add_column_field()

    tk.Button(window, text="Add new column", command=add_column_field,
          bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack(pady=(0, 10))

    #unique
    tk.Label(window, text="UNIQUE key(s)", bg=default_bg, fg=default_fg, font=default_font).pack(pady=(10, 0))
    unique_frame = tk.Frame(window)
    unique_frame.pack()
    unique_entries = []

    def add_unique_field():
            row = len(unique_entries)
            typ_entry = tk.Entry(unique_frame, width=15, bg="white", fg="black", font=default_font)
            name_entry = tk.Entry(unique_frame, width=20, bg="white", fg="black", font=default_font)

            tk.Label(unique_frame, text=f"{row+1}. Type:", bg=default_bg, fg=default_fg, font=default_font).grid(row=row, column=0, padx=5, pady=2)
            typ_entry.grid(row=row, column=1, padx=5)
            tk.Label(unique_frame, text="Column name:", bg=default_bg, fg=default_fg, font=default_font).grid(row=row, column=2, padx=5)
            name_entry.grid(row=row, column=3, padx=5)


            unique_entries.append((name_entry, typ_entry))

    add_unique_field()
    tk.Button(window, text="New UNIQUE key", command=add_unique_field,
          bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack()


    tk.Label(window, text="FOREIGN key(s)", bg=default_bg, fg=default_fg, font=default_font).pack(pady=(10, 0))
    foreign_frame = tk.Frame(window)
    foreign_frame.pack()
    foreign_entries = []

    def add_foreign_field():
        row = len(foreign_entries)

        fk_col = tk.Entry(foreign_frame, width=10, bg="white", fg="black", font=default_font)
        fk_typ = tk.Entry(foreign_frame, width=10, bg="white", fg="black", font=default_font)
        ref_table = tk.Entry(foreign_frame, width=10, bg="white", fg="black", font=default_font)
        ref_col = tk.Entry(foreign_frame, width=10, bg="white", fg="black", font=default_font)

        tk.Label(foreign_frame, text=f"{row+1}. FK column:", bg=default_bg, fg=default_fg, font=default_font).grid(row=row, column=0, padx=2)
        fk_col.grid(row=row, column=1)
        tk.Label(foreign_frame, text="Type:", bg=default_bg, fg=default_fg, font=default_font).grid(row=row, column=2)
        fk_typ.grid(row=row, column=3)
        tk.Label(foreign_frame, text="Ref. table:", bg=default_bg, fg=default_fg, font=default_font).grid(row=row, column=4)
        ref_table.grid(row=row, column=5)
        tk.Label(foreign_frame, text="Ref. column:", bg=default_bg, fg=default_fg, font=default_font).grid(row=row, column=6)
        ref_col.grid(row=row, column=7)


        foreign_entries.append((fk_col, fk_typ, ref_table, ref_col))

    add_foreign_field()
    tk.Button(window, text="New FOREIGN key", command=add_foreign_field,
          bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack()

    def submit_create_table():
        db_name = db_entry.get().strip()
        table_name = table_entry.get().strip()

        if not db_name or not table_name:
            messagebox.showerror("Missing data", "Fill in the name of teh database and table")
            return

        columns = {}
        unique_keys = []
        foreign_keys = {}

        first_column = True
        for name_entry, type_entry in column_entries:
            name = name_entry.get().strip()
            typ = type_entry.get().strip()
            if name and typ:
                    columns[name] = typ

        # UNIQUE
        for name_entry, type_entry in unique_entries:
            name = name_entry.get().strip()
            typ = type_entry.get().strip()
            if name and typ:
                unique_keys.append(name)
                columns[name] = typ


       # FOREIGN
        for fk_col_entry, fk_type_entry, ref_table_entry, ref_col_entry in foreign_entries:
            fk_col = fk_col_entry.get().strip()
            fk_type = fk_type_entry.get().strip()
            ref_table = ref_table_entry.get().strip()
            ref_col = ref_col_entry.get().strip()
            if fk_col and fk_type and ref_table and ref_col:
                foreign_keys[fk_col] = {"ref_table": ref_table, "ref_column": ref_col}
                columns[fk_col] = fk_type


        command = {
            "action": "CREATE_TABLE",
            "db_name": db_name,
            "table_name": table_name,
            "columns": columns,
            "unique_keys": unique_keys,
            "foreign_keys": foreign_keys
        }

        handle_submit_command(command, window)

    tk.Button(window, text="create table", command=submit_create_table,
          bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack(pady=15)

    #drop database
def open_drop_database_window():
        window = tk.Toplevel(root)
        window.title("DROP DATABASE")

        tk.Label(window, text="Database name:", bg=default_bg, fg=default_fg, font=default_font).pack(pady=10)
        db_entry = tk.Entry(window, width=40, bg="white", fg="black", font=default_font)
        db_entry.pack(pady=5)


        def submit():
            db_name = db_entry.get().strip()
            if not db_name:
                messagebox.showerror("Missing data", "Fill in the database name")
                return
            command = {"action": "DROP_DATABASE", "db_name": db_name}
            handle_submit_command(command, window)

        tk.Button(window, text="Delete", command=submit,
          bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack(pady=10)

    #drop table
def open_drop_table_window():
        window = tk.Toplevel(root)
        window.title("DROP TABLE")

        tk.Label(window, text="Database name:").pack(pady=5)
        db_entry = tk.Entry(window, width=40)
        db_entry.pack(pady=2)

        tk.Label(window, text="Table name:").pack(pady=5)
        table_entry = tk.Entry(window, width=40)
        table_entry.pack(pady=2)


        def submit():
            db = db_entry.get().strip()
            table = table_entry.get().strip()
            if not db or not table:
                messagebox.showerror("Missing data", "Töltsd ki mindkét mezőt.")
                return
            command = {"action": "DROP_TABLE", "db_name": db, "table_name": table}
            handle_submit_command(command, window)

        tk.Button(window, text="Tábla törlése", command=submit,
          bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack(pady=10)

#index letrehozas
def open_create_index_window():
    window = tk.Toplevel(root)
    window.title("CREATE INDEX")

    tk.Label(window, text="Database name:", bg=default_bg, fg=default_fg, font=default_font).pack()
    db_entry = tk.Entry(window, width=40, bg="white", fg="black", font=default_font)
    db_entry.pack()

    tk.Label(window, text="Table name:", bg=default_bg, fg=default_fg, font=default_font).pack()
    table_entry = tk.Entry(window, width=40, bg="white", fg="black", font=default_font)
    table_entry.pack()

    tk.Label(window, text="column neve (indexelendő):", bg=default_bg, fg=default_fg, font=default_font).pack()
    col_entry = tk.Entry(window, width=40, bg="white", fg="black", font=default_font)
    col_entry.pack()


    def submit():
        db = db_entry.get().strip()
        table = table_entry.get().strip()
        col = col_entry.get().strip()

        if not db or not table or not col:
            messagebox.showerror("Missing data", "Fill in all 3 fields.")
            return

        command = {
            "action": "CREATE_INDEX",
            "db_name": db,
            "table_name": table,
            "column_name": col
        }

        handle_submit_command(command, window)

    tk.Button(window, text="Create index", command=submit,
          bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack(pady=10)

#insert
def open_insert_window():
    window = tk.Toplevel(root)
    window.title("INSERT")

    tk.Label(window, text="Database name:", bg=default_bg, fg=default_fg, font=default_font).pack()
    db_entry = tk.Entry(window, width=40, bg="white", fg="black", font=default_font)
    db_entry.pack()

    tk.Label(window, text="Table name:", bg=default_bg, fg=default_fg, font=default_font).pack()
    table_entry = tk.Entry(window, width=40, bg="white", fg="black", font=default_font)
    table_entry.pack()

    columns_container = tk.Frame(window, bg=default_bg)
    columns_container.pack(pady=10)


    value_entries = []  # [(col_name_entry, value_entry)]

    def add_column_value_field():
        row = len(value_entries)
        col_entry = tk.Entry(columns_container, width=20, bg="white", fg="black", font=default_font)
        val_entry = tk.Entry(columns_container, width=20, bg="white", fg="black", font=default_font)

        tk.Label(columns_container, text=f"{row+1}. column:", bg=default_bg, fg=default_fg, font=default_font).grid(row=row, column=0, padx=5, pady=2)

        col_entry.grid(row=row, column=1, padx=5)
        val_entry.grid(row=row, column=2, padx=5)

        value_entries.append((col_entry, val_entry))

    # Kezdetben egy mezőpár legyen
    add_column_value_field()

    tk.Button(window, text="Add new field", command=add_column_value_field,
          bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack(pady=(0, 10))

    def submit():
        db = db_entry.get().strip()
        table = table_entry.get().strip()

        if not db or not table:
            messagebox.showerror("Missing data", "Fill in the name of the database and table.")
            return

        if not value_entries:
            messagebox.showerror("Missing fields", "Pick at least one column.")
            return

        values = []

        for i, (col_entry, val_entry) in enumerate(value_entries):
            col = col_entry.get().strip()
            val = val_entry.get().strip()
            if not col or not val:
                messagebox.showerror("Missing data", f"The {i+1}. field is not filled out completely.")
                return
            values.append(val)

        key = values[0]  
        command = {
            "action": "INSERT",
            "db_name": db,
            "table_name": table,
            "key": key,
            "value": "#".join(values)  
        }

        response = send_command(command)

        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, response)

        for _, val_entry in value_entries:
            val_entry.delete(0, tk.END)

    tk.Button(window, text="Insert", command=submit,
          bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack(pady=10)


    
#delete
def open_delete_window():
    window = tk.Toplevel(root)
    window.title("DELETE")

    
    tk.Label(window, text="Database name:", bg=default_bg, fg=default_fg, font=default_font).pack()
    db_entry = tk.Entry(window, width=40, bg="white", fg="black", font=default_font)
    db_entry.pack()

    tk.Label(window, text="Table name:", bg=default_bg, fg=default_fg, font=default_font).pack()
    table_entry = tk.Entry(window, width=40, bg="white", fg="black", font=default_font)
    table_entry.pack()

    
    columns_container = tk.Frame(window)
    columns_container.pack(pady=10)

    tk.Label(columns_container, text="Key of the deleted record (first column)",
          bg=default_bg, fg=default_fg, font=default_font).grid(row=0, column=0, columnspan=2)

    value_entries = []

    def add_column_field():
        row = len(value_entries) + 1
        col_name_entry = tk.Entry(columns_container, width=20, bg="white", fg="black", font=default_font)
        value_entry = tk.Entry(columns_container, width=20, bg="white", fg="black", font=default_font)

        tk.Label(columns_container, text=f"{row}. column:", bg=default_bg, fg=default_fg, font=default_font).grid(row=row, column=0, padx=5, pady=2)
        col_name_entry.grid(row=row, column=1, padx=5)
        value_entry.grid(row=row, column=2, padx=5)


        value_entries.append((col_name_entry, value_entry))

    add_column_field()

    tk.Button(window, text="Create new column", command=add_column_field,
          bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack(pady=(0, 10))

    def submit():
        db = db_entry.get().strip()
        table = table_entry.get().strip()

        if not db or not table:
            messagebox.showerror("Missing data", "Fill in the name of the database and table.")
            return

        if not value_entries:
            messagebox.showerror("Missing key", "Select at least one column to delete.")
            return

        pk_value = value_entries[0][1].get().strip()
        if not pk_value:
            messagebox.showerror("Missing key value", "The value of the first column (key).")
            return

        command = {
            "action": "DELETE",
            "db_name": db,
            "table_name": table,
            "key": pk_value
        }

        handle_submit_command(command, window)

    tk.Button(window, text="Delete", command=submit,
          bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack(pady=10)


#select
def open_select_window():
    window = tk.Toplevel(root)
    window.title("SELECT")
    default_font = ("Arial", 8)

    tk.Label(window, text="Database name:", bg=default_bg, fg=default_fg, font=default_font).pack()
    db_entry = tk.Entry(window, width=40, bg="white", fg="black", font=default_font)
    db_entry.pack()

    tk.Label(window, text="Table name:", bg=default_bg, fg=default_fg, font=default_font).pack()
    table_entry = tk.Entry(window, width=40, bg="white", fg="black", font=default_font)
    table_entry.pack()

    column_frame = tk.Frame(window)
    column_frame.pack(pady=10)
    tk.Label(column_frame, text="Selected columns", bg=default_bg, fg=default_fg, font=default_font).grid(row=0, column=0, columnspan=2)

    column_entries = []
    def add_column_field():
        row = len(column_entries) + 1
        col_entry = tk.Entry(column_frame, width=30, bg="white", fg="black", font=default_font)
        tk.Label(column_frame, text=f"{row}. column:", bg=default_bg, fg=default_fg, font=default_font).grid(row=row, column=0, padx=5, pady=2)
        col_entry.grid(row=row, column=1, padx=5)
        column_entries.append(col_entry)
    add_column_field()
    tk.Button(window, text="Add new column", command=add_column_field, bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack()

    condition_frame = tk.Frame(window)
    condition_frame.pack(pady=10)
    tk.Label(condition_frame, text="WHERE causes (optional)", bg=default_bg, fg=default_fg, font=default_font).grid(row=0, column=0, columnspan=4)
    condition_entries = []
    def add_condition_field():
        row = len(condition_entries) + 1
        col_entry = tk.Entry(condition_frame, width=15, bg="white", fg="black", font=default_font)
        op_entry = tk.Entry(condition_frame, width=5, bg="white", fg="black", font=default_font)
        val_entry = tk.Entry(condition_frame, width=15, bg="white", fg="black", font=default_font)
        tk.Label(condition_frame, text=f"{row}. cause:", bg=default_bg, fg=default_fg, font=default_font).grid(row=row, column=0, padx=5, pady=2)
        col_entry.grid(row=row, column=1)
        op_entry.grid(row=row, column=2)
        val_entry.grid(row=row, column=3)
        condition_entries.append((col_entry, op_entry, val_entry))
    add_condition_field()
    tk.Button(window, text="New WHERE cause", command=add_condition_field, bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack()

    group_frame = tk.LabelFrame(window, text="GROUP BY (optional)", bg=default_bg, fg=default_fg, font=default_font)
    group_frame.pack(pady=10)
    tk.Label(group_frame, text="GROUP BY column:", bg=default_bg, fg=default_fg, font=default_font).grid(row=0, column=0)
    group_col_entry = tk.Entry(group_frame, width=30, bg="white", fg="black", font=default_font)
    group_col_entry.grid(row=0, column=1)

    aggregate_entries = []
    def add_aggregate_field():
        row = len(aggregate_entries)
        col_entry = tk.Entry(group_frame, width=20, bg="white", fg="black", font=default_font)
        op_var = tk.StringVar()
        op_var.set("COUNT")
        op_menu = tk.OptionMenu(group_frame, op_var, "COUNT", "SUM", "AVG", "MIN", "MAX")
        col_entry.grid(row=row + 1, column=0, padx=5, pady=2)
        op_menu.grid(row=row + 1, column=1, padx=5, pady=2)
        aggregate_entries.append((col_entry, op_var))
    add_aggregate_field()
    tk.Button(group_frame, text="New aggregation field", command=add_aggregate_field, bg=highlight, fg="white", activebackground="#005f99", font=default_font).grid(row=99, column=0, columnspan=2, pady=5)

    order_frame = tk.LabelFrame(window, text="ORDER BY (optional)", bg=default_bg, fg=default_fg, font=default_font)
    order_frame.pack(pady=10)
    tk.Label(order_frame, text="ORDER BY column:", bg=default_bg, fg=default_fg, font=default_font).grid(row=0, column=0)
    order_col_entry = tk.Entry(order_frame, width=20, bg="white", fg="black", font=default_font)
    order_col_entry.grid(row=0, column=1)
    tk.Label(order_frame, text="Descending sort:", bg=default_bg, fg=default_fg, font=default_font).grid(row=1, column=0)
    desc_var = tk.BooleanVar()
    tk.Checkbutton(order_frame, variable=desc_var, bg=default_bg).grid(row=1, column=1, sticky="w")

    having_frame = tk.LabelFrame(window, text="HAVING (optional)", bg=default_bg, fg=default_fg, font=default_font)
    having_frame.pack(pady=10)
    tk.Label(having_frame, text="Aggregated column:", bg=default_bg, fg=default_fg, font=default_font).grid(row=0, column=0)
    having_col_entry = tk.Entry(having_frame, width=20, bg="white", fg="black", font=default_font)
    having_col_entry.grid(row=0, column=1)
    tk.Label(having_frame, text="Operator:", bg=default_bg, fg=default_fg, font=default_font).grid(row=1, column=0)
    having_op_entry = tk.Entry(having_frame, width=10, bg="white", fg="black", font=default_font)
    having_op_entry.grid(row=1, column=1)
    tk.Label(having_frame, text="Value:", bg=default_bg, fg=default_fg, font=default_font).grid(row=2, column=0)
    having_val_entry = tk.Entry(having_frame, width=20, bg="white", fg="black", font=default_font)
    having_val_entry.grid(row=2, column=1)

    def submit():
        db = db_entry.get().strip()
        table = table_entry.get().strip()
        
        if not db or not table:
            messagebox.showerror("Missing data", "Fill inthe name of the database and table.")
            return

        columns = [e.get().strip() for e in column_entries if e.get().strip()]
        if not columns:
            columns = ["*"]
        conditions = []
        for col_entry, op_entry, val_entry in condition_entries:
            col, op, val = col_entry.get().strip(), op_entry.get().strip(), val_entry.get().strip()
            if col and op and val:
                conditions.append({"column": col, "operator": op, "value": val})

        command = {
            "action": "SELECT",
            "db_name": db,
            "table_name": table,
            "columns": columns,
            "conditions": conditions
        }

        group_col = group_col_entry.get().strip()
        aggregates = []
        for col_entry, op_var in aggregate_entries:
            col = col_entry.get().strip()
            op = op_var.get().strip().upper()
            if col and op:
                aggregates.append({"agg_column": col, "operation": op})
        if group_col and aggregates:
            command["group_by"] = {"group_column": group_col, "aggregates": aggregates}

        order_col = order_col_entry.get().strip()
        if order_col:
            command["order_by"] = {"column": order_col, "desc": desc_var.get()}

        having_col = having_col_entry.get().strip()
        having_op = having_op_entry.get().strip()
        having_val = having_val_entry.get().strip()
        if having_col and having_op and having_val:
            command["having"] = {
                "column": having_col,
                "operator": having_op,
                "value": having_val
            }

        response = handle_submit_command(command, None, return_response=True)
        lines = response.strip().splitlines()
        if len(lines) > 100:
            with open("query_output.txt", "w", encoding="utf-8") as f:
                f.write(response)
            messagebox.showinfo("Large amount of data", f"{len(lines)} rows returned — saved to 'query_output.txt'.")
        else:
            output_box.delete("1.0", tk.END)
            output_box.insert(tk.END, response)

        window.destroy()

    tk.Button(window, text="Query", command=submit, bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack(pady=10)


def list_databases():
    command = {"action": "LIST_DATABASES"}
    response = send_command(command)

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Existing databases:\n" + response)

def list_tables():
    window = tk.Toplevel(root)
    window.title("LIST TABLES")

    tk.Label(window, text="Database name:", bg=default_bg, fg=default_fg, font=default_font).pack(pady=5)
    db_entry = tk.Entry(window, width=40, bg="white", fg="black", font=default_font)
    db_entry.pack(pady=5)


    def submit():
        db_name = db_entry.get().strip()
        if not db_name:
            messagebox.showerror("Missing data", "Fill in the name of the database.")
            return

        command = {
            "action": "LIST_TABLES",
            "db_name": db_name
        }
        response = send_command(command)

        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"Tables in '{db_name}' database:\n" + response)
        window.destroy()

    tk.Button(window, text="Select", command=submit,
          bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack(pady=10)


def open_join_select_window():
    window = tk.Toplevel(root)
    window.geometry("1920x1080")
    window.resizable(True,True)
    default_font = ("Arial", 8)  

    window.title("JOIN SELECT")

    tk.Label(window, text="Database name:").pack()
    db_entry = tk.Entry(window, width=40)
    db_entry.pack()

    tk.Label(window, text="Tables separated by commas (pl. A,B):").pack()
    tables_entry = tk.Entry(window, width=40)
    tables_entry.pack()

    join_conditions_frame = tk.Frame(window)
    join_conditions_frame.pack(pady=0)
    tk.Label(join_conditions_frame, text="JOIN conditions (A.c1 = B.c2)").pack()

    join_entries = []

    def add_join_condition():
        frame = tk.Frame(join_conditions_frame, bg=default_bg)
        frame.pack(pady=2)

        left_table = tk.Entry(frame, width=10, bg="white", fg="black", font=default_font)
        left_col = tk.Entry(frame, width=10, bg="white", fg="black", font=default_font)
        right_table = tk.Entry(frame, width=10, bg="white", fg="black", font=default_font)
        right_col = tk.Entry(frame, width=10, bg="white", fg="black", font=default_font)

        tk.Label(frame, text="LEFT Table", bg=default_bg, fg=default_fg, font=default_font).grid(row=0, column=0)
        left_table.grid(row=0, column=1)
        tk.Label(frame, text="Column", bg=default_bg, fg=default_fg, font=default_font).grid(row=0, column=2)
        left_col.grid(row=0, column=3)
        tk.Label(frame, text="RIGHT Table", bg=default_bg, fg=default_fg, font=default_font).grid(row=0, column=4)
        right_table.grid(row=0, column=5)
        tk.Label(frame, text="Column", bg=default_bg, fg=default_fg, font=default_font).grid(row=0, column=6)
        right_col.grid(row=0, column=7)

        join_entries.append((left_table, left_col, right_table, right_col))

    add_join_condition()
    tk.Button(window, text="+ JOIN condition", command=add_join_condition,
              bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack(pady=5)

    tk.Label(window, text="selected columns (* = all):", bg=default_bg, fg=default_fg, font=default_font).pack()
    columns_entry = tk.Entry(window, width=40, bg="white", fg="black", font=default_font)
    columns_entry.pack()
    columns_entry.insert(0, "*")

    where_frame = tk.Frame(window, bg=default_bg)
    where_frame.pack(pady=0)
    condition_entries = {}

    def add_where_for_table():
        tname = simpledialog.askstring("Table name", "To which table do you want to give WHERE conditions?")
        if not tname:
            return
        container = tk.Frame(where_frame, bg=default_bg)
        container.pack(pady=2, anchor="w")

        tk.Label(container, text=f"{tname} WHERE:", font=default_font, bg=default_bg, fg=default_fg).grid(row=0, column=0, padx=0, sticky="w")

        frame = tk.Frame(container, bg=default_bg)
        frame.grid(row=0, column=1)

        entries = []

        def add_row():
            row = len(entries)
            col = tk.Entry(frame, width=12, bg="white", fg="black", font=default_font)
            op = tk.Entry(frame, width=5, bg="white", fg="black", font=default_font)
            val = tk.Entry(frame, width=12, bg="white", fg="black", font=default_font)
            add_btn = tk.Button(frame, text="+", command=add_row,
                        bg=highlight, fg="white", font=default_font, width=3)
            col.grid(row=row, column=0, padx=0, pady=0)
            op.grid(row=row, column=1, padx=0, pady=0)
            val.grid(row=row, column=2, padx=0)
            add_btn.grid(row=row, column=3, padx=4)
            entries.append((col, op, val))

        add_row()
        
        condition_entries[tname] = entries

    tk.Button(window, text="add WHERE to table", command=add_where_for_table,
              bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack(pady=0)

    group_frame = tk.LabelFrame(window, text="GROUP BY (optional)", bg=default_bg, fg=default_fg, font=default_font)
    group_frame.pack(pady=0)

    tk.Label(group_frame, text="GROUP BY column:", bg=default_bg, fg=default_fg, font=default_font).grid(row=0, column=0, padx=5, pady=2)
    group_col_entry = tk.Entry(group_frame, width=20, bg="white", fg="black", font=default_font)
    group_col_entry.grid(row=0, column=1)

    aggregate_entries = []
    def add_aggregate_field():
        row = len(aggregate_entries) + 1
        col_entry = tk.Entry(group_frame, width=10, bg="white", fg="black", font=default_font)
        op_var = tk.StringVar()
        op_var.set("COUNT")
        op_menu = tk.OptionMenu(group_frame, op_var, "COUNT", "SUM", "AVG", "MIN", "MAX")
        col_entry.grid(row=row, column=0, padx=0, pady=0)
        op_menu.grid(row=row, column=1, padx=0, pady=0)
        aggregate_entries.append((col_entry, op_var))

    add_aggregate_field()
    tk.Button(group_frame, text="New aggregation field", command=add_aggregate_field,
              bg=highlight, fg="white", activebackground="#005f99", font=default_font).grid(row=99, column=0, columnspan=2, pady=0)

    order_frame = tk.LabelFrame(window, text="ORDER BY (optional)", bg=default_bg, fg=default_fg, font=default_font)
    order_frame.pack(pady=0)

    tk.Label(order_frame, text="ORDER BY column:", bg=default_bg, fg=default_fg, font=default_font).grid(row=0, column=0, padx=0, pady=1)
    order_col_entry = tk.Entry(order_frame, width=10, bg="white", fg="black", font=default_font)
    order_col_entry.grid(row=0, column=1)

    tk.Label(order_frame, text="Descending query:", bg=default_bg, fg=default_fg, font=default_font).grid(row=1, column=0, padx=0, pady=1)
    desc_var = tk.BooleanVar()
    desc_check = tk.Checkbutton(order_frame, variable=desc_var, bg=default_bg)
    desc_check.grid(row=1, column=1, sticky="w")

    having_frame = tk.LabelFrame(window, text="HAVING (optional)", bg=default_bg, fg=default_fg, font=default_font)
    having_frame.pack(pady=1)

    tk.Label(having_frame, text="Aggregated column:", bg=default_bg, fg=default_fg, font=default_font).grid(row=0, column=0)
    having_col_entry = tk.Entry(having_frame, width=10, bg="white", fg="black", font=default_font)
    having_col_entry.grid(row=0, column=1)
    tk.Label(having_frame, text="Operator:", bg=default_bg, fg=default_fg, font=default_font).grid(row=1, column=0)
    having_op_entry = tk.Entry(having_frame, width=5, bg="white", fg="black", font=default_font)
    having_op_entry.grid(row=1, column=1)
    tk.Label(having_frame, text="Value:", bg=default_bg, fg=default_fg, font=default_font).grid(row=2, column=0)
    having_val_entry = tk.Entry(having_frame, width=10, bg="white", fg="black", font=default_font)
    having_val_entry.grid(row=2, column=1)

    def submit():
        db = db_entry.get().strip()
        tables = [t.strip() for t in tables_entry.get().split(",") if t.strip()]
        columns = [c.strip() for c in columns_entry.get().split(",") if c.strip()]
        if not db or not tables or not columns:
            messagebox.showerror("Missing data", "Fill out databese, tables, columns!")
            return

        join_conditions = []
        for lt, lc, rt, rc in join_entries:
            left_table = lt.get().strip()
            left_col = lc.get().strip()
            right_table = rt.get().strip()
            right_col = rc.get().strip()
            if left_table and left_col and right_table and right_col:
                join_conditions.append({
                    "left_table": left_table,
                    "left_column": left_col,
                    "right_table": right_table,
                    "right_column": right_col
                })

        conditions = {}
        for table, entries in condition_entries.items():
            conditions[table] = []
            for col, op, val in entries:
                c = col.get().strip()
                o = op.get().strip()
                v = val.get().strip()
                if c and o and v:
                    conditions[table].append({
                        "column": c,
                        "operator": o,
                        "value": v
                    })

        command = {
            "action": "JOIN_SELECT",
            "db_name": db,
            "tables": tables,
            "join_conditions": join_conditions,
            "columns": columns,
            "conditions_per_table": conditions
        }

        group_col = group_col_entry.get().strip()
        aggregates = []
        for col_entry, op_var in aggregate_entries:
            col = col_entry.get().strip()
            op = op_var.get().strip().upper()
            if col and op:
                aggregates.append({"agg_column": col, "operation": op})
        if group_col and aggregates:
            command["group_by"] = {
                "group_column": group_col,
                "aggregates": aggregates
            }

        order_col = order_col_entry.get().strip()
        if order_col:
            command["order_by"] = {
                "column": order_col,
                "desc": desc_var.get()
            }

        having_col = having_col_entry.get().strip()
        having_op = having_op_entry.get().strip()
        having_val = having_val_entry.get().strip()
        if having_col and having_op and having_val:
            command["having"] = {
                "column": having_col,
                "operator": having_op,
                "value": having_val
            }

        response = send_command(command)
        lines = response.strip().splitlines()
        if len(lines) > 100:
            print("Too many rows to show in GUI — writing to terminal:")
            with open("query_output.txt", "w", encoding="utf-8") as f:
                f.write(response)
            messagebox.showinfo("Large amount of data", f"{len(lines)} rows returned — saved to 'query_output.txt'.")
        else:
            output_box.delete("1.0", tk.END)
            output_box.insert(tk.END, response)

        window.destroy()

    tk.Button(window, text="JOIN SELECT execution", command=submit,
              bg=highlight, fg="white", activebackground="#005f99", font=default_font).pack(pady=0)

    #submit gomb fuggvenye
def handle_submit_command(command, parent_window, return_response=False):
    response = send_command(command)

    if return_response:
        return response

    try:
        parsed = json.loads(response)
    except Exception as e:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"Error in response or json: {e}\n\n{response}")
        return
    else:
        if parsed.get("status") == "success":
            output_box.delete("1.0", tk.END)
            output_box.insert(tk.END, parsed.get("message")) 
            return
        else:
            print(parsed.get("message", "Unknown error"))

    row_count = len(parsed)
    if row_count > 1000:
        print(f" Response of{row_count} rows –  writing to terminal...")

        for row in parsed:
            print(row)
        
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"{row_count} rows returned. Wrote to terminal.")
    else:
        formatted = json.dumps(parsed, indent=2)
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, formatted)

    if parent_window is not None:
        parent_window.destroy()


output_box = tk.Text(root, height=20, width=120, bg="#95e793", fg="black", font=default_font)
output_box.pack(padx=15, pady=15)


root.mainloop()