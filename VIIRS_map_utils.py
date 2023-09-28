import numpy as np 

def degree_to_rad(alfa): 
    return alfa*2*np.pi/360 

def equirectangular_to_mercator(longitude,latitude,zoom): 
    longitude=degree_to_rad(longitude) 
    latitude=degree_to_rad(latitude) 

    x=256*2**zoom*(np.pi+longitude)/(2*np.pi) 
    y=256*2**zoom*(np.pi-np.log(np.tan(np.pi/4+latitude/2)))/(2*np.pi) 
    return x,y 

# def degree_decimal_to_degree_hexadecimal(degree_decimal): 
#     degree=np.floor(degree_decimal).astype('int') 
#     minute_decimal=(degree_decimal-degree)*60 
#     minute=np.floor(minute_decimal).astype('int') 
#     second=np.floor((minute_decimal-minute)*60).astype('int') 
#     return (degree,minute,second) 

# def E_mag(mag,m,n,Em,En): 
#     errors=[En,(mag-n)/m*Em,(m*0.1)/np.log(10)*10**((n-mag)/m)] 
#     return np.round(np.sqrt(sum(np.array(errors)**2)),2) 

def add_zero(a): 
    a=int(a)
    if a<10: 
        return ('0'+str(a)) 
    else: 
        return str(a) 

# def display_significant_figures(a): 
#     a=np.round(a,2) 
#     try: 
#         integer,decimal=str(a).split('.') 
#         n=len(decimal) 
#     except: 
#         integer=str(a) 
#         decimal=None 
#         n=0 
#     if n==0: 
#         a=integer+'.00' 
#     elif n==1:
#         a=integer+'.'+decimal+'0' 
#     else: 
#         a=str(a) 
#     return a 
