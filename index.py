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

import mongo_utils as mdbu #BORJA

import numpy as np #BORJA
from VIIRS_map_utils import add_zero #Borja

from PIL import Image #Borja
from patchify import patchify #Borja
import os #Borja


devices_v1_0_bp = Blueprint('devices_v1_0_bp', __name__)

CORS(devices_v1_0_bp)

api = Api(devices_v1_0_bp)

@api.resource('/api/img_map') #BORJA
class UploadImage(Resource): #BORJA
   def get(self): #BORJA
     parser = reqparse.RequestParser() #BORJA
     parser.add_argument('zoom', default=None, type=str,location='args') #BORJA
     parser.add_argument('v', default=None, type=str,location='args') #BORJA
     parser.add_argument('h', default=None, type=str,location='args') #BORJA
     args = parser.parse_args() #BORJA

     filename='h'+str(add_zero(args['h']))+'v'+str(add_zero(args['v']))+'.png' #BORJA
     zoom=str(args['zoom']) #BORJA
     tile=str(np.floor(int(args['h'])/(2**int(zoom)/16)).astype('int'))+'_'+str(np.floor(int(args['v'])/(2**int(zoom)/16)).astype('int')) #BORJA

     images_directory =r'C:\Users\borja\Downloads\V3\map\tiles' #BORJA

     try:
        purple_tiles=mdbu.get_map_purple_tiles(int(args['h']),int(args['v']),int(args['zoom']))[0] #BORJA
     except:
        purple_tiles=None #BORJA

     if purple_tiles: #BORJA
         #purple_tile='purple_exp.jpg' #BORJA
         purple_tile='purple.png' #BORJA
         image_path = f'{images_directory}\{purple_tile}' #BORJA
     else: #BORJA
        if int(zoom)>4: #BORJA
            image_path = f'{images_directory}\{tile}\{zoom}\{filename}' #BORJA
            if int(zoom)>9: #BORJA
                try: #BORJA
                    Image.open(image_path) #BORJA
                except: #BORJA
                    coefficient_scale=2**(int(zoom)-9) #BORJA
                    int_h=np.floor(int(args['h'])/(coefficient_scale)).astype('int') #BORJA
                    pos_h=int(int(args['h'])-int_h*(coefficient_scale)) #BORJA
                    int_v=np.floor(int(args['v'])/(coefficient_scale)).astype('int') #BORJA
                    pos_v=int(int(args['v'])-int_v*(coefficient_scale)) #BORJA

                    image=Image.open(images_directory+'\\'+tile+'\\9'+'\\'+'h'+str(add_zero(int_h))+'v'+str(add_zero(int_v))+'.png') #BORJA
                    patches = patchify(np.array(image), (256/coefficient_scale,256/coefficient_scale,4), step=int(256/coefficient_scale)) #BORJA
                    sub_image=Image.fromarray(patches[pos_v,pos_h,:,:][0]) #BORJA
                    sub_image = sub_image.resize((256,256), Image.NEAREST) #BORJA

                    try: #BORJA
                        os.mkdir(f'{images_directory}\{tile}\{zoom}') #BORJA
                    except: #BORJA
                        pass #BORJA
                    
                    sub_image.save(image_path) #BORJA
        else: #BORJA
            image_path = f'{images_directory}\{zoom}\{filename}' #BORJA    
     return send_file(image_path, mimetype='image/jpeg')  #BORJA
   
@api.resource('/api/values_map') #BORJA
class Values_map(Resource): #BORJA
   def get(self): #BORJA
     parser = reqparse.RequestParser() #BORJA
     parser.add_argument('latitude_degree', default=None, type=int,location='args') #BORJA
     parser.add_argument('latitude_minutes', default=None, type=int,location='args') #BORJA
     parser.add_argument('latitude_seconds', default=None, type=int,location='args') #BORJA
     parser.add_argument('longitude_degree', default=None, type=int,location='args') #BORJA
     parser.add_argument('longitude_minutes', default=None, type=int,location='args') #BORJA
     parser.add_argument('longitude_seconds', default=None, type=int,location='args') #BORJA
     args = parser.parse_args() #BORJA

     mag=mdbu.get_map_values(args['latitude_degree'],args['latitude_minutes'],args['latitude_seconds'],args['longitude_degree'],args['longitude_minutes'],args['longitude_seconds'])[0]['mag']

     return mag #BORJA

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
