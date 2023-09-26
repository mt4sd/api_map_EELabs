import numpy as np #BORJA

def degree_to_rad(alfa): #BORJA
    return alfa*2*np.pi/360 #BORJA

def equirectangular_to_mercator(longitude,latitude,zoom): #BORJA
    longitude=degree_to_rad(longitude) #BORJA
    latitude=degree_to_rad(latitude) #BORJA

    x=256*2**zoom*(np.pi+longitude)/(2*np.pi) #BORJA
    y=256*2**zoom*(np.pi-np.log(np.tan(np.pi/4+latitude/2)))/(2*np.pi) #BORJA
    return x,y #BORJA

# def degree_decimal_to_degree_hexadecimal(degree_decimal): #Borja
#     degree=np.floor(degree_decimal).astype('int') #Borja
#     minute_decimal=(degree_decimal-degree)*60 #Borja
#     minute=np.floor(minute_decimal).astype('int') #Borja
#     second=np.floor((minute_decimal-minute)*60).astype('int') #Borja
#     return (degree,minute,second) #Borja

# def E_mag(mag,m,n,Em,En): #Borja
#     errors=[En,(mag-n)/m*Em,(m*0.1)/np.log(10)*10**((n-mag)/m)] #Borja
#     return np.round(np.sqrt(sum(np.array(errors)**2)),2) #Borja

def add_zero(a): #BORJA
    a=int(a)
    if a<10: #BORJA
        return ('0'+str(a)) #BORJA
    else: #BORJA
        return str(a) #BORJA

# def display_significant_figures(a): #Borja
#     a=np.round(a,2) #Borja
#     try: #Borja
#         integer,decimal=str(a).split('.') #Borja
#         n=len(decimal) #Borja
#     except: #Borja
#         integer=str(a) #Borja
#         decimal=None #Borja
#         n=0 #Borja
#     if n==0: #Borja
#         a=integer+'.00' #Borja
#     elif n==1:
#         a=integer+'.'+decimal+'0' #Borja
#     else: #Borja
#         a=str(a) #Borja
#     return a #Borja