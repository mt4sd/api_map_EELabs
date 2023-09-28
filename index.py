import logging
import os

from dash import html
from dotenv import load_dotenv

from flask import Flask
import dash


load_dotenv()


from flask import Blueprint, send_file
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse

import mongo_utils as mdbu

import numpy as np 
from VIIRS_map_utils import add_zero 

from PIL import Image 
from patchify import patchify 
import os 


devices_v1_0_bp = Blueprint('devices_v1_0_bp', __name__)

CORS(devices_v1_0_bp)

api = Api(devices_v1_0_bp)

@api.resource('/eelabs/api/v1/img_map') 
class UploadImage(Resource): 
   def get(self): 
     parser = reqparse.RequestParser() 
     parser.add_argument('zoom', default=None, type=str,location='args') 
     parser.add_argument('v', default=None, type=str,location='args') 
     parser.add_argument('h', default=None, type=str,location='args') 
     args = parser.parse_args() 

     filename='h'+str(add_zero(args['h']))+'v'+str(add_zero(args['v']))+'.png' 
     zoom=str(args['zoom']) 
     tile=str(np.floor(int(args['h'])/(2**int(zoom)/16)).astype('int'))+'_'+str(np.floor(int(args['v'])/(2**int(zoom)/16)).astype('int')) 

     images_directory =r'/home/eelabs/map/tiles' 

     try:
        purple_tiles=mdbu.get_map_purple_tiles(int(args['h']),int(args['v']),int(args['zoom']))[0] 
     except:
        purple_tiles=None 

     if purple_tiles: 
         purple_tile='purple.png' 
         image_path = f'{images_directory}/{purple_tile}' 
     else: 
        if int(zoom)>4: 
            image_path = f'{images_directory}/{tile}/{zoom}/{filename}' 
            if int(zoom)>9: 
                try: 
                    Image.open(image_path) 
                except: 
                    coefficient_scale=2**(int(zoom)-9) 
                    int_h=np.floor(int(args['h'])/(coefficient_scale)).astype('int') 
                    pos_h=int(int(args['h'])-int_h*(coefficient_scale)) 
                    int_v=np.floor(int(args['v'])/(coefficient_scale)).astype('int') 
                    pos_v=int(int(args['v'])-int_v*(coefficient_scale)) 

                    image=Image.open(images_directory+'/'+tile+'/9'+'/'+'h'+str(add_zero(int_h))+'v'+str(add_zero(int_v))+'.png') 
                    patches = patchify(np.array(image), (256/coefficient_scale,256/coefficient_scale,4), step=int(256/coefficient_scale)) 
                    sub_image=Image.fromarray(patches[pos_v,pos_h,:,:][0]) 
                    sub_image = sub_image.resize((256,256), Image.NEAREST) 

                    try: 
                        os.mkdir(f'{images_directory}/{tile}/{zoom}') 
                    except: 
                        pass 
                    
                    sub_image.save(image_path) 
        else: 
            image_path = f'{images_directory}/{zoom}/{filename}' 
     return send_file(image_path, mimetype='image/jpeg')  
   
@api.resource('/eelabs/api/v1/values_map') 
class Values_map(Resource): 
   def get(self): 
     parser = reqparse.RequestParser() 
     parser.add_argument('latitude_degree', default=None, type=int,location='args') 
     parser.add_argument('latitude_minutes', default=None, type=int,location='args') 
     parser.add_argument('latitude_seconds', default=None, type=int,location='args') 
     parser.add_argument('longitude_degree', default=None, type=int,location='args') 
     parser.add_argument('longitude_minutes', default=None, type=int,location='args') 
     parser.add_argument('longitude_seconds', default=None, type=int,location='args') 
     args = parser.parse_args() 

     mag=mdbu.get_map_values(args['latitude_degree'],args['latitude_minutes'],args['latitude_seconds'],args['longitude_degree'],args['longitude_minutes'],args['longitude_seconds'])[0]['mag']

     return mag 

server = Flask(__name__, static_folder='static')
server.register_blueprint(devices_v1_0_bp)
app = dash.Dash(__name__, server=server)


app.layout = html.Div()


if __name__ == '__main__':
    if os.getenv("DEBUG") == 'True':
        logging.basicConfig(
            format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
            level=logging.INFO)

    app.run_server(debug=os.getenv("DEBUG") == 'True', port=os.getenv("PORT"), host='0.0.0.0')
    #app.run_server()
    # from waitress import serve
    # serve(app.server,host='0.0.0.0',port=os.getenv("PORT"))
