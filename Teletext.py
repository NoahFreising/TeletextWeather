#!/usr/bin/env python3.7
# coding: utf-8

# In[1]:


from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import requests, json
from datetime import datetime
import conf


# In[2]:

# Get weather first
#uses openweatherApi, you need to register a free account
#your API key here
api_key = conf.api_key

base_url = "http://api.openweathermap.org/data/2.5/weather?"

#Referenzstädte
city_name = {"Norden":"Hamburg", "Westen":"Köln", "Süden":"Munich","Osten":"Berlin"}

complete_url = dict()
for key in city_name:
    complete_url[key] = base_url + "appid=" + api_key + "&q=" + city_name[key]

response = dict()

for key in city_name:
    response[key] = requests.get(complete_url[key])
    
        


# In[3]:


pythonData = dict()
for key in city_name:
    pythonData[key] = response[key].json()

wetter = dict()
minTemp = dict()
maxTemp = dict()

for key in city_name:
    if (pythonData[key]["cod"] != 404) and (pythonData[key]["cod"] != 401):
        x = pythonData[key]
        y=x["main"]
        minTemp[key] = y["temp_min"] - 273.15
        maxTemp[key] = y["temp_max"] - 273.15
        z = x["weather"]
        wetter[key] = z[0]["main"]
    else:
        print("City not found")


# In[29]:


wochentagKurz = ["Mo","Di","Mi","Do","Fr","Sa","So"]
wochentag = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","SAMSTAG","Sonntag"]
monat = ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"]
now = datetime.now()
dateNow = now.strftime("%d.%m.%y")
timeNow = now.strftime("%H:%M:%S")
weekday = int(now.weekday())
month = now.month-1 #for indexing


# In[6]:


# Codes from https://openweathermap.org/weather-conditions
translate = {"Mist":"Nebel","Fog":"Nebel","Clouds":"Wolken","Rain":"Regen","Clear":"Sonne","Snow":"Schnee","Drizzle":"Nieselregen","Thunderstorm":"Gewitter"}


# In[7]:


# position of elements in image1
wetterPos={"Norden":(107,260), "Westen":(107,320), "Süden":(107,380), "Osten":(107,440)}
wochentagPos = (386, 38)
datum = (430,38)
uhrzeit = (560,38)
tempMinPos={"Norden": (420,200), "Westen":(370,300),"Süden":(493,400),"Osten":(545,200)}
tempMaxPos={"Norden":(420,220),"Westen":(370,320),"Süden":(493,420),"Osten":(545,220)}


# In[8]:


img = Image.open(conf.slide1path)


# In[9]:


draw = ImageDraw.Draw(img)
font = ImageFont.truetype(conf.fontpath, 20)


# In[17]:


#draw values on map
for key in wetter:
    draw.text(wetterPos[key],translate[wetter[key]], (255,255,255), font=font)

for key in minTemp:
    draw.text(tempMinPos[key], '{:>3}'.format(int(minTemp[key]))+"°C", (255,255,255), font=font)

for key in maxTemp:
    draw.text(tempMaxPos[key], '{:>3}'.format(int(maxTemp[key]))+"°C", (255,255,255), font=font)
    
draw.text(datum, dateNow, (255,255,255), font=font)
draw.text(uhrzeit, timeNow, (0,255,0), font=font)
# print(weekday)
# print(wochentagKurz[weekday])
draw.text(wochentagPos, wochentagKurz[weekday], (255,255,255), font=font)


# In[18]:


img.save(conf.slide1output)


# In[19]:


cities = {"Berlin","Bremen","Dresden","Frankfurt","Cottbus","Hamburg","Hannover","Kiel","Köln","Leipzig","München","Nürnberg","Saarbrücken","Stuttgart"}

complete_url = dict()
for city in cities:
    complete_url[city] = base_url+ "appid=" + api_key + "&q=" + city

response = dict()
for city in cities:
    response[city] = requests.get(complete_url[city])


# In[20]:


#load data for img2

pythonData = dict()
for city in cities:
    pythonData[city] = response[city].json()

temperature = dict()
for city in cities:
    if (pythonData[city]["cod"] != '404') and (pythonData[city]["cod"] != 401):
        x = pythonData[city]
        y = x["main"]
        temperature[city] = round(y["temp"] - 273.15,0)
    else:
        print("City "+ city + " not found")


# In[21]:


#positions img2

wochentagLangPos = ()
stadtPos = dict()
i=0
for city in cities:
    stadtPos[city] = (608, 220 + i*20)
    i += 1
    


# In[36]:


# draw

img2 = Image.open(conf.slide2path)
draw = ImageDraw.Draw(img2)
font = ImageFont.truetype(conf.fontpath, 20)

i = 0;
for city in cities:
    if i % 2 == 0:
        color = (255,255,255)
    else:
        color = (0,255,255)
        
    draw.text(stadtPos[city], '{:>3}'.format(int(temperature[city]))+"°C", color, font=font)
    i += 1


draw.text(datum, dateNow, (255,255,255), font=font)
draw.text(uhrzeit, timeNow, (0,255,0), font=font)
draw.text(wochentagPos, wochentagKurz[weekday], (255,255,255), font = font)

datumsString = '{:>8}, {}.{} {}'.format(wochentag[weekday],now.day,monat[month],now.year)

draw.text((280,160),datumsString,(255,255,255),font=font)

img2.save(conf.slide2output)

gifim = [img]

gifim[0].save("/var/www/virtual/bread/html/weather/wetter.gif", format='GIF', append_images=[img2], save_all=True, duration=10000, loop=0)

