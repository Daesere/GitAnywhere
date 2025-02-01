import simplekml
from gee_data import points
kml = simplekml.Kml()
kml.newlinestring(name="Path", coords = points)
kml.save("path.kml")