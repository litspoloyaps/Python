from collections import deque
from colorama import init, Fore, Back, Style
import os
import time

init(autoreset=True)

GREEN = Fore.GREEN + Style.BRIGHT
GOLD = Fore.YELLOW + Style.BRIGHT
WHITE = Fore.WHITE + Style.BRIGHT
ERROR = Fore.RED + Style.BRIGHT
INFO = Fore.CYAN
RESET = Style.RESET_ALL

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input(f"{INFO}Press Enter to continue...{RESET}")

def header():
    print(GREEN + Style.BRIGHT)
    print("  ██████╗      ██████╗      ███╗   ███╗ ")
    print(" ██╔════╝      ██╔══██╗     ████╗ ████║ ")
    print(" ██║           ██║  ██║     ██╔████╔██║   " + GREEN + "Colegio   De  Montalban" + RESET)
    print(" ██║           ██║  ██║     ██║╚██╔╝██║   " + GOLD + "Registrar Queue System" + RESET)
    print(" ╚██████╗      ██████╔╝     ██║ ╚═╝ ██║   " + GOLD + "2025" + RESET)
    print("  ╚═════╝      ╚═════╝      ╚═╝     ╚═╝ ")
    print(GREEN + "──────────────────────────────────────────────" + RESET)
    print()

class RegistrarQueue:
    def __init__(self):
        self.queue = deque()

    def add_student(self, student_id, name):
        self.queue.append({"id": student_id, "name": name})
        print(f"{GREEN}[✔] Student {student_id} - {name} added to queue.{RESET}\n")

    def serve_student(self):
        if not self.queue:
            print(f"{ERROR}[!] No students in queue.{RESET}\n")
            return

        student = self.queue.popleft()
        print(f"{GOLD}[⟲] Now serving: {student['id']} - {student['name']}{RESET}\n")
        pause()

    def view_queue(self):
        if not self.queue:
            print(f"{ERROR}[!] Queue is empty.{RESET}\n")
            return

        print(f"\n{Back.GREEN}{Fore.BLACK}=== CURRENT QUEUE ==={RESET}")
        for i, student in enumerate(self.queue, start=1):
            print(f"{GOLD}{i}. {student['id']} - {student['name']}{RESET}")
        print()

def menu():
    print(f"{WHITE}{Back.GREEN}        MAIN MENU        {RESET}")
    print(f"{GOLD}1.{RESET} Add Student to Queue")
    print(f"{GOLD}2.{RESET} Serve Next Student")
    print(f"{GOLD}3.{RESET} View Queue")
    print(f"{GOLD}4.{RESET} Exit Program\n")

    return input(f"{GREEN}Enter choice → {RESET}")

def main():
    system = RegistrarQueue()

    while True:
        clear_screen()
        header()
        choice = menu()

        if choice == "1":
            student_id = input(f"{INFO}Enter Student ID: {RESET}").strip()
            name = input(f"{INFO}Enter Student Name: {RESET}").strip()
            system.add_student(student_id, name)
            pause()

        elif choice == "2":
            system.serve_student()
            pause()

        elif choice == "3":
            clear_screen()
            header()
            system.view_queue()
            pause()

        elif choice == "4":
            print(f"{ERROR}Goodbye! Thank you for using the Registrar System.{RESET}")
            pause()
            break

        else:
            print(f"{ERROR}[!] Invalid option. Try again.{RESET}\n")
            pause()

if __name__ == "__main__":
    main()
