# import os

from tabulate import tabulate

table = []
table.append({'#': 0, 'Downlink Status': False,
              'Reed Solomon Decode Status': False, 'Unzip + Base64 Decode Status': False})
table.append({'#': 0, 'Downlink Status': False,
              'Reed Solomon Decode Status': False, 'Unzip + Base64 Decode Status': False})
table.append({'#': 0, 'Downlink Status': False,
              'Reed Solomon Decode Status': False, 'Unzip + Base64 Decode Status': False})
table.append({'#': 0, 'Downlink Status': False,
              'Reed Solomon Decode Status': False, 'Unzip + Base64 Decode Status': False})

table_values = [list(x.values()) for x in table]
headers = ['#', 'Downlink Status', 'Reed Solomon Decode Status', 'Unzip + Base64 Decode Status']
print(tabulate(table_values, headers=headers, tablefmt="pretty"))
# print(type(tabulate(table, headers=headers, tablefmt="pretty")))

# If no mission created yet, create file (should not exist yet)
# if not os.path.exists(f"status.txt"):
#     with open(f"status.txt", "w") as status_file:
#         status_file.write(tabulate(table, headers=headers, tablefmt="pretty"))
