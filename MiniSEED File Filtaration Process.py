import os
from obspy import read
import numpy as np
import matplotlib.pyplot as plt

# Define file name and paths
file_name = 'XB.ELYSE.02.BHV.2022-02-03HR08_evid0005.mseed'  # The MiniSEED file
output_folder = 'filtered_data'  # Folder to save the filtered files
event_time = 507  # The time of ocurrence of the seismic event in seconds
event_duration = 20  # Duration to include around the event in seconds

# Create output folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Read the MiniSEED file
stream = read(file_name)

# Create event and noise segments
event_start = event_time - event_duration
event_end = event_time + event_duration

# Filter data for the seismic event
event_data = stream.slice(starttime=stream[0].stats.starttime + event_start,
                          endtime=stream[0].stats.starttime + event_end)

# Filter data for noise (all data outside the event window)
noise_data = stream.slice(starttime=stream[0].stats.starttime,
                          endtime=stream[0].stats.starttime + event_start)

# Add noise segments after the event
noise_data += stream.slice(starttime=stream[0].stats.starttime + event_end,
                           endtime=stream[0].stats.endtime)

# Save the event and noise data to new files
event_file = os.path.join(output_folder, 'event_data.mseed')
noise_file = os.path.join(output_folder, 'noise_data.mseed')

event_data.write(event_file, format='MSEED')
noise_data.write(noise_file, format='MSEED')

print(f'Filtered event data saved to: {event_file}')
print(f'Filtered noise data saved to: {noise_file}')


# Visualization
def plot_data(stream, title, full_scale=False):
    plt.figure(figsize=(15, 5))
    plt.plot(stream[0].times(), stream[0].data, color='blue')
    plt.title(title)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.xlim(stream[0].times()[0], stream[0].times()[-1])

    # Set y-axis limits for noise data if requested
    if full_scale:
        plt.ylim(-1.5 * np.max(np.abs(stream[0].data)), 1.5 * np.max(np.abs(stream[0].data)))
    else:
        plt.ylim(np.min(stream[0].data), np.max(stream[0].data))

    plt.grid()
    plt.show()


# Read and visualize the saved event data
saved_event_data = read(event_file)
plot_data(saved_event_data, 'Filtered Event Data')

# Read and visualize the saved noise data (with full scale)
saved_noise_data = read(noise_file)
plot_data(saved_noise_data, 'Filtered Noise Data', full_scale=True)
