import json

FILE = "data.json"

def load_data():
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_user(username):
    data = load_data()
    if username not in data["users"]:
        data["users"].append(username)
        save_data(data)

def get_users():
    return load_data()["users"]

def add_message(sender, receiver, text):
    data = load_data()
    data["messages"].append({
        "sender": sender,
        "receiver": receiver,
        "text": text
    })
    save_data(data)

def get_messages():
    return load_data()["messages"]
