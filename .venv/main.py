# getting data from beam
from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Electrics

# big libary shiii
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

# sets up the connection , the initial call below is subjective to each setup, so the best way to do this would
# be calling for the (possibly different) port and grabbing the users game directory on startup
bng = BeamNGpy('localhost', 25252, home=r'D:\SteamLibrary\steamapps\common\BeamNG.drive')
bng.open(launch=False) # looks for running instance

# getting player vehicle
bng.get_current_vehicles()
vehicle = list(bng.vehicles.values())[0]
vehicle.connect(bng)

# initialize sensor
electrics = Electrics()
vehicle.attach_sensor('electrics', electrics)

# PLOT SETTINGS
UPDATE_INTERVAL = 0.5   # seconds
MAX_POINTS = 60

rpm_history = []
time_history = []
start_time = time.time()

fig, ax = plt.subplots(figsize=(10, 4))
line, = ax.plot([], [], color='tomato', linewidth=2)
ax.set_ylim(0, 8000)
ax.set_xlabel('Time (s)')
ax.set_ylabel('RPM')
ax.set_title('Engine RPM — Live')
ax.grid(True, alpha=0.3)

def update(frame):
    vehicle.poll_sensors()
    rpm = electrics.data.get('rpm', 0)

    elapsed = time.time() - start_time
    rpm_history.append(rpm)
    time_history.append(elapsed)

    t_win = time_history[-MAX_POINTS:]
    r_win = rpm_history[-MAX_POINTS:]

    line.set_data(t_win, r_win)
    ax.set_xlim(max(0, elapsed - MAX_POINTS * UPDATE_INTERVAL), elapsed + 1)
    return line,

ani = animation.FuncAnimation(
    fig, update,
    interval=UPDATE_INTERVAL * 1000,
    blit=True,
    cache_frame_data=False
)

plt.tight_layout()
plt.show()

bng.close()