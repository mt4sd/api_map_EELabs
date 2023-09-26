import os

import pymongo
import pytz
from bson import CodecOptions

import numpy as np #BORJA
from VIIRS_map_utils import equirectangular_to_mercator  #BORJA



def _get_client():
    if os.getenv("MONGO_HOST") == "localhost":
        __conn_string = "mongodb://{}:{}/".format(os.getenv("MONGO_HOST"), os.getenv("MONGO_PORT"))
    else:
        __conn_string = "mongodb+srv://{}:{}@{}/".format(os.getenv("MONGO_CON_USER"),
                                                         os.getenv("MONGO_CON_PASS"),
                                                         os.getenv("MONGO_HOST"))
    return pymongo.MongoClient(__conn_string)



def _get_db_map_values(): #Borja
    __mongo_db ='map_values' #Borja
    __mongo_client = _get_client() #Borja
    return __mongo_client[__mongo_db] #Borja

def _get_db_map_purple_tiles(): #Borja
    __mongo_db ='map_purple_tiles' #Borja
    __mongo_client = _get_client() #Borja
    return __mongo_client[__mongo_db] #Borja


def _get_map_values(tile): #Borja
    collection=str(int(tile[0]))+'_'+str(int(tile[1])) #Borja
    return _get_db_map_values()[collection].with_options( #Borja
        codec_options=CodecOptions( #Borja
            tz_aware=True, #Borja
            tzinfo=pytz.timezone('UTC') #Borja
        ) #Borja
    ) #Borja

def _get_map_purple_tiles(tile): #Borja
    collection=str(int(tile[0]))+'_'+str(int(tile[1])) #Borja
    return _get_db_map_purple_tiles()[collection].with_options( #Borja
        codec_options=CodecOptions( #Borja
            tz_aware=True, #Borja
            tzinfo=pytz.timezone('UTC') #Borja
        ) #Borja
    ) #Borja

def get_map_values(grad_lat,min_lat,sec_lat,grad_lon,min_lon,sec_lon): #BORJA
    tile=np.floor(np.array(equirectangular_to_mercator(grad_lon+min_lon/60+sec_lon/60/60,grad_lat+min_lat/60+sec_lat/60/60,4))/256) #BORJA
    query = {"grad_lat":int(grad_lat),"min_lat":int(min_lat),"sec_lat":int(sec_lat),"grad_lon":int(grad_lon),"min_lon":int(min_lon),"sec_lon":int(sec_lon)} #BORJA
    map_value = _get_map_values(tile).find(query, {"mag": 1}) #BORJA
    return list(map_value) #BORJA

def get_map_purple_tiles(h,v,zoom): #BORJA
    tile=[np.floor(h/(2**zoom/16)).astype('int'),np.floor(v/(2**zoom/16)).astype('int')] #BORJA
    query = {"zoom":zoom,"h":h,"v":v} #BORJA
    purple_tiles = _get_map_purple_tiles(tile).find(query, {"_id": 0}) #BORJA
    return list(purple_tiles) #BORJA
