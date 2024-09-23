
# Python Tracking and Forecasting Application

## Project Overview

This application is designed to perform vehicle tracking and traffic pattern forecasting based on input video data and segment regions. The process is orchestrated by the `app.py` script, which serves as the main entry point for running the entire pipeline.

## Features

- **Tracking:** Utilizes a pre-trained model (`640.pt`) to track vehicles in video segments.
- **Segmentation:** Processes and unnormalizes segment data to ensure accurate region mapping.
- **Pattern Update:** Updates the tracking structure to reflect correct region transitions.
- **Forecasting:** Predicts future traffic patterns based on the current tracking data.

## Requirements

- **Python 3.8+**
- **Dependencies:** Listed in the `Dockerfile` or can be manually installed using `pip`.

## File Structure

- **app.py:** Main entry point for running the application.
- **Dockerfile:** Used to create a Docker container for the application.
- **Asset/**: Directory containing auxiliary scripts, models, and configuration files:
  - `640.pt`: Pre-trained model for tracking.
  - `future_OTG.py`: Handles forecasting of future traffic patterns.
  - `get_segment.py`: Manages the retrieval and normalization of segment data.
  - `pattern.py`: Updates the tracking JSON structure.
  - `run_tracker.py`: Executes the tracking process.
  - `possible_pattern.json`, `segments_fixed.json`: JSON files with configuration details.

## Usage

### Running Locally

1. **Prepare the Input:**
   - Create a JSON file with the required input data (e.g., `input_file2.json`).

2. **Run the Application:**
   ```bash
   python app.py <input_file> <output_file>
   ```
   - `<input_file>`: Path to the input JSON file.
   - `<output_file>`: Path to the output JSON file where results will be saved.

### Using Docker

1. **Build the Docker Image:**
   ```bash
   docker build -t traffic-tracking-app .
   ```

2. **Run the Docker Container:**
   ```bash
   docker run --rm -v $(pwd):/app traffic-tracking-app <input_file> <output_file>
   ```

## Input JSON Structure

The input JSON file should have the following structure:

```json
{
    "CamID": {
        "segment1": "path/to/segment1/video",
        "segment2": "path/to/segment2/video"
    }
}
```

- **CamID**: Identifier for the camera or location.
- **segment1, segment2, ...**: Paths to the video segments that need to be processed.

## Output

The output will be a JSON file that contains the processed tracking data and the forecasted traffic patterns. This file can be used for further analysis or visualization.

## License

This project is licensed under the MIT License.
