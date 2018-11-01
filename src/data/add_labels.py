import pandas as pd
import numpy as np
from datetime import datetime
import time
import pytz
import re
import os
import sys
import pdb

def main(argv):
    
    datapath = os.path.abspath(argv[1])  # raw
    outpath = os.path.abspath(argv[2])  # interim

    # TODO: look into 'mixed datatype' warning

    # Read in and sort data tables
    images = pd.read_csv(os.path.join(datapath, 'images.csv'))
    images.sort_values(by='date_added', inplace=True)
    images.reset_index(drop=True, inplace=True)

    reports = pd.read_csv(os.path.join(datapath, 'NCDC-CDO-LCD.csv'))
    reports['unix_time'] = reports['DATE'].apply(parse_date)
    # Drop weather observations before start of image series
    cutoff_dt = datetime(2017, 11, 3)
    time_zero = datetime(1970, 1, 1)
    cutoff_unix = int((cutoff_dt - time_zero).total_seconds())
    reports = reports[reports['unix_time'] > cutoff_unix]
    reports.sort_values(by='unix_time', inplace=True)
    reports.reset_index(drop=True, inplace=True)

    # Binary search
    for i in images.index:
        image_time = images.loc[i]['date_added']
        m = binary_search(image_time, reports['unix_time'])
        if m == -1:
            # No close observation in weather reports
            break
        report_time = reports.loc[m]['unix_time']
        diff = image_time - report_time
        if diff > 1800:
            # choose m + 1
            observation = reports.loc[m + 1]['HOURLYPRSENTWEATHERTYPE']
        elif diff < -1800:
            # choose m - 1
            observation = reports.loc[m - 1]['HOURLYPRSENTWEATHERTYPE']
        else:
            # choose m
            observation = reports.loc[m]['HOURLYPRSENTWEATHERTYPE']
        images.at[i, 'rain'] = parse_label(observation)

    # Drop images without label; write out data
    images = images[images['rain'].notna()]
    images.to_csv(os.path.join(outpath, 'images.csv'), index=False)

# For reference, see:
# https://en.wikipedia.org/wiki/Binary_search_algorithm#Procedure
def binary_search(value, series):
    # Find the index of the value in target_series closest to the
    # search value.
    # series is a pandas Series holding integers. value is an integer.
    n = len(series)
    L = 0
    R = n - 1
    # return binary_search(value, series[L:R+1])
    while L <= R:
        m = (L + R) / 2  # since integers, returns floor
        if 3600 < value - series.loc[m]:
            L = m + 1
        elif -3600 > value - series.loc[m]:
            R = m - 1
        else:
            return m  # value within +/- 3600 of series.loc[m]
    return -1  # value not found

def parse_label(observation):
    # Parse observations for indicators of rain
    if type(observation) is not str:
        return 0  # no observation
    try:
        AU, AW, MW = observation.split('|')
    except:
        print("Observation is malformed")
    AU_re = re.search(r'RA:02', AU)
    AW_re = re.search(r'RA:6\d', AW)
    if AU_re or AW_re:
        return 1  # rain was observed
    else:
        return 0  # rain was not observed

def parse_date(string):
    dt = datetime.strptime(string, '%Y-%m-%d %H:%M')
    # Set timezone to make "offset-aware"
    # The weather data is always in EST, ignoring DST
    dt = dt.replace(tzinfo=pytz.timezone('EST'))
    # Time zero of Unix epoch, with timezone information added
    time_zero = datetime(1970, 1, 1).replace(tzinfo=pytz.timezone('UTC'))
    unix_time = int((dt - time_zero).total_seconds())
    return unix_time

if __name__ == '__main__':
    main(sys.argv)
