import os

import pymongo
import pytz
from bson import CodecOptions

import numpy as np 
from VIIRS_map_utils import equirectangular_to_mercator  



def _get_client():
    if os.getenv("MONGO_HOST") == "localhost":
        __conn_string = "mongodb://{}:{}/".format(os.getenv("MONGO_HOST"), os.getenv("MONGO_PORT"))
    else:
        __conn_string = "mongodb+srv://{}:{}@{}/".format(os.getenv("MONGO_CON_USER"),
                                                         os.getenv("MONGO_CON_PASS"),
                                                         os.getenv("MONGO_HOST"))
    return pymongo.MongoClient(__conn_string)



def _get_db_map_values(): 
    __mongo_db ='map_values' 
    __mongo_client = _get_client() 
    return __mongo_client[__mongo_db] 

def _get_db_map_purple_tiles(): 
    __mongo_db ='map_purple_tiles' 
    __mongo_client = _get_client() 
    return __mongo_client[__mongo_db] 


def _get_map_values(tile): 
    collection='t' + str(int(tile[0]))+'_'+str(int(tile[1])) 
    return _get_db_map_values()[collection].with_options( 
        codec_options=CodecOptions( 
            tz_aware=True, 
            tzinfo=pytz.timezone('UTC') 
        ) 
    ) 

def _get_map_purple_tiles(tile): 
    collection='t' + str(int(tile[0]))+'_'+str(int(tile[1])) 
    return _get_db_map_purple_tiles()[collection].with_options( 
        codec_options=CodecOptions( 
            tz_aware=True, 
            tzinfo=pytz.timezone('UTC') 
        ) 
    ) 

def get_map_values(grad_lat,min_lat,sec_lat,grad_lon,min_lon,sec_lon): 
    tile=np.floor(np.array(equirectangular_to_mercator(grad_lon+min_lon/60+sec_lon/60/60,grad_lat+min_lat/60+sec_lat/60/60,4))/256) 
    query = {"grad_lat":int(grad_lat),"min_lat":int(min_lat),"sec_lat":int(sec_lat),"grad_lon":int(grad_lon),"min_lon":int(min_lon),"sec_lon":int(sec_lon)} 
    map_value = _get_map_values(tile).find(query, {"mag": 1}) 
    return list(map_value) 

def get_map_purple_tiles(h,v,zoom): 
    tile=[np.floor(h/(2**zoom/16)).astype('int'),np.floor(v/(2**zoom/16)).astype('int')] 
    query = {"zoom":zoom,"h":h,"v":v} 
    purple_tiles = _get_map_purple_tiles(tile).find(query, {"_id": 0}) 
    return list(purple_tiles) 
