import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class EventManagementSystem:
    def __init__(self):
        self.conn = sqlite3.connect('event_management.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                role TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_name TEXT,
                description TEXT,
                date TEXT,
                organizer TEXT,
                created_by TEXT
            )
        ''')
        self.conn.commit()

    def register_user(self, username, password, role):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO users VALUES (?, ?, ?)", 
                           (username, password, role))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", 
                       (username, password))
        return cursor.fetchone()

    def create_event(self, event_name, description, date, organizer, created_by):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO events (event_name, description, date, organizer, created_by) VALUES (?, ?, ?, ?, ?)", 
                       (event_name, description, date, organizer, created_by))
        self.conn.commit()

    def get_events(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM events")
        return cursor.fetchall()

    def get_user_role(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        return result[0] if result else None

    def delete_event(self, event_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM events WHERE event_id=?", (event_id,))
        self.conn.commit()

    def update_event(self, event_id, event_name, description, date, organizer):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE events 
            SET event_name=?, description=?, date=?, organizer=? 
            WHERE event_id=?
        """, (event_name, description, date, organizer, event_id))
        self.conn.commit()

class EventDashboard:
    def __init__(self, master, username, ems):
        self.master = master
        self.ems = ems
        self.username = username
        self.user_role = ems.get_user_role(username)
        master.title(f"Event Management Dashboard - Welcome {username}")
        master.geometry("700x500")
        self.create_event_btn = tk.Button(master, text="Create New Event", command=self.open_create_event_window)
        self.create_event_btn.pack(pady=10)
        self.events_frame = tk.Frame(master)
        self.events_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        self.events_label = tk.Label(self.events_frame, text="Current Events:", font=("Arial", 12, "bold"))
        self.events_label.pack()
        self.events_tree = ttk.Treeview(self.events_frame, 
            columns=("ID", "Name", "Description", "Date", "Organizer", "Created By"), 
            show="headings"
        )
        self.events_tree.heading("ID", text="Event ID")
        self.events_tree.heading("Name", text="Event Name")
        self.events_tree.heading("Description", text="Description")
        self.events_tree.heading("Date", text="Date")
        self.events_tree.heading("Organizer", text="Organizer")
        self.events_tree.heading("Created By", text="Created By")
        self.events_tree.pack(fill=tk.BOTH, expand=True)
        if self.user_role == 'admin':
            self.admin_frame = tk.Frame(master)
            self.admin_frame.pack(pady=10)
            self.delete_event_btn = tk.Button(self.admin_frame, text="Delete Event", command=self.delete_event)
            self.delete_event_btn.pack(side=tk.LEFT, padx=5)
            self.edit_event_btn = tk.Button(self.admin_frame, text="Edit Event", command=self.edit_event)
            self.edit_event_btn.pack(side=tk.LEFT, padx=5)
        self.load_events()

    def open_create_event_window(self):
        create_window = tk.Toplevel(self.master)
        create_window.title("Create New Event")
        create_window.geometry("400x300")
        tk.Label(create_window, text="Event Name:").pack()
        event_name_entry = tk.Entry(create_window, width=40)
        event_name_entry.pack()
        tk.Label(create_window, text="Description:").pack()
        description_entry = tk.Text(create_window, height=4, width=40)
        description_entry.pack()
        tk.Label(create_window, text="Organizer:").pack()
        organizer_entry = tk.Entry(create_window, width=40)
        organizer_entry.pack()
        tk.Label(create_window, text="Date:").pack()
        date_entry = tk.Entry(create_window, width=40)
        date_entry.pack()
        def save_event():
            name = event_name_entry.get()
            description = description_entry.get("1.0", tk.END).strip()
            organizer = organizer_entry.get()
            date = date_entry.get()
            if name and description and date and organizer:
                self.ems.create_event(name, description, date, organizer, self.username)
                messagebox.showinfo("Success", "Event Created Successfully!")
                create_window.destroy()
                self.load_events()
            else:
                messagebox.showerror("Error", "Please fill all fields")
        save_btn = tk.Button(create_window, text="Save Event", command=save_event)
        save_btn.pack(pady=10)

    def load_events(self):
        for i in self.events_tree.get_children():
            self.events_tree.delete(i)
        events = self.ems.get_events()
        for event in events:
            self.events_tree.insert("", "end", values=event)

    def delete_event(self):
        if self.user_role != 'admin':
            messagebox.showerror("Access Denied", "Only admins can delete events")
            return
        selected_item = self.events_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an event to delete")
            return
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this event?")
        if confirm:
            event_id = self.events_tree.item(selected_item[0])['values'][0]
            self.ems.delete_event(event_id)
            messagebox.showinfo("Success", "Event deleted successfully")
            self.load_events()

    def edit_event(self):
        if self.user_role != 'admin':
            messagebox.showerror("Access Denied", "Only admins can edit events")
            return
        selected_item = self.events_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an event to edit")
            return
        event_details = self.events_tree.item(selected_item[0])['values']
        event_id, event_name, description, date, organizer, _ = event_details
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Event")
        edit_window.geometry("400x300")
        tk.Label(edit_window, text="Event Name:").pack()
        event_name_entry = tk.Entry(edit_window, width=40)
        event_name_entry.insert(0, event_name)
        event_name_entry.pack()
        tk.Label(edit_window, text="Description:").pack()
        description_entry = tk.Text(edit_window, height=4, width=40)
        description_entry.insert("1.0", description)
        description_entry.pack()
        tk.Label(edit_window, text="Organizer:").pack()
        organizer_entry = tk.Entry(edit_window, width=40)
        organizer_entry.insert(0, organizer)
        organizer_entry.pack()
        tk.Label(edit_window, text="Date:").pack()
        date_entry = tk.Entry(edit_window, width=40)
        date_entry.insert(0, date)
        date_entry.pack()
        def save_edited_event():
            new_name = event_name_entry.get()
            new_description = description_entry.get("1.0", tk.END).strip()
            new_organizer = organizer_entry.get()
            new_date = date_entry.get()
            if new_name and new_description and new_date and new_organizer:
                self.ems.update_event(event_id, new_name, new_description, new_date, new_organizer)
                messagebox.showinfo("Success", "Event Updated Successfully!")
                edit_window.destroy()
                self.load_events()
            else:
                messagebox.showerror("Error", "Please fill all fields")
        save_btn = tk.Button(edit_window, text="Save Changes", command=save_edited_event)
        save_btn.pack(pady=10)

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.ems = EventManagementSystem()
        master.title("College Event Management")
        master.geometry("300x200")
        self.username_label = tk.Label(master, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(master)
        self.username_entry.pack(pady=5)
        self.password_label = tk.Label(master, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack(pady=5)
        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.pack(pady=10)
        self.register_button = tk.Button(master, text="Register", command=self.register)
        self.register_button.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.ems.login(username, password)
        if user:
            self.master.withdraw()
            dashboard_root = tk.Toplevel(self.master)
            EventDashboard(dashboard_root, username, self.ems)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register(self):
        username = simpledialog.askstring("Register", "Enter Username:")
        password = simpledialog.askstring("Register", "Enter Password:", show='*')
        role = simpledialog.askstring("Register", "Enter Role (admin/student):")
        if username and password and role:
            if self.ems.register_user(username, password, role):
                messagebox.showinfo("Success", "Registration Successful!")
            else:
                messagebox.showerror("Error", "Username already exists")

root = tk.Tk()
login_window = LoginWindow(root)
root.mainloop()
