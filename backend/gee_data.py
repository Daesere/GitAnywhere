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
start_c = (48.2, 10)
end_c = (48.25, 10.05)
bodyweight = 65
height = 1.70

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
    # Define the area of interest
    aoi = ee.Geometry.Rectangle([start_c, end_c])

    # Get elevation and landcover datasets
    elevation = ee.Image('USGS/SRTMGL1_003')
    landcover = ee.Image("ESA/WorldCover/v100/2020")

    # Sample elevation and landcover data
    elev_samples = elevation.sample(region=aoi, scale=scale, geometries=True)
    land_samples = landcover.sample(region=aoi, scale=scale, geometries=False)

    # Get the sampled data
    elev_list = elev_samples.getInfo()['features']
    land_list = land_samples.getInfo()['features']

    # Combine elevation and landcover data for each point
    coordinate_feature_pairs = []
    for elev_feature, land_feature in zip(elev_list, land_list):
        coords = elev_feature['geometry']['coordinates']
        elevation_value = elev_feature['properties']['elevation']
        terrain_type = land_feature['properties']['Map']
        coordinate_feature_pairs.append((coords, [elevation_value, terrain_type]))

    print('Sample points obtained')
    return coordinate_feature_pairs

def create_path(start_c, end_c, scale, bodyweight=70, height=1.70):

    points_c = get_points(start_c, end_c, scale)
    points_m = []
    for point in points_c:
        points_m.append([coords_to_m(start_c, point[0]), point[1]])
    
    
    path, cost = find_path.find_path(points_m, scale, bodyweight, height)

    return path, cost

def path_to_coords(path, scale, start_m, end_m, start_c, end_c):
    path = np.array(path)
    angle = math.tan((end_m[0] - start_m[0])/(end_m[1] - start_m[1])) - math.pi/2
    rotation_matrix = np.array([[math.cos(angle), math.sin(angle)], [-math.sin(angle), math.cos(angle)]])
    rotated_points = np.dot(path, rotation_matrix)
    coord_path = []
    for point in rotated_points:
        coord_path.append(m_to_coords(point * scale, start_c, end_c)[::-1])
    
    return coord_path

def smooth_points(points):
    for i in range(len(points) - 1):
        points[i] = [(points[i][0] + points[i + 1][0])/2, (points[i][1] + points[i + 1][1])/2]

def create_map(start_c, end_c, bodyweight=70, height=1.70):
    try:
        start_c = (float(start_c[0]), float(start_c[1]))
        end_c = (float(end_c[0]), float(end_c[1]))
        bodyweight = float(bodyweight)
        height = float(height)
    except:
        raise(TypeError)
    start_m, end_m = (0,0), coords_to_m(start_c, end_c)
    scale = get_scale(start_m, end_m)

    path, cost = create_path(start_c, end_c, scale, bodyweight, height)
    coord_path = path_to_coords(path, scale, start_m, end_m, start_c, end_c)
    smooth_points(coord_path)
    route = ee.Geometry.LineString(coord_path)

    route_map = geemap(center=[(start_c[0] + end_c[0])/2, (start_c[1] + end_c[1])/2], zoom=14)

    route_map.addLayer(route, {"color": "blue"}, "Route")

    if not os.path.exists('/frontend/public'):
        os.makedirs('/frontend/public')

    output_file = os.path.join('/frontend/public', 'route_map.html')
    route_map.save(outfile=output_file)

    print(f'route map save to {output_file}')
    return coord_path, cost

create_map(start_c, end_c)
