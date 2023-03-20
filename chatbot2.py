from flask import Flask,request,jsonify
import requests
from geopy.geocoders import Nominatim
from datetime import date
app= Flask(__name__)
@app.route('/',methods=['POST','GET'])
def index():
    today = date.today()
    print(str(today)[8:10])
    data=request.get_json()
    source_city=data['queryResult']['parameters']['geo-city']
    datee=data['queryResult']['parameters']['date']
    print(datee[8:10])
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(source_city)
    lat=location.latitude
    lon=location.longitude
    if  datee=="" or (int(datee[8:10]) ==int(str(today)[8:10])):  
        url="https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=013b716d17cad1e8064a6a092a8cf06d".format(lat,lon)
        response=requests.get(url)
        response=response.json()
        current_temp=round(float(response['main']['temp']-273.15),2)
        min_temp=round(float(response['main']['temp_min']-273.15),2)
        max_temp=round(float(response['main']['temp_max']-273.15),2)
        weather=response['weather'][0]['main']
        description=response['weather'][0]['description']
        final="Today the weather in {} is mainly {},more specifically {}. Current temprature is approximately {}C with minimum temperature {}C and maximum temperature {}C.".format(source_city,weather,description,current_temp,min_temp,max_temp)
        ft={"fulfillmentText":final}
        return jsonify(ft)        
    elif int(datee[8:10])==int(str(today)[8:10]) + 1 :
        url="https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid=013b716d17cad1e8064a6a092a8cf06d".format(lat,lon)
        response=requests.get(url)
        response=response.json()
        weather=response['list'][7]['weather'][0]['main']
        description=response['list'][7]['weather'][0]['description']
        min_temp=round(float(response['list'][7]['main']['temp_min']-273.15),2)
        max_temp=round(float(response['list'][7]['main']['temp_max']-273.15),2)
        final="Tomorrow's weather in {} is mainly {},more specifically {}. Minimum temperature will be around {}C while maximum temperature being around {}C.".format(source_city,weather,description,min_temp,max_temp)   
        ft={"fulfillmentText":final}
        return jsonify(ft)
    else:
        final="Sorry cant predict".format(source_city,weather,description,min_temp,max_temp)   
        ft={"fulfillmentText":final}
        return jsonify(ft)

if __name__=="__main__":

    app.run()
