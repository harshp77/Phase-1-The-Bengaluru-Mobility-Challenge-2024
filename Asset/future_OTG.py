import pandas as pd
import json
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX



def forecast(final_tracking, cam_ID, structure, BASE_DIR):
    
    """
    Forecasts the vehicle movement patterns based on tracking data.

    Args:
        final_tracking (list of lists): The tracking data, where each sublist contains minute, label, and transition information.
        cam_ID (str): The camera ID used to fetch allowed patterns.
        structure (dict): The data structure containing predicted counts for various transitions and labels.
        BASE_DIR (str): The base directory for file operations.

    Returns:
        dict: Updated structure with forecasted counts for the next 30 minutes.
    """

    flattened_list = [item for sublist in final_tracking for item in sublist]

    df = pd.DataFrame(flattened_list, columns=["Minute", "Label", "Transition"])
    
    df['unique_track_Label'] = df['Transition'] + '_' + df['Label']  

    unique_combinations = df['unique_track_Label'].unique()
    minutes = range(30)  
    cumulative_df = pd.DataFrame(index=minutes)

    for combination in unique_combinations:
        cumulative_df[combination] = 0
        filtered_df = df[df['unique_track_Label'] == combination]

        for minute in minutes:
            cumulative_count = filtered_df[filtered_df['Minute'] <= minute].shape[0]
            cumulative_df.at[minute, combination] = cumulative_count

    growth_rate = (cumulative_df.loc[29] - cumulative_df.loc[0]) / 29
    forecast_60th_minute = cumulative_df.loc[29] + growth_rate * 30
    forecast_next_30_min = forecast_60th_minute - cumulative_df.loc[29]

    forecast_next_30_min_df = pd.DataFrame(forecast_next_30_min).T
    forecast_next_30_min_df.columns = [col for col in forecast_next_30_min_df.columns]
    
    with open(f'{BASE_DIR}/Asset/possible_pattern.json', 'r') as file:
        patt = json.load(file)
        
    allowed_pattern = patt[cam_ID]

    for column in forecast_next_30_min_df.columns:
        transition, label = column.split('_', 1) 

        if transition in structure[cam_ID]['Predicted Counts'] and label in structure[cam_ID]['Predicted Counts'][transition]:
            if transition in allowed_pattern:
                structure[cam_ID]['Predicted Counts'][transition][label] += int(forecast_next_30_min_df[column].values[0])

    return structure



# def forecast(final_tracking, cam_ID, structure, BASE_DIR):

#     flattened_list = [item for sublist in final_tracking for item in sublist]

#     df = pd.DataFrame(flattened_list, columns=["Minute", "Label", "Transition"])
    
#     df['unique_track_Label'] = df['Transition'] + '_' + df['Label']  

#     minutes = range(30)  
#     cumulative_df = pd.DataFrame(index=minutes)

#     forecast_next_30_min = {}

#     for column in cumulative_df.columns:
#         # model = ARIMA(cumulative_df[column], order=(1, 1, 1))
#         # fit = model.fit()
            
#         seasonal_order = (1, 1, 1, 12)  
#         model = SARIMAX(cumulative_df[column], order=(1, 1, 1), seasonal_order=seasonal_order)
#         fit = model.fit()
            
#         forecast_60th_minute = fit.forecast(steps=30)
        
#         forecast_next_30_min[column] = forecast_60th_minute.iloc[-1] - cumulative_df[column].iloc[-1]

#     forecast_next_30_min_df = pd.DataFrame(forecast_next_30_min, index=[0])

#     forecast_next_30_min_df = pd.DataFrame(forecast_next_30_min).T
#     forecast_next_30_min_df.columns = [col for col in forecast_next_30_min_df.columns]
    
#     with open(f'{BASE_DIR}/Asset/possible_pattern.json', 'r') as file:
#         patt = json.load(file)
        
#     allowed_pattern = patt[cam_ID]

#     for column in forecast_next_30_min_df.columns:
#         transition, label = column.split('_', 1) 

#         if transition in structure[cam_ID]['Predicted Counts'] and label in structure[cam_ID]['Predicted Counts'][transition]:
#             if transition in allowed_pattern:
#                 structure[cam_ID]['Predicted Counts'][transition][label] += int(forecast_next_30_min_df[column].values[0])

#     return structure