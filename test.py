__author__ = 'munees'
# Import the Earth Engine Python Package
import ee
from ee import mapclient
from PIL import _imagingtk

# Initialize the Earth Engine object, using the authentication credentials.
ee.Initialize()

# Print the information for an image asset.
image = ee.Image('srtm90_v4')
print(image.getInfo())
image = ee.Image('LANDSAT/LC8_L1T_TOA/LC80440342014077LGN00')

# Define the visualization parameters.

mapclient.addToMap(image)