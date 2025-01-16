from django.shortcuts import render, redirect
from django.http import JsonResponse

from datetime import datetime
import requests
import time


def home_view(request):
    context = {}

    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''

    if 'search' in request.GET:
        return redirect('/' + request.GET.get('search'))
        
    return render(request, 'base/index.html', context=context)


def forecast_view(request, city):
    appid = 'a8b95910906c4134b9a152822241104'
    
    today_forecast = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={appid}&q={city}&days=5&alerts=on", stream=True).json()
    
    if 'forecast' not in today_forecast.keys():
        request.session['error'] = 'There is no such city.'
        return redirect('home')
    
    directions = {'W': 'Запад', 'E': 'Восток', 'S': 'Юг', 'N': 'Север'}
    
    for day in today_forecast['forecast']['forecastday']:
        day['name'] = datetime.strptime(day['date'], '%Y-%m-%d').strftime('%A')
        day['date'] = datetime.strptime(day['date'], '%Y-%m-%d').strftime('%B, %d')
        
    if 'search' in request.GET:
        return redirect('/' + request.GET.get('search'))
    
    context = {
        'name': today_forecast['location']['name'],
        'country': today_forecast['location']['country'],
        'curr_localtime': datetime.strptime(today_forecast['location']['localtime'], '%Y-%m-%d %H:%M').strftime("It's %H:%M. %B %d, %A."),
        
        'curr_condition_text': today_forecast['current']['condition']['text'].lower(),
        'curr_condition_icon': today_forecast['current']['condition']['icon'],
        
        'curr_temp': today_forecast['current']['temp_c'],
        'curr_temp_feelslike': today_forecast['current']['feelslike_c'],
        
        'curr_wind_speed': today_forecast['current']['wind_kph'],
        'curr_wind_direction': ''.join([directions[dir] for dir in today_forecast['current']['wind_dir']]),
        
        'curr_visibility': today_forecast['current']['vis_km'],
        'curr_humidity': today_forecast['current']['humidity'],
        'curr_pressure': today_forecast['current']['pressure_mb'] / 100,
        'curr_precip': today_forecast['current']['precip_mm'],
        
        'will_it_rain': bool(today_forecast['forecast']['forecastday'][0]['day']['daily_will_it_rain']),
        'will_it_snow': bool(today_forecast['forecast']['forecastday'][0]['day']['daily_will_it_snow']),
        
        'sunrise': today_forecast['forecast']['forecastday'][0]['astro']['sunrise'],
        'sunset': today_forecast['forecast']['forecastday'][0]['astro']['sunset'],
        
        'hours': today_forecast['forecast']['forecastday'][0]['hour'],
        'days': today_forecast['forecast']['forecastday'],
    }
    
    
    return render(request, 'base/forecast.html', context)
