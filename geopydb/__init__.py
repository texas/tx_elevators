"""
A simple wrapper around geopy that caches to disk.
"""
__version__ = "0.1.0-dev"


import geocoders


if __name__ == "__main__":
    # this is my test suite lol
    g = geocoders.GoogleV3()  # instead of from geopy.geocoders import GoogleV3
    place, (lat, lng) = g.geocode("10900 Euclid Ave in Cleveland")
    print "%s: %.5f, %.5f" % (place, lat, lng)
    # 10900 Euclid Avenue, Cleveland, OH 44106, USA: 41.50726, -81.60701
