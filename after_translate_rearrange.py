import json
from collections import defaultdict
import os

# Read the data from the file
with open("11_new.json", "r") as file:
    lines = file.readlines()

# Parse a line as a JSON object and group by FloorPlan
floor_plan_data = defaultdict(list)

for line in lines:
    entry = json.loads(line)
    floor_plan = entry.pop("FloorPlan") 
    floor_plan_data[floor_plan].append(entry)


# Define the target folder
output_folder = "rearranged_taks_for_SmartLLM_1Task"

# Create the target folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)


# Write a group to a separate JSON file
for floor_plan, entries in floor_plan_data.items():
    filename = os.path.join(output_folder, f"{floor_plan}.json")
    with open(filename, "w") as file:
        for entry in entries:

            file.write(json.dumps(entry) +'\n')



print("Data has been split into separate files based on FloorPlan.")
