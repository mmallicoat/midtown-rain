Notes
=====

Todo
----

*   Write code to process images: convert to greyscale, reduce
    size/dimensionality
*   Figure out API to get historical weather data
*   Write script to get weather data correpsonding to time of images;
    we only need a binary variable 'raining' vs. 'not raining' I think
*   Figure out which algorithm to use to train the model;
    Convolutional NN?
*   Find library to implement training algorithm, etc.

Done
----
*   Is there a weather station near Times Square?
    Should I pick a different camera location?
    Central Park station and Midtown camera are good.
*   Write curl script to save URLs of images to a file
*   Write python script to extract URLs and collect
*   Write wget/curl script to download images



NWS API and Data
----------------

Historical Data
```````````````

The NWS is part of the NOAA. They have an `API portal
<https://graphical.weather.gov/xml/>`__.

NOAA publishes `data
<https://www.ncdc.noaa.gov/data-access/land-based-station-data/data-publications>`__.
`Local Climatological Data <https://www.ncdc.noaa.gov/IPS/lcd/lcd.html>`__ gives hourly preciptation data.
`Hourly Precipitation Data
<http://www.ncdc.noaa.gov/IPS/hpd/hpd.html>`__ also gives hourly
precipitation data by station.

I think here is `past weather data
<https://w2.weather.gov/climate/>`__.

Stations
````````

There is a list of `NWS stations
<https://www.weather.gov/arh/stationlist>`__.
Here is `another station list
<https://forecast.weather.gov/stations.php?foo=0>`__ including
**latitude and longitude** and an XML version.

There is also a `KML map
<https://www.weather.gov/ctwp/stationsmap>`__.
Here is a `map of radio stations <http://www.nws.noaa.gov/nwr/Maps/`__.

`KNYC <https://w1.weather.gov/obhistory/KNYC.html>`__ is located
in Central Park.

Here is a `tool for finding observation stations
<https://www.ncdc.noaa.gov/cdo-web/datatools/findstation>`__.

Station to Use
``````````````

KNYC is at (40.783, -73.967). It is at
`Belvedere Castle
<https://en.wikipedia.org/wiki/Belvedere_Castle>`__, which Google
Maps gives as (40.7794302, -73.9712617). This is about 1.8 miles
northeast of Times Square.

Per Google Maps, the lat and long of Times Square is (40.758895,
-73.987325). Earthcam has multiple cameras at this location and
the photos seem to be all mixed together. This may make the photos
unusable.

There is also an Earthcam at Columbus Circle at the southwest
corner of Central Park, which is about 1.2 miles away from the
weather station.


Earthcom
--------

The images_ on earthcam.com_ are timestamped in the filename with
the Unix epoch in milliseconds, with some other identifier
following an underscore. From their website, it would be possible
to scrape hundreds of timestamped photos from fixed, known
locations.

These could then be used to train an image classifier of some
kind. My suggestion is to join these images with historical
weather data, in particular precipitation, and then train a image
classifier to predict whether the image indicates it is clear, raining,
snowing, etc. at that location.

.. _earthcam.com: https://www.earthcam.com/usa/newyork/skyline/?cam=hyatthd
.. _images: https://static.earthcam.com/hof/newjersey/jerseycity/1526418900896_68.jpg

Besides the "Hall of Fame" images, also look at the "Archive"
button.

Cameras
```````

These are all fairly stationary and include sky and water:
*   `NYC Skyline from Jersey City Hyatt Regency
    <https://www.earthcam.com/usa/newyork/skyline/?cam=hyatthd>`__
*   `NYC Skyline from ???
    <https://www.earthcam.com/usa/newyork/skyline/?cam=skyline_pano>`__.
*   `World Trade Tower
    <https://www.earthcam.com/usa/newyork/worldtradecenter/?cam=skyline_g>`__.

`Midtown Manhattan
<https://www.earthcam.com/usa/newyork/midtown/skyline/?cam=midtown4k>`__,
with a view of what I think is the 432 Park Avenue building, the
second tallest in Manhattan, and I think the Chrysler Building,
405 Lexington Avenue. The camera may be located at the Affinia
Dumont hotel at 551 5th Ave. This is also only 2 miles from the
Central Park weather station.
(Or, it may be at Javits Center, 655 W 34th St. This name shows
when you click on an image in the HOF. The building does seem tall
enough, though, on Google Satellite view.)
I think it is looking roughly north up 5th Ave toward the 432 Park
Ave building, from near the Empire State Building. See Google
Satellite 3D view, oritented north.
At the bottom of `this image
<https://static.earthcam.com/hof/newyork/skyline/1538580430210_16.jpg>`__,
I think you see the top of 400 5th Ave. You can see the crane.
Because the camera is looking down on it and there are no other
taller buildings around, I think the camera must actually *be* in
the Empire State Building, on the north side.
`This image
<https://static.earthcam.com/hof/newyork/skyline/1538576240486_65.jpg>`__
maybe shows the cage in the area where people go up.
In the JSON request, the camera name is "empirestatebuilding"!

`Columbus Circle
<https://www.earthcam.com/usa/newyork/columbuscircle/?cam=columbus_circle>`__.

AJAX
----

Requests
````````

Full: https://www.earthcam.com/cams/common/gethofitems.php?hofsource=com&tm=ecn&camera=timessquare_hd&start=22&length=21&ec_favorite=0&cdn=0&callback=onjsonpload

Minimal: https://www.earthcam.com/cams/common/gethofitems.php

Works: https://www.earthcam.com/cams/common/gethofitems.php?camera=timessquare_hd

DNW: https://www.earthcam.com/cams/common/gethofitems.php?camera=timessquare_hd&start=22&length=21

Works: "https://www.earthcam.com/cams/common/gethofitems.php?camera=timessquare_hd&start=22&length=21"

Works, but only returns 50 items: "https://www.earthcam.com/cams/common/gethofitems.php?camera=timessquare_hd&start=1&length=100"

Notes
`````

*   camera: camera to request images for
*   length: number of images to request, I think
*   start: index of image to start request on

First two bytes (?) of request are not part of JSON string. The
JSON is valid and can be loaded with Python ``json`` library.
The number of items in ``hofdata`` is 21 in the standard request.
(First two bytes can be ignored by using ``json_str[3:]``.)

Need to put quotes around URL to avoid problems with ampersand.

Number of items returned may be capped at 50.

Other Variables
---------------

"Expected luminosity": draw a graph with x-axis of time of day and
y-axis as "expected luminosity," how bright it would be with no
cloud cover. The brightness increasing linearly at some slope
until solar noon, then decreases at the same rate until dusk. The
maximum is set at 1 on the longest day of the year, so shorter
days will achieve a lesser brightness. This captures time of day
and season. The model can maybe use this to adjust the brightness
of the photos for how much sun there is.

