import geopandas as gp
import mapbox as mb
import pandas as pd
from shapely.geometry import Point

gdb = gp.read_file('C:/Users/Austin/Documents/Coding/Python/Geospatial/OSM/Flood2019/EGS_Flood_Product_Current.gdb')
ottawa = pd.read_pickle('C:/Users/Austin/Documents/Coding/Python/Geospatial/OSM/OttawaAddr.pkl')


geometry = [Point(xy) for xy in zip(ottawa['Longitude'],ottawa['Latitude'])]
ottawa = gp.GeoDataFrame(ottawa,geometry=geometry)
ottawa.crs = {'init' :'epsg:4326'}
ottawa = ottawa.to_crs(gdb.crs)


ottawa_flood = gp.sjoin(ottawa,gdb,how='inner',op='within')
ottawa_flood = ottawa_flood.loc[:,['NodeID','StreetNumber','StreetName','geometry']]
ottawa_flood = ottawa_flood.to_crs({'init' :'epsg:4326'})
ottawa_flood.to_file('ottawa_flood.geojson',driver='GeoJSON',encoding="utf-8")

u = mb.Uploader(access_token=
    'sk')

url = u.stage(open('ottawa_flood.geojson', 'rb'))
job = u.create(url, 'ottawa_flood').json()