import json
import os
from datetime import datetime


DATA_FILE = "tasks.json"
def get_sorted_tasks(tasks):
    # this sorts the list in-place based on the due_date field
    def get_date(task):
        try:
            # we convert the string to a date object so 01/01 comes before 05/07
            return datetime.strptime(task.get('due_date', '12/31/2099'), "%m/%d/%Y")
        except ValueError:
            # if the date is formatted wrong, put it at the end
            return datetime.strptime('12/31/2099', "%m/%d/%Y")
    #sorts the list in place
    tasks.sort(key=get_date)

def load_data():
    # check if file exists or is empty
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        return {"tasks": [], "completed": [], "stats": {"tallies": 0, "stars": 0, "fun_money": 0.0, "goal_tallies": 5, "goal_stars": 5}}
    #open and load data
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    # sort the tasks so most recent is at top, calls sort_tasks_by_date
    get_sorted_tasks(data["tasks"])
    return data

def save_data(data):
    get_sorted_tasks(data["tasks"]) #sort before writing to file
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_task(data, name, due, desc):
    data["tasks"].append({"name": name, "due_date": due, "description": desc, "status": "incomplete"})
    save_data(data)

def complete_task(data, index):
    task = data["tasks"].pop(index)
    task["status"] = "complete"
    data["completed"].insert(0, task) # newest at the top
    
    # update tallies
    data["stats"]["tallies"] += 1
    # check if tally goal is reached to earn a star
    if data["stats"]["tallies"] >= int(data["stats"]["goal_tallies"]):
        data["stats"]["tallies"] = 0
        data["stats"]["stars"] += 1
        print("\nYou earned a star!")
        # check if star goal is reached to earn fun money
        if data["stats"]["stars"] >= int(data["stats"]["goal_stars"]):
            data["stats"]["stars"] = 0
            data["stats"]["fun_money"] += 3.0 #reward earned
            print("\nMilestone reache! $3.00 added to Fun Money!")
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


def update_goals(data, t, s):
    data["stats"]["goal_tallies"], data["stats"]["goal_stars"] = t, s
    data["stats"]["tallies"], data["stats"]["stars"] = 0, 0
    save_data(data)

def clear_history(data):
    data["completed"]=[]
    save_data(data)