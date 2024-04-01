array = [
    {
    "username":"target",
    "access_level": 1,
    },
    {
    "username":"name",
    "access_level": 2,
    },
    {
    "username":"me",
    "access_level": 1,
    }
    ]
target = "target"
print(array)
for entry in array:
    if entry["username"].lower() == target:
        array.remove(entry)
print(array)