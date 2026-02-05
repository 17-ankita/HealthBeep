import sqlite3
import threading
import time
from datetime import datetime

# --- Step 1: Database Setup ---
conn = sqlite3.connect('medicines.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS Medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    dosage TEXT NOT NULL,
    time TEXT NOT NULL
)
''')

conn.commit()
conn.close()
print("Database and table are ready!")

# --- Step 2: Function to add medicine ---
def add_medicine():
    conn = sqlite3.connect('medicines.db')
    c = conn.cursor()
    
    name = input("Enter medicine name: ")
    dosage = input("Enter dosage (e.g., 1 pill): ")
    time_input = input("Enter time (HH:MM, 24-hour format): ")
    
    c.execute("INSERT INTO Medicines (name, dosage, time) VALUES (?, ?, ?)",
              (name, dosage, time_input))
    conn.commit()
    conn.close()
    
    print(f"Medicine '{name}' added for {time_input}!")

# --- Step 3: Function to show medicines ---
def show_medicines():
    conn = sqlite3.connect('medicines.db')
    c = conn.cursor()
    
    c.execute("SELECT id, name, dosage, time FROM Medicines ORDER BY time")
    rows = c.fetchall()
    
    if not rows:
        print("No medicines found.")
    else:
        print("\nYour Medicine Schedule:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Dosage: {row[2]}, Time: {row[3]}")
    
    conn.close()

# --- Step 4: Reminder function ---
def reminder_loop():
    while True:
        now = datetime.now().strftime("%H:%M")
        conn = sqlite3.connect('medicines.db')
        c = conn.cursor()
        
        # Get medicines scheduled for current time
        c.execute("SELECT name, dosage FROM Medicines WHERE time = ?", (now,))
        rows = c.fetchall()
        
        for row in rows:
         print(f"\nReminder: Take {row[0]} ({row[1]}) NOW!") 
        conn.close()
        time.sleep(60)  # check every minute

# --- Step 5: Start reminder in background ---
threading.Thread(target=reminder_loop, daemon=True).start()

# --- Step 6: Console menu ---
while True:
    command = input("\nEnter command (add/show/exit): ").lower()
    if command == "add":
        add_medicine()
    elif command == "show":
        show_medicines()
    elif command == "exit":
        print("Exiting program...")
        break
    else:
        print("Invalid command. Use 'add', 'show', or 'exit'.")
