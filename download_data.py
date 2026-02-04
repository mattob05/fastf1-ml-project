import os
import fastf1
import pandas as pd

dir = os.getcwd()
project_root = os.path.abspath(dir)
cache_patch = os.path.join(project_root)
fastf1.Cache.enable_cache(cache_patch)

all_data_race = []
all_data_quali = []
for i in range(1, 25):
    if i == 22:
        continue
    session = fastf1.get_session(2025, i, 'R')
    session.load(weather=True, telemetry=True, messages=False)
    quali = fastf1.get_session(2025, i, 'Q')
    quali.load(weather=False, telemetry=False, messages=False)
    q = quali.laps.copy()
    q = q.pick_quicklaps()
    q = q.reset_index(drop=True)
    laps = session.laps
    laps = laps.pick_wo_box()
    laps = laps.reset_index(drop=True)

    weather_data = laps.get_weather_data()
    laps = laps.sort_values('Time')

    weather_data = weather_data.sort_values('Time')
    df = pd.merge_asof(laps, weather_data[['Time', 'TrackTemp', 'Rainfall', 'WindSpeed']], on='Time', direction='nearest')

    df['RoundNumber'] = i
    q['RoundNumber'] = i

    all_data_race.append(df)
    all_data_quali.append(q)
    if i == 1:
        break

full_df = pd.concat(all_data_race, ignore_index=True)
output_file = os.path.join(project_root, 'data', 'f1_data.csv')
full_df.to_csv(output_file, index=False)

quali_df = pd.concat(all_data_quali, ignore_index=True)
quali_file = os.path.join(project_root, 'data', 'f1_quali_data.csv')
quali_df.to_csv(quali_file, index=False)
