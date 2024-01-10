import json

info = """[
    {
        "id" : "001",
        "x" : "2",
        "name" : "Chuck"
    },
    {
        "id" : "009",
        "x" : "7",
        "name" : "Severance"
    }
]"""

users = json.loads(info)
print(f"There are {len(users)} users...\n")

for user in users:
    print("Name:", user["name"])
    print("Id:", user["id"])
    print("Attr:", user["x"], "\n")
