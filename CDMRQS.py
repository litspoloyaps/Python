import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
from PIL import Image, ImageTk
import datetime
import winsound

regular_queue = deque()
priority_queue = deque()
irregular_queue = deque()

def update_clock():
    now = datetime.datetime.now().strftime("%A | %B %d, %Y | %I:%M:%S %p")
    clock_label.config(text=now)
    root.after(1000, update_clock)

def add_to_queue():
    student_id = id_entry.get().strip()
    name = name_entry.get().strip()
    queue_type = type_var.get()

    if student_id == "" or name == "":
        messagebox.showerror("Error", "Please enter both Student ID and Name")
        return

    data = f"{student_id} - {name}"

    if queue_type == "Priority":
        priority_queue.append(data)
    elif queue_type == "Irregular":
        irregular_queue.append(data)
    else:
        regular_queue.append(data)

    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    update_queue_display()
    winsound.Beep(1200, 150)
    messagebox.showinfo("Added", f"Student ID: {student_id}\n{name} added to {queue_type} Queue")

def serve_next():
    if priority_queue:
        next_student = priority_queue.popleft()
    elif irregular_queue:
        next_student = irregular_queue.popleft()
    elif regular_queue:
        next_student = regular_queue.popleft()
    else:
        messagebox.showwarning("Queue Offline", "No students in queue.")
        return

    student_id, name = next_student.split(" - ", 1)
    now_serving_label.config(text=f"{student_id} - {name}")
    update_queue_display()
    winsound.Beep(600, 500)

def update_queue_display():
    queue_list.delete(*queue_list.get_children())
    for student in priority_queue:
        student_id, name = student.split(" - ", 1)
        queue_list.insert("", tk.END, values=(student_id, name, "PRIORITY"))
    for student in irregular_queue:
        student_id, name = student.split(" - ", 1)
        queue_list.insert("", tk.END, values=(student_id, name, "IRREGULAR"))
    for student in regular_queue:
        student_id, name = student.split(" - ", 1)
        queue_list.insert("", tk.END, values=(student_id, name, "REGULAR"))

root = tk.Tk()
root.title("Colegio de Montalban - Registrar Queuing System")
root.geometry("900x620")
root.configure(bg="#0c3b2e")

header = tk.Frame(root, bg="#0c3b2e", height=110)
header.pack(fill="x")

cdm_image = Image.open("cdm.jpg")
cdm_image = cdm_image.resize((90, 90))
cdm_logo = ImageTk.PhotoImage(cdm_image)

logo_label = tk.Label(header, image=cdm_logo, bg="#0c3b2e")
logo_label.pack(side="left", padx=20)

title_label = tk.Label(header, text="COLEGIO DE MONTALBAN\nREGISTRAR QUEUING SYSTEM",
                       font=("Arial Black", 18), bg="#0c3b2e", fg="#f1c40f", justify="left")
title_label.pack(side="left", padx=10)

clock_label = tk.Label(header, font=("Arial", 12, "bold"), bg="#0c3b2e", fg="white")
clock_label.pack(side="right", padx=20)

update_clock()

input_frame = tk.Frame(root, bg="#0c3b2e")
input_frame.pack(pady=20)

tk.Label(input_frame, text="Student ID:", font=("Arial", 12), bg="#0c3b2e", fg="white").grid(row=0, column=0, padx=5)
id_entry = tk.Entry(input_frame, font=("Arial", 12), width=15)
id_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Student Name:", font=("Arial", 12), bg="#0c3b2e", fg="white").grid(row=0, column=2, padx=5)
name_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
name_entry.grid(row=0, column=3, padx=5)

type_var = tk.StringVar(value="Regular")
tk.Radiobutton(input_frame, text="Regular", variable=type_var, value="Regular", bg="#0c3b2e",
               fg="white", selectcolor="#0c3b2e").grid(row=0, column=4, padx=10)
tk.Radiobutton(input_frame, text="Irregular", variable=type_var, value="Irregular", bg="#0c3b2e",
               fg="white", selectcolor="#0c3b2e").grid(row=0, column=5, padx=10)
tk.Radiobutton(input_frame, text="Priority (PWD/Senior/Faculty)", variable=type_var, value="Priority",
               bg="#0c3b2e", fg="white", selectcolor="#0c3b2e").grid(row=0, column=6, padx=10)

add_btn = tk.Button(input_frame, text="Add to Queue", font=("Arial", 12, "bold"),
                    bg="#f1c40f", fg="#0c3b2e", command=add_to_queue)
add_btn.grid(row=0, column=7, padx=10)

now_frame = tk.Frame(root, bg="#0c3b2e")
now_frame.pack(pady=10)

tk.Label(now_frame, text="NOW SERVING:", font=("Arial Black", 16), bg="#0c3b2e", fg="gold").pack()
now_serving_label = tk.Label(now_frame, text="---", font=("Arial Black", 32), bg="#0c3b2e", fg="white")
now_serving_label.pack(pady=5)

serve_btn = tk.Button(root, text="SERVE NEXT", font=("Arial Black", 14), bg="green", fg="white", width=20, command=serve_next)
serve_btn.pack(pady=10)

table_frame = tk.Frame(root)
table_frame.pack(pady=20)

columns = ("StudentID", "Name", "Type")
queue_list = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
queue_list.heading("StudentID", text="Student ID")
queue_list.heading("Name", text="Student Name")
queue_list.heading("Type", text="Queue Type")
queue_list.column("StudentID", width=120)
queue_list.column("Name", width=280)
queue_list.column("Type", width=180)
queue_list.pack()

root.mainloop()
