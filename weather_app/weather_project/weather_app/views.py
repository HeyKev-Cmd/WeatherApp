from django.shortcuts import render
import requests
import datetime
import os
import logging
# endpoints
# Create your views here.
from weather_project.settings import BASE_DIR
def index(request):
    path=os.path.join(BASE_DIR, 'weather_app\API_KEY.txt')
    API_KEY=open(path,"r").read()
    current_weather_url="https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url="https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"
    # "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"
    # "
    
    if request.method=="POST":
        city1=request.POST['city1']
        # optional
        city2=request.POST.get('city2',None)
        weather_data1,daily_forecast1=fetch_weather_and_forcast(city1,API_KEY,current_weather_url,forecast_url)
        if city2:
            weather_data2,daily_forecast2=fetch_weather_and_forcast(city2,API_KEY,current_weather_url,forecast_url)
        else:
            weather_data2,daily_forecast2=None,None
        context={
            "weather_data1":weather_data1,
            "daily_forecast1":daily_forecast1,
            "weather_data2":weather_data2,
            "daily_forecast2":daily_forecast2
        }
        return render(request,"weather_app/index.html",context)
    else:
        return render(request,"weather_app/index.html")
    
def  fetch_weather_and_forcast(city,api_key,current_weather_url,forecast_url):
    logger = logging.getLogger(__name__)
    response=requests.get(current_weather_url.format(city,api_key)).json()
    lat,lon=response['coord']['lat'],response['coord']['lon']
    forcast_response=requests.get(forecast_url.format(lat,lon,api_key)).json()
    weather_data={
        "city":city,
        "temperature":round(response['main']['temp']-273.15,2),
        "description":response['weather'][0]['description'],
        "icon":response['weather'][0]['icon']
    }
    # logger.warning('city={} temperature={} description={} icon={}'.format(city,round(response['main']['temp']-273.15,2),response['weather'][0]['description'],response['weather'][0]['icon']))
    daily_forecasts=[]
    for x in forcast_response['daily'][:5]:
        daily_forecasts.append(
            {
                "day":datetime.datetime.fromtimestamp(x['dt']).strftime("%A"),
                "min_temp":round(x['temp']['min']-273.15/2),
                "max_temp":round(x['temp']['max']-273.15/2),
                "description":x['weather'][0]['description'],
                "icon":x['weather'][0]['icon']
            }
        )
        # logger.warning('day={} min={} max={} descirption={} icon={}'.format(datetime.datetime.fromtimestamp(x['dt']).strftime("%A"),round(x['temp']['min']-273.15/2),round(x['temp']['max']-273.15/2),x['weather'][0]['description'],x['weather'][0]['icon']))
    return  weather_data,daily_forecasts