import os

from tabulate import tabulate

table = [["spam", 42], ["eggs", 451], ["bacon", 0]]
headers = ["item", "qty"]
print(tabulate(table, headers=headers, tablefmt="pretty"))
print(type(tabulate(table, headers=headers, tablefmt="pretty")))

# If no mission created yet, create file (should not exist yet)
if not os.path.exists(f"status.txt"):
    with open(f"status.txt", "w") as status_file:
        status_file.write(tabulate(table, headers=headers, tablefmt="pretty"))
