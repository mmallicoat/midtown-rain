import pandas as pd
from datetime import datetime
import time
import pytz
import os
import sys
import pdb

def main(argv):
    
    datapath = os.path.abspath(argv[1])  # raw
    outpath = os.path.abspath(argv[2])  # interim

    images = pd.read_csv(os.path.join(datapath, 'images.csv'))
    reports = pd.read_csv(os.path.join(datapath, 'NCDC-CDO-LCD.csv'))
    reports['unix_time'] = reports['DATE'].apply(parse_date)

    for i in images.index:
        image_time = images.ix[i]['date_added']
        # Datetime object is "offset-naive," but UTC is implicit
        # image_time = datetime.utcfromtimestamp(image_time)
        pdb.set_trace()

        # TODO: look up closest time in reports['unix_time']
        # TODO: parse report codes and determine if raining
        # TODO: add raininglabel to images df
        
    
    # Write out
    images.to_csv(os.path.join(outpath, 'images.csv'), index=False)

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
