import pandas as pd
from datetime import datetime
import time
import os
import sys
import pdb

def main(argv):
    
    datapath = os.path.abspath(argv[1])  # raw
    outpath = os.path.abspath(argv[2])  # interim

    images = pd.read_csv(os.path.join(datapath, 'images.csv'))
    reports = pd.read_csv(os.path.join(datapath, 'NCDC-CDO-LCD.csv'))
    reports['unix_time'] = reports['DATE'].apply(parse_date)

    pdb.set_trace()
    for i in images.index:
        image_time = images.ix[i]['date_added']
        # utcfromtimestamp assumes I am in CST ?
        image_time = datetime.utcfromtimestamp(image_time)

        # TODO: convert to EST
        # TODO: look up closest time in reports
        # TODO: parse report codes and determine if raining
        # TODO: add raininglabel to images df

        
    
    # Write out
    images.to_csv(os.path.join(outpath, 'images.csv'), index=False)

def parse_date(string):
    # https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
    dt = datetime.strptime(string, '%Y-%m-%d %H:%M')
    # mktime assumes datetime object is in UTC??
    unix_time = int(time.mktime(dt.timetuple()))
    return unix_time

if __name__ == '__main__':
    main(sys.argv)
