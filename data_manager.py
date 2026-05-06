import json
import os
from datetime import datetime


DATA_FILE = "tasks.json"

def load_data():
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        return {"tasks": [], "completed": [], "stats": {"tallies": 0, "stars": 0, "fun_money": 0.0, "goal_tallies": 5, "goal_stars": 5}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    data["tasks"]=get_sorted_tasks(data["tasks"])
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_task(data, name, due, desc):
    data["tasks"].append({"name": name, "due_date": due, "description": desc, "status": "incomplete"})
    save_data(data)

def complete_task(data, index):
    task = data["tasks"].pop(index)
    task["status"] = "complete"
    data["completed"].insert(0, task) # newest at the top!
    
    # add $3.00 for every task completed
    data["stats"]["fun_money"]+=3.0

    data["stats"]["tallies"] += 1
    if data["stats"]["tallies"] >= int(data["stats"]["goal_tallies"]):
        data["stats"]["tallies"] = 0
        data["stats"]["stars"] += 1
        if data["stats"]["stars"] >= int(data["stats"]["goal_stars"]):
            data["stats"]["stars"] = 0
            data["stats"]["fun_money"] += 3.0
    save_data(data)
def uncomplete_task(data,index):
    # remove from compelted and put back into active tasks
    task = data["completed"].pop(index)
    task["status"]="incomplete"
    data["tasks"].append(task)

    # deducts rewards
    data["stats"]["fun_money"] -=3.0
    if data["stats"]["tallies"]>0:
        data["stats"]["tallies"]-=1
    
    save_data(data)

def get_sorted_tasks(tasks):
    # this sorts the list in-place based on the due_date field
    def sort_key(task):
        try:
            # We convert the string to a date object so 01/01 comes before 05/07
            return datetime.strptime(task.get('$due_date$', '12/31/2099'), "%m/%d/%Y")
        except ValueError:
            # If the date is formatted wrong, put it at the end
            return datetime.strptime('12/31/2099', "%m/%d/%Y")

    return sorted(tasks, key=sort_key)

def update_goals(data, t, s):
    data["stats"]["goal_tallies"], data["stats"]["goal_stars"] = t, s
    data["stats"]["tallies"], data["stats"]["stars"] = 0, 0
    save_data(data)

def clear_history(data):
    data["completed"]=[]
    save_data(data)