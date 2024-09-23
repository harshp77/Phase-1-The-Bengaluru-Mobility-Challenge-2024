from Asset.run_tracker import trak           # Import the function responsible for tracking 
from Asset.get_segment import run_get_segment_json, unnormalize_segment_data   # Import Segment Data (Regions) for the Specified CamID 
from Asset.pattern import update_json_structure   # Import the function responisble for Fixing and saving the tracking in a Output.json
from Asset.future_OTG import forecast
import sys
import json
import pathlib   
import pandas as pd

input_file = sys.argv[1]
output_file = sys.argv[2]

# Load JSON data from the input file
BASE_DIR = str(pathlib.Path().resolve())
with open(input_file) as f:
    data = json.load(f)
    
    
cam_ID = list(data.keys())[0]
model_path = f'{BASE_DIR}/Asset/640.pt'

i=0
c=0
final_tracking = []
# Process each entry in the data for the specified camera ID
for ele in data[cam_ID]:
    print(cam_ID, data[cam_ID][ele], "HELLO")    
    # Load segment data (regions) for the camera ID
    segment_data = run_get_segment_json(cam_ID, BASE_DIR)
    # Perform tracking using the model and update the index counter
    tracking, width, height, i = trak(model_path, data[cam_ID][ele],i)
    # Unnormalize segment data to match video dimensions
    segment_data = unnormalize_segment_data(segment_data, width, height)
    # Update the JSON structure with the current tracking data
    current_tracking_list=update_json_structure(segment_data, tracking, BASE_DIR, output_file, cam_ID,c)
    # Append the current tracking results to the final tracking list
    final_tracking.append(current_tracking_list)
    c+=1
    
    
# Load the updated structure from the output file    
with open(output_file, 'r') as file:
    structure = json.load(file)

# Forecast future patterns based on the final tracking data
structure = forecast(final_tracking,cam_ID, structure, BASE_DIR)

# Save the updated structure back to the output file
with open(output_file, 'w') as file:
    json.dump(structure, file, indent=4)