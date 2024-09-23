import cv2
from ultralytics import YOLO
import pandas as pd
from tqdm import tqdm


def trak(model_path, video_path, add):
    """
    This function performs object tracking on a given video using a pre-trained YOLO model.

    Parameters:
        model_path (str): Path to the YOLO model file.
        video_path (str): Path to the video file.
        add (int): An additional value to be added to the calculated 'Min' column in the output data.

    Returns:
        pd.DataFrame: A DataFrame containing the tracking data with columns ['Min', 'ID', 'X', 'Y', 'Label'].
        width (int): The width of the video frames.
        height (int): The height of the video frames.
    """
    
    model = YOLO(model_path)
    class_labels = ["Bicycle", "Bus", "Car", "LCV", "Three Wheeler", "Truck", 'Two Wheeler']

    cap = cv2.VideoCapture(video_path)
    data = []
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_id = 0

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    
    with tqdm(total=total_frames, desc="Processing Video") as pbar:
        while cap.isOpened():
            success, frame = cap.read()
            if success:
                frame_id+=1
                results = model.track(frame, persist=True, verbose=False, iou=0.10)
                pbar.update(1)
                if results[0].boxes:
                    boxes = results[0].boxes.xywh.cpu().numpy()
                    track_ids = results[0].boxes.id
                    classes = results[0].boxes.cls
                    if track_ids is not None and classes is not None:
                        track_ids = track_ids.int().cpu().tolist()
                        classes = classes.int().cpu().tolist()
                        for box, track_id, cls in zip(boxes, track_ids, classes):
                            x, y, w, h = box
                            center_x = x + w / 2
                            center_y = y + h / 2
                            class_label = class_labels[cls]
                            data.append([int(frame_id/(fps*60))+add, track_id, center_x, center_y, class_label])
            else:
                print("Completed")
                break
        
        cap.release()
    
    return pd.DataFrame(data, columns=['Min','ID', 'X', 'Y', 'Label']), width, height, int(frame_id/(fps*60))+add






















########################################## IGNORE ###########################################




def botsort():
    # tracker_type: botsort # tracker type, ['botsort', 'bytetrack']
    # track_high_thresh: 0.5 # threshold for the first association
    # track_low_thresh: 0.1 # threshold for the second association
    # new_track_thresh: 0.6 # threshold for init new track if the detection does not match any tracks
    # track_buffer: 30 # buffer to calculate the time when to remove tracks
    # match_thresh: 0.8 # threshold for matching tracks
    # fuse_score: True # Whether to fuse confidence scores with the iou distances before matching
    # # min_box_area: 10  # threshold for min box areas(for tracker evaluation, not used for now)

    # # BoT-SORT settings
    # gmc_method: sparseOptFlow # method of global motion compensation
    # # ReID model related thresh (not supported yet)
    # proximity_thresh: 0.5
    # appearance_thresh: 0.25
    # with_reid: False
    pass

def bytetrack():
    # tracker_type: bytetrack # tracker type, ['botsort', 'bytetrack']
    # track_high_thresh: 0.5 # threshold for the first association
    # track_low_thresh: 0.1 # threshold for the second association
    # new_track_thresh: 0.6 # threshold for init new track if the detection does not match any tracks
    # track_buffer: 30 # buffer to calculate the time when to remove tracks
    # match_thresh: 0.8 # threshold for matching tracks
    # fuse_score: True # Whether to fuse confidence scores with the iou distances before matching
    pass




# def trak(model_path, video_path,BASE_DIR):
#     model = YOLO(model_path)
#     class_labels = ["Bicycle", "Bus", "Car", "LCV", "Three-Wheeler", "Truck", 'Two-Wheeler']

#     cap = cv2.VideoCapture(video_path)
#     data = []
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    
#     with tqdm(total=total_frames, desc="Processing Video") as pbar:
#         while cap.isOpened():
#             success, frame = cap.read()
#             if success:
#                 # results = model.track(frame, persist=True, verbose=False, iou=0.10, conf=0.65, tracker = f'{BASE_DIR}/Asset/botsort.yaml' )
#                 results = model.track(frame, persist=True, verbose=False, iou=0.1)
#                 pbar.update(1)
#                 if results[0].boxes:
#                     boxes = results[0].boxes.xywh.cpu().numpy()
#                     track_ids = results[0].boxes.id
#                     classes = results[0].boxes.cls
#                     if track_ids is not None and classes is not None:
#                         track_ids = track_ids.int().cpu().tolist()
#                         classes = classes.int().cpu().tolist()
#                         for box, track_id, cls in zip(boxes, track_ids, classes):
#                             x, y, w, h = box
#                             center_x = x + w / 2
#                             center_y = y + h / 2
#                             class_label = class_labels[cls]
#                             data.append([track_id, center_x, center_y, class_label])
#             else:
#                 print("Completed")
#                 break
        
#         cap.release()
    
#     return pd.DataFrame(data, columns=['ID', 'X', 'Y', 'Label']), width, height


