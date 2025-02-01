import ee
from geemap import Map as geemap
import math
import numpy as np
import os

ee.Authenticate()
print('Authenticated')
ee.Initialize(project='gm-git-any')
print('Initialized')

start_c = (float(input('lat start: ')), float(input('lon start: ')))
end_c = (float(input('lat end: ')), float(input('lon end: ')))

# Get elevation
elevation = ee.Image('USGS/SRTMGL1_003')

# Convert to meters (zeroed)
def coords_to_m(start_c, end_c):
    R = 6378137

    lat_m = math.sin((end_c[0] - start_c[0]) * math.pi/180) * R
    lon_m = math.sin((end_c[1] - start_c[1]) * math.pi/180) * math.cos((end_c[0] - start_c[0]) * math.pi/180) * R

    return (0,0), (lat_m, lon_m)

# Convert to coords from zeroed meter values
def m_to_coords(point_m, start_c, end_c):
    R = 6378137
    
    lat_c = math.asin(point_m[1] / R) * 180/math.pi + start_c[0]
    lon_c = math.asin(point_m[0] / (math.cos(end_c[0] - start_c[0]) * R)) * 180/math.pi + start_c[1]

    return lat_c, lon_c

# Area of interst
def set_scaled_rect(start_m, end_m):
    point_distance = math.sqrt((end_m[0] - start_m[0])**2 + (end_m[1] - start_m[1])**2)

    sqrt_4 = math.sqrt(4)
    
    base_rect = np.array([(-1,1), (1,1), (1,-1), (-1,-1)])
    scaled_rect = base_rect * point_distance/sqrt_4

    return scaled_rect

def set_final_rect(start_m, end_m):
    path_angle = math.tan((end_m[0] - start_m[0])/(end_m[1] - start_m[1]))
    rotation_matrix = np.array([[math.cos(path_angle), math.sin(path_angle)],[-math.sin(path_angle), math.cos(path_angle)]])
    
    scaled_rect = set_scaled_rect(start_m, end_m)
    rotated_rect = np.dot(scaled_rect, rotation_matrix)
    final_rect = rotated_rect + start_m

    return final_rect
    
def get_scale(start_m, end_m):
    rect_m = set_scaled_rect(start_m, end_m)
    base = abs(int(rect_m[0][0] - rect_m[1][0]))
    print(base,'base')
    for dis in range(1, base):
        if int(base/dis + 1) * int(base/dis + 1) < 5000:
            if dis > 30:
                print(dis, 'scale')
                return dis
    return 30

def get_points(start_c, end_c):
    # Set inital scale
    start_m, end_m = coords_to_m(start_c, end_c)
    scale = get_scale(start_m, end_m)

    final_rect_m = set_final_rect(start_m, end_m)
    final_rect_c = []
    for coord in final_rect_m:
        final_rect_c.append(m_to_coords(coord, start_c, end_c)[0])

    print(final_rect_c)
    aoi = ee.Geometry.Rectangle(final_rect_c)

    point_samples = elevation.sample(region=aoi, scale=scale, geometries=True)

    samples_list = point_samples.getInfo()['features']
    coordinate_elevation_pairs = [(point['geometry']['coordinates'], point['properties']['elevation']) for point in samples_list]
    print('sample points obtained')

    return coordinate_elevation_pairs

points = get_points(start_c, end_c)

def create_map(points):
    test_route = ee.Geometry.LineString([start_c, end_c])

    route_map = geemap(centger=[(start_c[0] + end_c[0])/2, (start_c[1] + end_c[1])/2], zoom=14)

    route_map.addLayer(test_route, {"color": "blue"}, "Route")

    if not os.path.exists('maps'):
        os.makedirs('maps')

    output_file = os.path.join('maps', 'route_map.html')
    route_map.save(outfile=output_file)

    print(f'route map save to {output_file}')

create_map(points)