import json  # Import the JSON module to work with JSON data

def unnormalize_segment_data(segment_data, width, height):
    """
    This function takes normalized segment data and converts it back to 
    the original pixel coordinates based on the provided image width and height.
    
    Parameters:
        segment_data (dict): A dictionary containing normalized segment coordinates.
        width (int): The width of the image.
        height (int): The height of the image.
    
    Returns:
        unnormalized_data (dict): A dictionary containing unnormalized segment coordinates.
    """
    unnormalized_data = {}
    
    # Loop through each segment in the segment_data dictionary
    for key in segment_data.keys():
        coords = segment_data[key]  # Get the normalized coordinates for the current segment
        # Unnormalize the coordinates based on the image dimensions (width, height)
        unnormalized_data[key] = {
            "x1": int(coords["x1"] * width),
            "y1": int(coords["y1"] * height),
            "x2": int(coords["x2"] * width),
            "y2": int(coords["y2"] * height)
        }
    
    return unnormalized_data  # Return the dictionary with unnormalized coordinates

def run_get_segment_json(cam_id, BASE_DIR):
    """
    This function retrieves segment data from a JSON file for a specific camera ID.
    
    Parameters:
        cam_id (str): The camera ID for which to retrieve the segment data.
        BASE_DIR (str): The base directory path where the segments_fixed.json file is located.
    
    Returns:
        dict: The segment data for the specified camera ID.
    """
    # Open and load the segment data JSON file
    with open(f"{BASE_DIR}/Asset/segments_fixed.json") as f:
        data = json.load(f)

    return data[cam_id]  # Return the segment data corresponding to the given camera ID
