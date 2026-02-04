import fastf1
import pandas as pd
import os

YEAR = 2025 

dir = os.getcwd()
project_root = os.path.abspath(dir)
cache_patch = os.path.join(project_root)
fastf1.Cache.enable_cache(cache_patch)

FINAL_COLUMNS = [
    'RoundNumber', 'LapNumber', 'DriverNumber', 
    'Speed', 'RPM', 'nGear', 'Throttle', 'Brake'
]

all_races_telemetry = []

for i in range(1, 25): 
    if i == 22:
        continue

    session = fastf1.get_session(YEAR, i, 'R')
    session.load(telemetry=True, weather=False, messages=False)
    
    laps = session.laps
    laps = laps.pick_wo_box()

    round_telemetry_chunks = []

    for _, lap in laps.iterrows():
        tel = lap.get_telemetry()
        tel = tel[['Speed', 'RPM', 'nGear', 'Throttle', 'Brake']].copy()
        
        tel['RoundNumber'] = i
        tel['LapNumber'] = lap['LapNumber']
        tel['DriverNumber'] = lap['DriverNumber']

        tel['Speed'] = tel['Speed'].astype('float32')
        tel['RPM'] = tel['RPM'].astype('uint16')      
        tel['nGear'] = tel['nGear'].astype('uint8')
        tel['Throttle'] = tel['Throttle'].astype('float32')
        tel['Brake'] = tel['Brake'].astype('bool')
        
        tel['RoundNumber'] = tel['RoundNumber'].astype('uint8')
        tel['LapNumber'] = tel['LapNumber'].astype('uint8') 
        tel['DriverNumber'] = tel['DriverNumber'].astype('uint8') 

        round_telemetry_chunks.append(tel)

    round_df = pd.concat(round_telemetry_chunks, ignore_index=True)
    round_df = round_df[FINAL_COLUMNS]        
    all_races_telemetry.append(round_df)

    del session
    del laps

full_df = pd.concat(all_races_telemetry, ignore_index=True)
full_df = full_df.reset_index(drop=True)

full_file = os.path.join(project_root, 'data', 'f1_2025_telemetry.parquet')
full_df.to_parquet(full_file, index=False)
    
