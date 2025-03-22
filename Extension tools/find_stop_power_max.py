# -*- coding: utf-8 -*-
"""
Find the position where acceleration starts and maximum energy consumption occurs.

Example of inserting a file:

Insert file path: "C:\\Users\\User\\Desktop\\route.csv"

"""
import pandas as pd
import numpy as np
from colorama import init, Fore, Style
from tqdm import tqdm

# Initialize colorama
init()

# Set pandas display options
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print(r'''
 _____   _               _                                           
|  ___| (_)  _ __     __| |                                          
| |_    | | | '_ \   / _` |                                          
|  _|   | | | | | | | (_| |                                          
|_|     |_| |_| |_|  \__,_|                                          
 _                          _     _                              __  
| |   ___     ___    __ _  | |_  (_)   ___    _ __       ___    / _| 
| |  / _ \   / __|  / _` | | __| | |  / _ \  | '_ \     / _ \  | |_  
| | | (_) | | (__  | (_| | | |_  | | | (_) | | | | |   | (_) | |  _| 
|_|  \___/   \___|  \__,_|  \__| |_|  \___/  |_| |_|    \___/  |_|   
 _ __ ___     __ _  __  __    _ __     ___   __      __   ___   _ __ 
| '_ ` _ \   / _` | \ \/ /   | '_ \   / _ \  \ \ /\ / /  / _ \ | '__|
| | | | | | | (_| |  >  <    | |_) | | (_) |  \ V  V /  |  __/ | |   
|_| |_| |_|  \__,_| /_/\_\   | .__/   \___/    \_/\_/    \___| |_|   
                             |_|                                       
''')
print('')
print('Example of inserting a file')
print('Insert file path: "C:\\Users\\User\\Desktop\\route.csv"\n')

data_route = pd.read_csv(r"{}".format(input("Insert file path: ").replace('"', '')), encoding='utf-8') # Read the file
data_route.columns = ['distance', 'angle', 'set_speed', 'column0', 'column1'] # Set column names
data_route_describe = data_route.describe()       # Create DataFrame for statistical data usage data_route_describe.distance['max']

# Define variables for calculation
C_d = 0.51
Crr = 0.018
g = 9.81
m = 1000
acc_start = 1
acc = acc_start
Ro = 1.22
A = 10
#v_max = (5/18) * float(entry_V.get()) #km/hr to m/s
v_max = (5/18) * data_route['set_speed'].max() #km/hr to m/s
radius = 1
R = 1
position = 0.00
position_max = float(data_route_describe.distance['max'])
alpha = 0
v_t = 0.00
time = 0.00
power = 0.00
dt = 0.01
eff_motor = 0.85
run_turn = 1
power_stop_max_list = []

def position_stop_maxpower(index_number):
    v_t = 0
    time = 0
    position = data_route['distance'][index_number]
    power = 0
    alpha = data_route['angle'][index_number]
    max_speed = data_route['set_speed'].max() * (5 / 18)  # km/hr to m/s

    while position <= data_route['distance'].iloc[-1]:
        # Access data_route
        if index_number < len(data_route) - 1 and position >= data_route['distance'][index_number + 1]:
            index_number += 1
            alpha = data_route['angle'][index_number]

        # Acceleration condition
        if v_t >= max_speed:
            return power
        
        acc = acc_start if v_t < max_speed else 0

        # Calculation equations
        F_tractive = (m * acc) + (Crr * m * g) + (m * g * np.sin(np.deg2rad(alpha))) + ((1 / 2) * Ro * C_d * A * (v_t ** 2))

        # Calculate power
        if F_tractive > 0:
            T_wheel = F_tractive * radius
            W_wheel = v_t / radius
            N_wheel = (W_wheel * (60 / (2 * np.pi)))
            N_motor = R * N_wheel
            T_motor = T_wheel / R
            power = max(power, ((2 * np.pi * N_motor * T_motor) / 60) * (1 / eff_motor))

        # Update variables for the next loop
        time += dt
        v_t += acc * dt
        position += v_t * dt
        
        # Prevent infinite loop
        if time > 3600:  # Over 1 hour
            break
            
    return power

# Create DataFrame to store results
results = []
for index_number_position in tqdm(range(len(data_route.distance)), desc="Processing Data"):
    power = position_stop_maxpower(index_number_position)
    results.append({
        'distance': data_route['distance'][index_number_position],
        'power': power
    })

# Create DataFrame from all results at once
power_stop_max = pd.DataFrame(results)
power_stop_max = power_stop_max.dropna()
# Display calculation results
print(f"\n{Fore.CYAN}Calculation results for maximum power at each position:{Style.RESET_ALL}")
print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
print(power_stop_max.to_string(float_format=lambda x: '{:.2f}'.format(x)))
print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)

# Find the maximum power value and the position where it occurs
max_power_row = power_stop_max.loc[power_stop_max['power'].idxmax()]
print(f"\n{Fore.GREEN}Maximum Power:{Style.RESET_ALL} {Fore.RED}{max_power_row['power']:.2f}{Style.RESET_ALL} Watts")
print(f"{Fore.GREEN}Occurs at Position:{Style.RESET_ALL} {Fore.RED}{max_power_row['distance']:.2f}{Style.RESET_ALL} Meters")

# Display all rankings from highest to lowest
print(f"\n{Fore.CYAN}All power rankings (from highest to lowest):{Style.RESET_ALL}")
print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
sorted_power = power_stop_max.sort_values('power', ascending=False).reset_index(drop=True)
# Add ranking column
sorted_power.index = sorted_power.index + 1
sorted_power = sorted_power.rename_axis('Rank')
print(sorted_power.to_string(float_format=lambda x: '{:.2f}'.format(x)))
print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)

input('\n_____Press Enter to Exit_____')
