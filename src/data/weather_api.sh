DIR="."
TOKEN=`cat $DIR/mytoken`  # read in token
OUTFILE=$DIR/data/raw/noaa_response.json

# Get all stations, sorting by city?
REQUEST="https://www.ncdc.noaa.gov/cdo-web/api/v2/locations?locationcategoryid=CITY&sortfield=name&sortorder=desc"

# Get all stations in state of New York (FIPS 36)
REQUEST="https://www.ncdc.noaa.gov/cdo-web/api/v2/stations?locationid=FIPS:36"

# Get info about Central Park station (COOP ID 305801)
REQUEST="https://www.ncdc.noaa.gov/cdo-web/api/v2/stations/COOP:305801"

# Get datasets for Central Park station
REQUEST="https://www.ncdc.noaa.gov/cdo-web/api/v2/datasets?stationid=COOP:305801"
# Only dataset is "Precipitation Hourly" from 1900-01-01 to 2014-01-01

curl -H "token:$TOKEN" $REQUEST -o $OUTFILE
