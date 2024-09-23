import os
import pandas as pd
import json
import warnings
warnings.filterwarnings("ignore")

# Define all possible segments and labels
ALL_SEGMENTS = list("ABCDEFGH")

ALL_LABELS = ["Bus", "Cars", "LCV", "Three-Wheeler", "Two-Wheeler", "Bicycle", 'Truck']
ALL_LABELS_FIXED = ["Bus", "Car", "LCV", "Three Wheeler", "Two Wheeler", "Bicycle", "Truck"]


# Create a mapping dictionary
LABEL_MAPPING = dict(zip(ALL_LABELS, ALL_LABELS_FIXED))

import math

def zone(x, y, segment_data):
    
    """
    Determines the zone or region of a point (x, y) based on predefined segment data.
    If the point is not within any defined region, finds the nearest region based on distance.

    Args:
        x (float): X-coordinate of the point.
        y (float): Y-coordinate of the point.
        segment_data (dict): Dictionary with segment names as keys and coordinates as values.

    Returns:
        str: The name of the segment or region where the point is located or nearest to.
    """
    
    for segment, coords in segment_data.items():
        if coords['x1'] <= x <= coords['x2'] and coords['y1'] <= y <= coords['y2']:
            return segment
    
    # If not in any region, find the nearest region center
    min_distance = float('inf')
    nearest_segment = None
    
    for segment, coords in segment_data.items():
        center_x = (coords['x1'] + coords['x2']) / 2
        center_y = (coords['y1'] + coords['y2']) / 2
        distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        
        if distance < min_distance:
            min_distance = distance
            nearest_segment = segment
            
    return nearest_segment

def core(segment_data, tracking):
    """
    Processes tracking data to identify transitions between segments based on tracking IDs.

    Args:
        segment_data (dict): Dictionary with segment names as keys and coordinates as values.
        tracking (pd.DataFrame): DataFrame containing tracking data with columns ['ID', 'X', 'Y', 'Label', 'Min'].

    Returns:
        list: A list of tracking results where each result is a list containing minute, label, and transition.
    """
    df = tracking
    ids = df['ID'].unique()
    
    track = []

    for id in ids:

        fd = df[df['ID'] == id]
        if len(fd)<40:
            continue
        first_segment = zone( fd.iloc[0]['X'], fd.iloc[0]['Y'], segment_data)
        
        last_segment = zone( fd.iloc[-1]['X'], fd.iloc[-1]['Y'], segment_data)
        
        if first_segment is None or last_segment is None or first_segment == last_segment:
            continue
        
        label = fd.iloc[0]['Label']
        minute = fd.iloc[-1]['Min']
        fixed_label = LABEL_MAPPING.get(label, label)  
        track.append([minute, fixed_label, f'{first_segment}{last_segment}'])
    return track

def initialize_json_structure(cam_ID):
    """
    Initializes the JSON structure for storing cumulative and predicted counts for each transition.

    Args:
        cam_ID (str): The camera ID used to initialize the structure.

    Returns:
        dict: Initialized structure with cumulative and predicted counts set to 0.
    """
    
    structure = {
        cam_ID: {
            'Cumulative Counts': {},
            'Predicted Counts': {}
        }
    }
    for seg1 in ALL_SEGMENTS:
        for seg2 in ALL_SEGMENTS:
            if seg1 != seg2:
                transition = f"{seg1}{seg2}"
                structure[cam_ID]['Cumulative Counts'][transition] = {label: 0 for label in ALL_LABELS_FIXED}
                
    for seg1 in ALL_SEGMENTS:
        for seg2 in ALL_SEGMENTS:
            if seg1 != seg2: 
                transition = f"{seg1}{seg2}"
                structure[cam_ID]['Predicted Counts'][transition] = {label: 0 for label in ALL_LABELS_FIXED}
    return structure

def update_json_structure(segment_data, tracking, BASE_DIR, output_file, cam_ID,i):
    """
    Updates the JSON structure with cumulative counts based on the current tracking data.

    Args:
        segment_data (dict): Dictionary with segment names as keys and coordinates as values.
        tracking (pd.DataFrame): DataFrame containing tracking data.
        BASE_DIR (str): Base directory for file operations.
        output_file (str): Path to the JSON file to be updated.
        cam_ID (str): The camera ID used to update the structure.
        i (int): Index or iteration counter to determine if the file should be loaded or initialized.

    Returns:
        list: The current track list with minute, label, and transition information.
    """
    if os.path.exists(output_file) and i!=0:
        with open(output_file, 'r') as file:
            structure = json.load(file)
    else:
        structure = initialize_json_structure(cam_ID)

        
    current_track_list = core(segment_data,tracking)
    with open(f'{BASE_DIR}/Asset/possible_pattern.json', 'r') as file:
        patt = json.load(file)
        
    allowed_pattern = patt[cam_ID]
    
    for item in current_track_list:
        _, label, transition = item
        if label in ALL_LABELS_FIXED and transition in structure[cam_ID]['Cumulative Counts']:
            if transition  in allowed_pattern:
                structure[cam_ID]['Cumulative Counts'][transition][label] += 1
            
        
            
    with open(output_file, 'w') as file:
        json.dump(structure, file, indent=4)
        
    return current_track_list
