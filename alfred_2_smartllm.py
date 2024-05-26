import json

# Function to transform the input JSON to the desired output format
def transform_json(input_data, pattern):
  # List to hold the transformed data
    data_after = []

    # Iterate over each entry in the input JSON
    for entry in input_data:
        # Extract the task key and value
        task_key = list(entry.keys())[0]
        task_value = entry[task_key]

        # Extract the floor plan from the task key
        floor_plan = task_key.split('.')[0]

        
        # Extract the first initial position
        init_pos = entry["init_pos"][0][0]
        
        # Construct the new dictionary
        new_entry = {
            "FloorPlan": floor_plan,
            "task": task_value,
            "robot list": [1, 2, 3],
            "object_states": [],
            "trans": 0,
            "max_trans": 1,
            "init_pos": init_pos
        }
        
        # Append the new entry to the transformed data list
        data_after.append(new_entry)

        
        return data_after

# Load the JSON data from a file
input_file = '/home/tim/alfred_multiagent/multiagent_tasks_1_summary_with_robot_init_pos.json'

pattern = 'FloorPlan1|tasks_1|'

with open(input_file, 'r') as f:
    input_json = json.load(f)

# Extract the output file name from the first key in the input JSON
first_50_dict = input_json[:50]

# output_file_name = first_key.split('|')[0] + '.json'

# Transform the input JSON
transformed_data = transform_json(first_50_dict, pattern)

# Output the transformed data to a file
with open('11.json', 'w') as f:
    for item in transformed_data:
        f.write(json.dumps(item) + '\n')

print(f"Transformed data has been written to {'giao'}")