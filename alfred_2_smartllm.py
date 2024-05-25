import json

# Function to transform the input JSON to the desired output format
def transform_json(input_data, pattern):
    output_data = []

    for key, task in input_data.items():
        if key.startswith(pattern):
            task_data = {"task": task,"robot list": [1, 2, 3], "object_states": [],"trans": 0,"max_trans": 1}
            
            # Append the transformed task data to the output list
            output_data.append(task_data)
    
    return output_data

# Load the JSON data from a file
input_file = '/home/tim/alfred_multiagent/multiagent_longtasks_summary.json'

pattern = 'FloorPlan1|tasks_1|'

with open(input_file, 'r') as f:
    input_json = json.load(f)

# Extract the output file name from the first key in the input JSON
first_key = list(input_json.keys())[0]
output_file_name = first_key.split('|')[0] + '.json'

# Transform the input JSON
transformed_data = transform_json(input_json, pattern)

# Output the transformed data to a file
with open(output_file_name, 'w') as f:
    for item in transformed_data:
        f.write(json.dumps(item) + '\n')

print(f"Transformed data has been written to {output_file_name}")