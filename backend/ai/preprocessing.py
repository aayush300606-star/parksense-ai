import os
import pandas as pd
import numpy as np

RAW_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'jan to may police violation_anonymized791b166.csv')
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
CLEANED_DATA_PATH = os.path.join(PROCESSED_DIR, 'cleaned_dataset.csv')

def preprocess_data(file_path: str = RAW_DATA_PATH) -> pd.DataFrame:
    """
    Loads and preprocesses the parking violation dataset.
    """
    print(f"Loading raw dataset from {file_path}...")
    df = pd.read_csv(file_path)
    
    # Remove duplicate records
    print(f"Removing duplicates. Initial rows: {len(df)}")
    df = df.drop_duplicates()
    print(f"Rows after removing duplicates: {len(df)}")
    
    # Handle missing coordinates and values
    df = df.dropna(subset=['latitude', 'longitude', 'created_datetime'])
    
    # Remove invalid coordinates (Bangalore bounds roughly)
    # Latitude: 12.0 to 14.0, Longitude: 77.0 to 78.0
    df = df[(df['latitude'] >= 12.0) & (df['latitude'] <= 14.0)]
    df = df[(df['longitude'] >= 77.0) & (df['longitude'] <= 78.0)]
    
    # Standardize coordinates
    df['latitude'] = df['latitude'].round(6)
    df['longitude'] = df['longitude'].round(6)
    
    # Parse timestamps
    df['created_datetime'] = pd.to_datetime(df['created_datetime'], errors='coerce')
    df = df.dropna(subset=['created_datetime'])
    
    # Generate temporal features
    df['hour'] = df['created_datetime'].dt.hour
    df['day'] = df['created_datetime'].dt.day
    df['weekday'] = df['created_datetime'].dt.day_name()
    df['month'] = df['created_datetime'].dt.month
    df['is_weekend'] = df['created_datetime'].dt.dayofweek >= 5
    
    # Time slot generation (Morning, Afternoon, Evening, Night)
    def get_time_slot(h):
        if 6 <= h < 12: return 'Morning'
        if 12 <= h < 16: return 'Afternoon'
        if 16 <= h < 20: return 'Evening'
        return 'Night'
        
    df['time_slot'] = df['hour'].apply(get_time_slot)
    
    # Peak hour generation (9-11 AM, 5-8 PM)
    df['peak_hour'] = df['hour'].apply(lambda x: 1 if (9 <= x <= 11) or (17 <= x <= 20) else 0)
    
    # Sort chronologically
    df = df.sort_values(by='created_datetime').reset_index(drop=True)
    
    # Violation frequency: simple global count per location logic or let's keep it as is
    # Using group by location rounding to 3 decimals to find frequency
    df['lat_grid'] = df['latitude'].round(3)
    df['lon_grid'] = df['longitude'].round(3)
    freq_map = df.groupby(['lat_grid', 'lon_grid']).size().reset_index(name='violation_frequency')
    df = pd.merge(df, freq_map, on=['lat_grid', 'lon_grid'], how='left')
    df = df.drop(columns=['lat_grid', 'lon_grid'])
    
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    print(f"Saving cleaned dataset to {CLEANED_DATA_PATH}...")
    # For speed and size, we might only want to save a sample if it's too big, 
    # but the task requires saving the cleaned data.
    # If the file is 100MB, saving it to CSV is fine.
    df.to_csv(CLEANED_DATA_PATH, index=False)
    print("Preprocessing completed.")
    
    return df

if __name__ == '__main__':
    preprocess_data()
