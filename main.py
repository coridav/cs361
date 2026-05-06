import data_manager
import menus
from types import SimpleNamespace

# Fix: Date Formatting with zero-padding
def format_date(raw):
    parts = raw.split('/')
    if len(parts) < 2: return "01/01/2026" 
    mm = parts[0].strip().zfill(2)
    dd = parts[1].strip().zfill(2)
    yyyy = parts[2].strip() if len(parts) > 2 else "2026"
    if len(yyyy) == 2: yyyy = "20" + yyyy
    return f"{mm}/{dd}/{yyyy}"

def add_task_wizard_flow(temp_task):
    menus.view_task_menu(temp_task)
    print("\n--- Let's set up your new task! ---")
    temp_task['name'] = input("Step 1 of 3 - Enter Name: ")
    raw_date = input("Step 2 of 3 - Enter Due Date (M/D/YY): ")
    temp_task['due_date'] = format_date(raw_date)
    temp_task['description'] = input("Step 3 of 3 - Enter Description: ")
    
    menus.view_task_menu(temp_task)
    confirm = input("Does this look right? (Y/N): ").lower()
    return temp_task if confirm == 'y' else None

def edit_task_flow(data, index):
    while True:
        task = data["tasks"][index]
        menus.view_task_menu(task)
        choice = input().strip()

        if choice == "0": return
        elif choice == "1": task['name'] = input("Enter name: ")
        elif choice == "2": task['description'] = input("Enter description: ")
        elif choice == "3": 
            raw = input("Enter date (M/D/YY): ")
            task['due_date'] = format_date(raw)
        elif choice == "4": # Quick Edit Logic
            raw = input("Enter [Name], [Desc], [Date]: ")
            if "," in raw:
                parts = raw.split(",")
                task['name'] = parts[0].strip()
                task['description'] = parts[1].strip()
                task['due_date'] = format_date(parts[2].strip())
        elif choice == "5":
            data_manager.complete_task(data, index)
            return
        elif choice == "6": # Delete Logic
            menus.delete_task_menu()
            if input().strip() == "1":
                data["tasks"].pop(index)
                data_manager.save_data(data)
                return
        data_manager.save_data(data)

def rewards_flow(data, stats):
    while True:
        menus.rewards_menu(stats)
        choice = input().strip().lower()
        if choice == "0": return "HOME" 
        elif choice == "1":
            raw = input("Enter [Tally Goal], [Star Goal]: ")
            if "," in raw:
                t, s = raw.split(",")
                data_manager.update_goals(data, t.strip(), s.strip())
                stats.goal_tallies, stats.goal_stars = t.strip(), s.strip()
        elif choice == "2":
            item = input("Reward Item: ")
            cost = input("Cost: ")
            print(f"Added {item} for ${cost}!")
            input("Press Enter...")

def history_flow(data):
    start_index = 0
    while True:
        # Pass only the slice of 10 tasks to the menu
        current_view = data["completed"][start_index : start_index + 10]
        menus.history(current_view)
        choice = input().strip().lower()

        if choice == "0":
            return # Back to Main Menu
        
        elif choice == "a": # View Next 10
            if start_index + 10 < len(data["completed"]):
                start_index += 10
            else:
                print("No more history to show!")
                input("Press Enter...")
                
        elif choice == "b": # Clear History
            confirm = input("Are you sure? (Y/N): ").lower()
            if confirm == 'y':
                data_manager.clear_history(data)
                return # Return to menu since history is gone
                
        elif choice.isdigit() and 0 < int(choice) <= len(current_view):
            # Uncomplete Logic
            actual_index = start_index + (int(choice) - 1)
            data_manager.uncomplete_task(data, actual_index)
            print("Task moved back to To-Do list!")
            return # Refresh to show changes

def task_management_flow(data, stats):
    while True:
        sorted_tasks = data_manager.get_sorted_tasks(data["tasks"])
        
        menus.task_mgmt_menu(data["tasks"])
        choice = input().strip().lower()
        
        if choice == "0": return
        elif choice == "b": # Add from list
            new_task = {"name": "New", "description": "None", "due_date": "01/01/2026", "status": "incomplete"}
            final = add_task_wizard_flow(new_task)
            if final: data_manager.add_task(data, final['name'], final['due_date'], final['description'])
        elif choice == "c":
            if rewards_flow(data, stats) == "HOME": return
        elif choice.isdigit() and 0 < int(choice) <= len(data["tasks"]):
            edit_task_flow(data, int(choice) - 1)

def main_loop():
    while True:
        data = data_manager.load_data()
        stats = SimpleNamespace(**data["stats"])
        menus.main_menu(stats)
        choice = input().strip()

        if choice == "1": task_management_flow(data, stats)
        elif choice == "2": # add from dashboard
            new_task = {"name": "New", "description": "None", "due_date": "01/01/2026", "status": "incomplete"}
            final = add_task_wizard_flow(new_task)
            if final: data_manager.add_task(data, final['name'], final['due_date'], final['description'])
        elif choice == "3":
            history_flow(data)
        elif choice == "0":
            print("Saving and exiting... Goodbye!"); break

if __name__ == "__main__":
    main_loop()
    