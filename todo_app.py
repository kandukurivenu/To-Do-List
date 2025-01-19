import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('todo.db')
c = conn.cursor()

# Create tasks table with additional columns
c.execute('''CREATE TABLE IF NOT EXISTS tasks (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             task TEXT NOT NULL,
             due_date TEXT,
             priority TEXT CHECK(priority IN ('Low', 'Medium', 'High')),
             status TEXT NOT NULL DEFAULT "Pending"
             )''')
conn.commit()

def add_task(task, due_date=None, priority='Medium'):
    c.execute('INSERT INTO tasks (task, due_date, priority) VALUES (?, ?, ?)', (task, due_date, priority))
    conn.commit()
    print(f"Task added: {task}")

def view_tasks():
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    if not tasks:
        print("No tasks found.")
    else:
        print("\nYour To-Do List:")
        for task in tasks:
            print(f"{task[0]}. {task[1]} - Due: {task[2]} - Priority: {task[3]} - Status: {task[4]}")

def mark_completed(task_id):
    if task_exists(task_id):
        c.execute('UPDATE tasks SET status = "Completed" WHERE id = ?', (task_id,))
        conn.commit()
        print(f"Task {task_id} marked as completed.")
    else:
        print(f"Task {task_id} does not exist.")

def delete_task(task_id):
    if task_exists(task_id):
        c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        print(f"Task {task_id} deleted.")
    else:
        print(f"Task {task_id} does not exist.")

def search_tasks(keyword):
    c.execute('SELECT * FROM tasks WHERE task LIKE ?', (f'%{keyword}%',))
    tasks = c.fetchall()
    if not tasks:
        print(f"No tasks found containing '{keyword}'.")
    else:
        print(f"\nTasks containing '{keyword}':")
        for task in tasks:
            print(f"{task[0]}. {task[1]} - Due: {task[2]} - Priority: {task[3]} - Status: {task[4]}")

def export_tasks(filename='tasks_export.txt'):
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    if not tasks:
        print("No tasks to export.")
    else:
        with open(filename, 'w') as file:
            file.write("ID | Task | Due Date | Priority | Status\n")
            file.write("-" * 40 + "\n")
            for task in tasks:
                file.write(f"{task[0]} | {task[1]} | {task[2]} | {task[3]} | {task[4]}\n")
        print(f"Tasks exported to {filename}.")

def task_exists(task_id):
    c.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    return c.fetchone() is not None

def main():
    while True:
        print("\n--- To-Do List App ---")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Search Tasks")
        print("6. Export Tasks")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_tasks()
        elif choice == '2':
            task = input("Enter the task: ")
            due_date = input("Enter the due date (YYYY-MM-DD, optional): ")
            priority = input("Enter the priority (Low/Medium/High, default: Medium): ") or 'Medium'
            add_task(task, due_date, priority)
        elif choice == '3':
            task_id = input("Enter the task ID to mark as completed: ")
            mark_completed(task_id)
        elif choice == '4':
            task_id = input("Enter the task ID to delete: ")
            delete_task(task_id)
        elif choice == '5':
            keyword = input("Enter a keyword to search for: ")
            search_tasks(keyword)
        elif choice == '6':
            filename = input("Enter the filename to export tasks (default: tasks_export.txt): ") or 'tasks_export.txt'
            export_tasks(filename)
        elif choice == '7':
            print("Exiting the app. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the app
if __name__ == "__main__":
    main()
    conn.close()
