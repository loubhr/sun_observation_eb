"""Just a visualization of the events as a function of time (x, y, t)

Input: raw file path

Parameters:
- start_ts: start timestamp for the event processing
- max_duration: maximum duration for the event processing
- ROI: region of interest x0, y0, xend, yend as a comma-separated string
- max_points_per_polarity: maximum number of ON/OFF points plotted each (set <=0 for no limit)

Output: 3D plot of events with x and y as spatial dimensions and time as the z-axis

Required packages: numpy, matplotlib, metavision_core, metavision_sdk_cv (from Prophesee SDK but open source version is openeb)
"""

import argparse
import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import ipdb

import os
import sys
import re
import traceback

from metavision_core.event_io import EventsIterator
from metavision_sdk_cv import TrailFilterAlgorithm

def map_3D(raw_file, ROI, dt=1e4, start_ts=8.50e6, max_duration=5e5, max_points_per_polarity=300000):
    """Function to create a 2D map of events as a function of time."""
    on_x, on_y, on_t = [], [], []
    off_x, off_y, off_t = [], [], []

    evt_iter = EventsIterator(raw_file, delta_t=dt, start_ts=start_ts, max_duration=max_duration)

    (height, width) = evt_iter.get_size() #evt_iter function to get sensor's size

    trail_filter = TrailFilterAlgorithm(height, width, 10000)
    out_evts = trail_filter.get_empty_output_buffer()

    for events in evt_iter:

        trail_filter.process_events(events, out_evts)

        for x, y, pol, ts in events:
            if ROI[0] <= x < ROI[2] and ROI[1] <= y < ROI[3]:
                rel_x = x
                rel_y = y
                rel_t = ts

                if pol == 1:
                    on_x.append(rel_x)
                    on_y.append(rel_y)
                    on_t.append(rel_t)
                else:
                    off_x.append(rel_x)
                    off_y.append(rel_y)
                    off_t.append(rel_t)

    on_x = np.asarray(on_x, dtype=np.int32)
    on_y = np.asarray(on_y, dtype=np.int32)
    on_t = np.asarray(on_t, dtype=np.int32)

    off_x = np.asarray(off_x, dtype=np.int32)
    off_y = np.asarray(off_y, dtype=np.int32)
    off_t = np.asarray(off_t, dtype=np.int32)

    return {
        "on": (on_x, on_y, on_t),
        "off": (off_x, off_y, off_t),
    }


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Prophesee nb events CTF")

    parser.add_argument("-r", "--raw-file", dest="raw_file", required=True,
                        help="Raw file path.")

    parser.add_argument("-o", "--output-folder", dest="output_folder", required=False,
                        help="Path to the output folder")
    
    parser.add_argument("-start_ts", "--start-timestamp", dest="start_ts", required=False,
                        default=8.50e6,
                        type=float,
                        help="Start timestamp for the event processing")
    
    parser.add_argument("-max_d", "--max-duration", dest="max_duration", required=False,
                        default=5e5,
                        type=float,
                        help="Maximum duration for the event processing")

    parser.add_argument("-roi", "--ROI", dest="ROI", required=False,
                        default= "0, 0, 1280, 720",
                        type=str,
                        help="Region of interest x0, y0, xend, yend as a comma-separated string")
    
    parser.add_argument("-save", "--save-figures", dest="save_figures", action='store_true',
                        help="Flag to save the figures instead of only displaying them")

    parser.add_argument("--max-points-per-polarity", dest="max_points_per_polarity", required=False,
                        default=300000,
                        type=int,
                        help="Maximum number of ON/OFF points plotted each (set <=0 for no limit)")
    
    args = parser.parse_args()

    # Parse the ROI argument
    ROI = list(map(int, args.ROI.split(',')))

    # Create the 3D map of events as a function of time
    map_3d = map_3D(
        args.raw_file,
        ROI,
        dt=1e4,
        start_ts=args.start_ts,
        max_duration=args.max_duration,
        max_points_per_polarity=args.max_points_per_polarity,
    )

    # Plot the 3D ON and OFF maps as a 3D graph with x and y as spatial dimensions and time as the z-axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x_data_ON, y_data_ON, time_data_ON = map_3d["on"]
    y_data_ON = 720 - y_data_ON # Invert y-axis for better visualization (optional)

    x_data_OFF, y_data_OFF, time_data_OFF = map_3d["off"]
    y_data_OFF = 720 - y_data_OFF # Invert y-axis for better visualization (optional)

    ax.scatter(x_data_ON, y_data_ON, time_data_ON, c='r', label='ON events', s=0.5)
    ax.scatter(x_data_OFF, y_data_OFF, time_data_OFF, c='b', label='OFF events', s=0.5)

    ax.set_xlabel('x (pixel)')
    ax.set_ylabel('y (pixel)')
    ax.set_zlabel('time (µs)')
    ax.set_title('Events 3D representation as a function of time')
    ax.legend()

    if args.save_figures:
        raw_basename = os.path.splitext(os.path.basename(args.raw_file))[0]
        output_path = os.path.join(args.output_folder, f"{raw_basename}_3D_map_xy_time.png")
        plt.savefig(output_path)
        print(f"Figure saved to {output_path}")

    plt.show()

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("Process interrupted by user. Exiting...")
        sys.exit(0)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        tb = traceback.extract_tb(sys.exc_info()[2])
        if tb:
            filename, lineno, func, text = tb[-1]
            print(f"Error occurred in file '{filename}', line {lineno}, in {func}: {text}")
        traceback.print_exc()
        sys.exit(1) 
