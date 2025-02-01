import ee
from geemap import Map as geemap
import math
import numpy as np
import os
import find_path

ee.Authenticate()
print('Authenticated')
ee.Initialize(project='gm-git-any')
print('Initialized')

# start_c = (float(input('lat start: ')), float(input('lon start: ')))
# end_c = (float(input('lat end: ')), float(input('lon end: ')))
# bodyweight = float(input('wight in kg: '))
# height = float(input('height in m: '))
start_c = (46.2, 8)
end_c = (46.25, 8.05)
bodyweight = 65
height = 1.70


# Get elevation
elevation = ee.Image('USGS/SRTMGL1_003')

# Convert to meters (zeroed)
def coords_to_m(start_c, end_c):
    R = 6378137

    lat_m = math.sin((end_c[0] - start_c[0]) * math.pi/180) * R
    lon_m = math.sin((end_c[1] - start_c[1]) * math.pi/180) * math.cos((end_c[0] - start_c[0]) * math.pi/180) * R

    return (lat_m, lon_m)

# Convert to coords from zeroed meter values
def m_to_coords(point_m, start_c, end_c):
    R = 6378137
    
    lat_c = math.asin(point_m[1] / R) * 180/math.pi + start_c[0]
    lon_c = math.asin(point_m[0] / (math.cos(end_c[0] - start_c[0]) * R)) * 180/math.pi + start_c[1]

    return (lat_c, lon_c)

# Area of intrest
    
def get_scale(start_m, end_m):
    distance = math.sqrt((end_m[0] - start_m[0]) ** 2 + (end_m[1] - start_m[1]) ** 2)
    base = int(distance / math.sqrt(2))

    for dis in range(1, base):
        if int(base/dis + 1) * int(base/dis + 1) < 5000:
            if dis > 30:
                print(dis, 'scale')
                return dis
    return 30

def get_points(start_c, end_c, scale):

    aoi = ee.Geometry.Rectangle([start_c, end_c])
    point_samples = elevation.sample(region=aoi, scale=scale, geometries=True)

    samples_list = point_samples.getInfo()['features']
    coordinate_elevation_pairs = [(point['geometry']['coordinates'], [point['properties']['elevation']]) for point in samples_list]
    print('sample points obtained')
    return coordinate_elevation_pairs

def create_path(start_c, end_c, scale, bodyweight=70, height=1.70):

    points_c = get_points(start_c, end_c, scale)
    points_m = []
    for point in points_c:
        points_m.append([coords_to_m(start_c, point[0]), point[1]])
    
    
    path, cost = find_path.find_path(points_m, scale, bodyweight, height)

    return path, cost

def path_to_coords(path, scale, start_m, end_m):
    path = np.array(path)
    angle = math.tan((end_m[0] - start_m[0])/(end_m[1] - start_m[1])) - math.pi/2
    rotation_matrix = np.array([[math.cos(angle), math.sin(angle)], [-math.sin(angle), math.cos(angle)]])
    rotated_points = np.dot(path, rotation_matrix)
    coord_path = []
    for point in rotated_points:
        coord_path.append(m_to_coords(point * scale, start_c, end_c)[::-1])
    
    return coord_path

def create_map(start_c, end_c, bodyweight=70, height=1.70):
    start_m, end_m = (0,0), coords_to_m(start_c, end_c)
    scale = get_scale(start_m, end_m)

    path, cost = create_path(start_c, end_c, scale, bodyweight, height)
    print(path)
    coord_path = path_to_coords(path, scale, start_m, end_m)
    print(coord_path)
    route = ee.Geometry.LineString(coord_path)

    route_map = geemap(center=[(start_c[0] + end_c[0])/2, (start_c[1] + end_c[1])/2], zoom=14)

    route_map.addLayer(route, {"color": "blue"}, "Route")

    if not os.path.exists('maps'):
        os.makedirs('maps')

    output_file = os.path.join('maps', 'route_map.html')
    route_map.save(outfile=output_file)

    print(f'route map save to {output_file}')

create_map(start_c, end_c)
