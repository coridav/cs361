import json
import os

def clear():
    # 'nt' is Windows, 'posix' is Mac/Linux
    os.system('cls' if os.name == 'nt' else 'clear')

# creates border for project
def border():
    print("-" * 40)

def load_tasks():
    tasks_path = os.path.join(os.path.dirname(__file__), "tasks.json")
    try:    
        with open(tasks_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and "tasks" in data and isinstance(data["tasks"], list):
                return data["tasks"]
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return []


def load_completed_tasks():
    completed_path = os.path.join(os.path.dirname(__file__), "completed.json")
    try:
        with open(completed_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and "completed" in data and isinstance(data["completed"], list):
                return data["completed"]
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return []


def main_menu(stats):
    clear()
    border()
    print("MAIN DASHBOARD")
    print(f"Tallies: {stats.tallies} | Stars: {stats.stars}")
    print("Goal: "+str(stats.goal_tallies)+" more tallies for a star!")
    print("Complete 5 stars for a $3 treat!")
    border()
    print("0. Exit")
    print("1. View Tasks")
    print("2. Add New Task")
    print("3. View History")
    print("")
    print("Enter Selection: ", end="")

def task_mgmt_menu(tasks):
    clear()
    border()
    print("TASK MANAGEMENT")
    print("Top 10 Tasks:")
    border()
    # check if tasks have passed from data_manager
    if not tasks:
        print("No tasks available.")
    else:  # IH#3 information control - only show basics here
        for index, task in enumerate(tasks[:10], start=1):
            task_name = task.get("name") or "Untitled Task"
            due_date = task.get("due_date") or "No due date"
            print(f"{index}. {task_name}: {due_date}")
    # #. [Task Name]: [Due Date]
    # *** add list of options: exit to menu, select task to view/edit/delete, view next 10 tasks, add enw task, view rewards
    print("")
    print("0. Exit to Main Menu")
    print("#. Select task to view/edit/delete")
    print("A. View next 10 tasks")
    print("B. Add new task")
    print("C. View Rewards")
    print("")
    print("Enter Selection: ", end="")

def view_task_menu(task):
    clear()
    border()
    print("TASK EDIT")
    # uses f-strings to fixes the 'None' and concatenation errors
    print(f"Task: {task.get('name','Untitled Task')}")
    print(f"Description: {task.get('description','No description')}")
    print(f"Due Date: {task.get('due_date','No due date')}")
    print(f"Status: {task.get('status','No status')}")
    border()
    print("0. Back to List")#directs to task mgmt menu
    print("1. Edit Task")
    print("2. Edit Description")
    print("3. Edit Due Date ([MM/DD/YYYY] or 'today'/'tmrw')")
    print("4. Quick Edit -> enter on one line: [Task Name], [Description], [Due Date]") # edit everything on one line with format: [Task Name], [Description], [Due Date]
    print("5. Mark as Completed") # directs to task mgmt menu and adds tally to stats
    print("6. Delete Task") # directs to delete task confirmation menu
    print("")
    print("Enter Selection: ", end="")

def delete_task_menu():
    clear()
    border()
    print("DELETE TASK")
    print("Are you sure you want to delete this task? This action cannot be undone!")
    border()
    print("1. Yes, delete task")
    print("2. No, keep task")
    print("")
    print("Enter Selection: ", end="")

def rewards_menu(stats):
    clear()
    border()
    print("REWARDS")
    print(f"Fun money: ${stats.fun_money}")
    border()    
    # check if the file exists first for Reliability
    if os.path.exists("rewards.json"):
        with open("rewards.json") as f:
            rewards = json.load(f)
        for reward in rewards:
            # Change 'name' to 'item' here!
            item_name = reward.get('item', 'Unknown Item')
            cost = reward.get('cost', 0)
            print(f"{item_name}: ${cost}")
            
    print("")
    print("0. Exit to Main Menu")
    print("1. Edit tallies and stars goal")
    print("2. Input Custom cost of reward")

    print("Enter Selection: ", end="")

def edit_treat_goal_menu(stats):
    clear()
    border()
    print("TALLIES AND STARS GOAL")
    print("Are you sure? Changing your goal will reset your current progress toward you next milestone.")
    print(f"# tallies until next star: {stats.goal_tallies}")
    print(f"# stars until next treat: {stats.goal_stars}")
    border()
    print("0. Exit to rewards without saving")
    print("Step 1. Enter # of tallies you'd like until a star is earned")
    print("Step 2. Enter # of stars you'd like until a treat is earned")
    print("Separate your answers with a comma: [# of tallies], [# of stars]")
    print("Enter Selection: ", end="")

def history(completed_tasks):
    clear()
    border()
    print("HISTORY")
    print("Last 10 Completed Tasks:")
    # *** add list of past tasks with completion dates
    if not completed_tasks:
        print("No completed tasks yet.")
    else:
        # Get last 10
        top10 = completed_tasks[-10:]
        for i, item in enumerate(top10, start=1):
            # Use 'name' to match your task structure
            print(f"{i}. {item.get('name', 'Untitled')}")
    border()
    print("0. Exit to Main Menu")
    print("#. Uncomplete task") #removes top task from completed list and adds it back to tasks list
    print("A. View next 10 tasks")
    print("B. Clear history")
    print("")
    print("Enter Selection: ", end="")