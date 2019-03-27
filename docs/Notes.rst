Notes
=====

Todo
----


Done
----
*   Write code to process images: convert to greyscale, reduce
    size/dimensionality
*   Prepare image data: get into a 3D numpy array
*   Collect times of images. For each, find the nearest
    observation and record the Raining/Not binary variable.
    This variable could be added to the 'images.csv' file.
*   Figure out API to get historical weather data
*   Write script to get weather data correpsonding to time of images;
    we only need a binary variable 'raining' vs. 'not raining' I think
*   Is there a weather station near Times Square?
    Should I pick a different camera location?
    Central Park station and Midtown camera are good.
*   Write curl script to save URLs of images to a file
*   Write python script to extract URLs and collect
*   Write wget/curl script to download images

Specific References
-------------------

`Downsampling <https://ai.stackexchange.com/questions/3938/how-to-handle-images-of-large-sizes-in-cnn>`__

`Stride <https://www.quora.com/How-does-one-determine-stride-size-in-CNN-filters>`__

`Loss function <https://stackoverflow.com/questions/47034888/how-to-choose-cross-entropy-loss-in-tensorflow>`__

References
----------

*   `Image classification
    <http://www.coldvision.io/2016/07/29/image-classification-deep-learning-cnn-caffe-opencv-3-x-cuda/>`__
*   `TensorFlow Keras documentation <https://www.tensorflow.org/guide/keras>`__
*   `TensorFlow docs for CNN <https://www.tensorflow.org/tutorials/estimators/cnn>`__
*   `Pillow docs <https://pillow.readthedocs.io/en/stable/>`__

NWS API and Data
----------------

LCD Hourly Weather Type
```````````````````````

From documentation:

    **Weather Type (AU|AW|MW):** Weather types describe precipitation or
    obstructions to vision occurring at the time of observation. These
    are reported by automated sensors (AU or AW) and manually (MW) by
    human observation. AU elements are listed first and followed by
    “|” and followed by AW elements. After the AW elements there will
    be another “|” followed by the MW elements (e.g.
    “-RA:02|RA:61|RA:61”). In the preceding example -RA:02 is an AU
    element, RA:61 is an AW element and RA:61 is an MW element. Note
    that precipitation types often use “-“ for light intensity or “+”
    for heavy intensity. If a precipitation type has no “-“ or “+” it
    is considered to be moderate intensity. It is not uncommon for one
    type of element to be reported without another. In other words, it
    is possible to have an AU element without an AW element or MW
    element. Definitions of contractions used are listed in the
    Present Weather Appendix at the end of this document.

Record schema: [AU]|[AW]|[MW]

Observation schema: RA:[code]

Codes for rain:

-   AU

    *   DZ:01 - Drizzle
    *   RA:02 - Rain

-   AW

    *   21 - Precipitation (during preceding hour but not at time of
        observation)
    *   22 - Drizzle (not freezing) or snow grains (during preceding hour
        but not at time of observation)
    *   23 - Rain (not freezing) (during preceding hour but not at time of
        observation)
    *   25 - Freezing drizzle or freezing rain (during preceding hour but
        not at time of observation)
    *   40 - Precipitation
    *   41 - Precipitation, slight or moderate
    *   42 - Precipitation, heavy
    *   43 - Liquid precipitation, slight or moderate
    *   44 - Liquid precipitation, heavy
    *   45 - Solid precipitation, slight or moderate
    *   46 - Solid precipitation, heavy
    *   47 - Freezing precipitation, slight or moderate
    *   48 - Freezing precipitation, heavy
    *   DZ:50 - Drizzle
    *   DZ:51 - Drizzle, not freezing, slight
    *   DZ:52 - Drizzle, not freezing, moderate
    *   DZ:53 - Drizzle, not freezing, heavy
    *   FZDZ:54 - Drizzle, freezing, slight
    *   FZDZ:55 - Drizzle, freezing, moderate
    *   FZDZ:56 - Drizzle, freezing, heavy
    *   DZ:57 - Drizzle and rain, slight
    *   DZ:58 - Drizzle and rain, moderate or heavy
    *   RA:60 - Rain
    *   RA:61 - Rain, not freezing, slight
    *   RA:62 - Rain, not freezing, moderate
    *   RA:63 - Rain, not freezing, heavy
    *   FZRA:64 - Rain, freezing, slight
    *   FZRA:65 - Rain, freezing, moderate
    *   FZRA:66 - Rain, freezing, heavy
    *   RA:67 - Rain or drizzle and snow, slight
    *   RA:68 - Rain or drizzle and snow, moderate or heavy
    *   SHRA:81 - Rain showers or intermittent rain, slight
    *   SHRA:82 - Rain showers or intermittent rain, moderate
    *   SHRA:83 - Rain showers or intermittent rain, heavy
    *   SHRA:84 - Rain showers or intermittent rain, violent
    *   SHSN:85 - Snow showers or intermittent snow, slight
    *   SHSN:86 - Snow showers or intermittent snow, moderate
    *   SHSN:87 - Snow showers or intermittent snow, heavy
    *   TS:92 - Thunderstorm, slight or moderate, with rain showers and/or
        snow showers
    *   TS:95 - Thunderstorm, heavy, with rain showers and/or snow
    
-   MW

    *   25 - Shower(s) of rain (during the preceding hour but not at the
        time of observation)
    *   DZ:50 - Drizzle, not freezing, intermittent, slight at time of
        observation
    *   DZ:51 - Drizzle, not freezing, continuous, slight at time of
        observation
    *   DZ:52 - Drizzle, not freezing, intermittent, moderate at time of
        observation
    *   DZ:53 - Drizzle, not freezing, continuous, moderate at time of
        observation
    *   DZ:54 - Drizzle, not freezing, intermittent, heavy (dense) at time
        of observation
    *   DZ:55 - Drizzle, not freezing, continuous, heavy (dense) at time
        of observation
    *   FZDZ:56 - Drizzle, freezing, slight
    *   FZDZ:57 - Drizzle, freezing, moderate or heavy (dense)
    *   DZ:58 - Drizzle and rain, slight
    *   DZ:59 - Drizzle and rain, moderate or heavy
    *   RA:60 - Rain, not freezing, intermittent, slight at time of
        observation
    *   RA:61 - Rain, not freezing, continuous, slight at time of
        observation
    *   RA:62 - Rain, not freezing, intermittent, moderate at time of
        observation
    *   RA:63 - Rain, not freezing, continuous, moderate at time of
        observation
    *   RA:64 - Rain, not freezing, intermittent, heavy at time of
        observation
    *   RA:65 - Rain, not freezing, continuous, heavy at time of
        observation
    *   FZRA:66 - Rain, freezing, slight
    *   FZRA:67 - Rain, freezing, moderate or heavy
    *   RA:68 - Rain or drizzle and snow, slight
    *   RA:69 - Rain or drizzle and snow, moderate or heavy
    *   SHRA:80 - Rain shower(s), slight
    *   SHRA:81 - Rain shower(s), moderate or heavy
    *   SHRA:82 - Rain shower(s), violent
    *   RA:91 - Slight rain at time of observation, thunderstorm during
        the preceding hour but not at time of observation
    *   RA:92 - Moderate or heavy rain at time of observation,
        thunderstorm during the preceding hour but not at time of
        observation

Glossary:

*   +: high intensity, rather than moderate
*   -: low intensity, rather than moderate
*   AU: report by automatic sensor
*   AW: report by automatic sensor
*   MW: report by human observation






Historical Data
```````````````

Promising:

*   `Environmental Web Services
    <https://www.ncdc.noaa.gov/cdo-web/webservices/ncdcwebservices>`__:
    requires token [vbuLRFzLHqYPeHGCfCMgSLuuNoUodnhw].
    This data is provided by the National Center for Environmental
    Information (formerly the National Climatic Data Center, NCDC).
    This is part of the NOAA.
    The 15-minute and hourly percipitation reports are only
    available through 2014, it seem.
*   `Local Climatological Data
    <https://www.ncdc.noaa.gov/cdo-web/datasets/LCD/stations/WBAN:94728/detail>`__
    The LCD data is provided in PDF or CSV.
*   `National Weather Service Forecast Office observations
    <https://w2.weather.gov/climate/index.php?wfo=okx>`__.
    This provides current observations, but not past observations
    in hourly detail.
    

The NWS is part of the NOAA. They have an `API portal
<https://graphical.weather.gov/xml/>`__ for **forecast** data.

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
Here is a `map of radio stations
<http://www.nws.noaa.gov/nwr/Maps/>`__.

`KNYC <https://w1.weather.gov/obhistory/KNYC.html>`__ is located
in Central Park. Here is the station's `metadata
<https://www.ncdc.noaa.gov/homr/#ncdcstnid=20019453&tab=MSHR>`__.

*   COOP ID: 305801
*   ICAO ID: KNYC
*   WBAN ID: 94728
*   FAA ID: NYC
*   NCDC ID: 20019453

Here is a `tool for finding observation stations
<https://www.ncdc.noaa.gov/cdo-web/datatools/findstation>`__.


Station to Use
``````````````

KNYC is at (40.783, -73.967) or (40.77898°, -73.96925°), per
another source.
It is at `Belvedere Castle
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

