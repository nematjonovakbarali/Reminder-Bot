import json
from datetime import datetime

def load_users_data():
    with open("data/users.json", "r") as f:
        data = json.load(f)
    return data

def load_reminds_data():
    with open("data/reminds.json", "r") as f:
        data = json.load(f)
    return data

def save_user(id, name):
    data = load_users_data()
    notes = load_reminds_data()
    if not any(i["user_id"] == id for i in data):
        data.append({
            "user_id": id,
            "name": name,
        })
        with open("data/users.json", "w") as f:
            json.dump(data, f, indent=4)
        notes.append({
            "user_id": id,
            "notes": [],
            "time_notes": []
        })
        with open("data/reminds.json", "w") as f:
            json.dump(notes, f, indent=4)
        return True
    else:
        return False

def save_note(note, id):
    data = load_reminds_data()
    for i in data:
        if i["user_id"] == id:
            i["notes"].append(f"{note}")
    with open("data/reminds.json", "w") as f:
        json.dump(data, f, indent=4)
    return True

def save_note_time(note, time, id):
    data = load_reminds_data()
    for i in data:
        if i["user_id"] == id:
            i["time_notes"].append({f"{time}": f"{note}"})
            with open("data/reminds.json", "w") as f:
                json.dump(data, f, indent=4)
    return True


def check_time_format(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False
    

def remove_note(id, note_id):
    try:
        note_index = int(note_id) - 1
    except (TypeError, ValueError):
        return False

    data = load_reminds_data()
    for i in data:
        if i["user_id"] == id:
            if 0 <= note_index < len(i["notes"]):
                i["notes"].pop(note_index)
                with open("data/reminds.json", "w") as f:
                    json.dump(data, f, indent=4)
                return True
            return False
    return False

def remove_note_time(id, note_id):
    try:
        note_index = int(note_id) - 1
    except (TypeError, ValueError):
        return False

    data = load_reminds_data()
    for i in data:
        if i["user_id"] == id:
            if 0 <= note_index < len(i["time_notes"]):
                i["time_notes"].pop(note_index)
                with open("data/reminds.json", "w") as f:
                    json.dump(data, f, indent=4)
                return True
            return False
    return False
    
def clear_notes(id):
    data = load_reminds_data()
    found = False

    for i in data:
        if i["user_id"] == id:
            i["notes"] = []
            i["time_notes"] = []
            found = True
            break  

    if found:
        with open("data/reminds.json", "w") as f:
            json.dump(data, f, indent=4)


    return found

