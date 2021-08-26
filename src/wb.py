import re
import pandas as pd
from os import system
from datetime import datetime, timedelta
from selenium import webdriver



""" load data """
total_cs = pd.read_csv('../input/weight_and_balance.csv')
rwy_df = pd.read_csv('../input/rwy_info.csv')



""" input """
system('cls')
print('This program comes with ABSOLUTELY NO WARRANTY. This is free software, and you are welcome to redistribute it under certain conditions. \n\n\n')
print('< Weight & Balance > \n')
print('ENTER for default setting')
print('* Default airport : KSFB')
print('* Default time : Current Time \n')

# airport id
arpt = input('- Departing Airport [ICAO] : ').lower()
print ('\033[1A' + '\033[K')
while True :
    if len(arpt) == 0:
        arpt = 'KSFB'
        print('- Departing Airport [ICAO] : KSFB')
        break
    elif len(arpt) != 4:
        print('\nERROR : Enter ICAO aiport codes with 4 letters\n')
        arpt = input('- Departing Airport [ICAO] : ').lower()
        print ('\033[1A' + '\033[K')
    else:
        print(f'- Departing Airport [ICAO] : {arpt}')
        break

# time
time = input('- Time(Z) [YYYYMMDD HHMM] : ')
print ('\033[1A' + '\033[K')
if len(time) == 0:
    time = datetime.utcnow()
    print(f'- Time(Z) [YYYYMMDD HHMM] : {time}Z')
else:
    time = datetime.strptime(time, '%Y%m%d %H%M')
    print(f'- Time(Z) [YYYYMMDD HHMM] : {time}Z')

# aircraft callsign
cs = input('- Aircraft N number : ').upper()
cs_df = total_cs[total_cs['N'] == cs]
print ('\033[1A' + '\033[K')
while True:
    if len(cs_df) == 0:
        print('\nERROR : Invalid N number')
        cs = input('- Aircraft N number : ').upper()
        cs_df = total_cs[total_cs['N'] == cs]
        print ('\033[1A' + '\033[K')
    else:
        print(f'- Aircraft N number : {cs}')
        break
print('\n\n\n')



""" Wx data"""
print('< Weather >')

# webdriver
options = webdriver.ChromeOptions()
options.add_argument("headless")
url = f'https://www.aviationweather.gov/metar/data?ids={arpt}&format=raw&hours=0&taf=on&layout=on'
driver = webdriver.Chrome(options=options)
driver.get(url)

# metar
metar = driver.find_element_by_xpath(f"//*[@id='awc_main_content_wrap']/code[1]")
metar = str(metar.text)

# taf
taf = driver.find_element_by_xpath(f"//*[@id='awc_main_content_wrap']/code[2]")
taf = str(taf.text)
driver.quit()

# print
print ('\033[1A' + '\033[K')
print('METAR') 
print(metar + '\n')
print('TAF')
print(taf)
print('\n\n\n')



""" wx to dataframe"""
# pattern
pattern_issue = '[0-9].....Z'
pattern_date = '[0-9]+/[0-9]{2,4}|[0-9][0-9][0-9][0-9][0-9][0-9]\s'
pattern_wind = '\s[0-9]...[0-9][A-Z]'              # limited below 100kt
pattern_temp = '[0-9][0-9]/[0-9][0-9]|M[0-9][0-9]/[0-9][0-9]|[0-9][0-9]/M[0-9][0-9]|M[0-9][0-9]/M[0-9][0-9]'
pattern_pres = 'A[0-9][0-9][0-9][0-9]'
pattern_vis = '\s[0-9][0-9]SM\s'               
pattern_cavok = '\sC[A-Z][A-Z][A-Z][A-Z]\s'
pattern_wc = 'NSW|TS|DZ|RA|SN|SG|IC|PL|GR|GS|BR|FG|FU|VA|DU|SA|HZ|SQ|FC|SS|DS'
pattern_cloud = '[FSBO][A-Z][A-Z]..[0-9]'
pattern_chg = 'BECMG|TEMPO|FM'
regex = re.compile(pattern_date)
search = regex.search(metar)

# issue time
issue = metar[re.search(pattern_issue, metar).start() : re.search(pattern_issue, metar).start()+6]
if datetime.utcnow().day > int(issue[:2]):
    yyyymm = datetime.utcnow().strftime('%Y') + (datetime.utcnow() + timedelta(days = 1)).strftime('%m')    # 달 넘어가는 것
else: 
    yyyymm = datetime.utcnow().strftime('%Y') + datetime.utcnow().strftime('%m')
issue_time = datetime.strptime(yyyymm + issue, '%Y%m%d%H%M')

# wind
wind_dir = int(metar[re.search(pattern_wind, metar).start()+1 : re.search(pattern_wind, metar).start()+4])
wind_vel = int(metar[re.search(pattern_wind, metar).start()+4 : re.search(pattern_wind, metar).start()+6])
if metar[re.search(pattern_wind, metar).start()+6] == 'G':
    gust = metar[re.search(pattern_wind, metar).start()+6 : re.search(pattern_wind, metar).start()+9]
else:
    gust = 0

# temp, due
if metar[re.search(pattern_temp, metar).start()] == 'M':
    temp = int(metar[re.search(pattern_temp, metar).start()+1 : re.search(pattern_temp, metar).start()+3]) * (-1)
else:
    temp = int(metar[re.search(pattern_temp, metar).start() : re.search(pattern_temp, metar).start()+2])
if metar[re.search(pattern_temp, metar).end()-3] == 'M':
    due = int(metar[re.search(pattern_temp, metar).end()-2 : re.search(pattern_temp, metar).end()]) * (-1)
else:
    due = int(metar[re.search(pattern_temp, metar).end()-2 : re.search(pattern_temp, metar).end()])

# pressure
pres = int(metar[re.search(pattern_pres, metar).start()+1 : re.search(pattern_pres, metar).start()+5])/100

# rwy
fe = rwy_df[rwy_df['arpt'] == arpt]['fe'][0] * 0.3048    # field elevation(ft) into meters

# station pressure (https://www.weather.gov/media/epz/wxcalc/stationPressure.pdf)
station_pressure_inHg = pres * (((288 - (0.0065 * fe))/288)**(5.2561))
station_pressure_mil = station_pressure_inHg * 33.8639

# pressure altitude(https://www.weather.gov/media/epz/wxcalc/pressureAltitude.pdf)
pa = (1 - (station_pressure_mil/1013.25)**(0.190284)) * 145366.45

# density altitude (https://www.weather.gov/media/epz/wxcalc/densityAltitude.pdf)
vapor_pressure = 6.11 * (10 **((7.5 * due) / (237.7 + due)))
tv_kelvin = (temp + 273.15) / (1 - ((vapor_pressure / station_pressure_mil) * (1 - 0.622)))  # Kelvin
tv_rankine = (tv_kelvin * 9 / 5)
da = 145366 * ( 1 - ((17.326 * station_pressure_mil * 0.029530 / tv_rankine )**(0.235)))









""" takeoff data """
# wind_dir = 
# wind_vel = 
# gust = 
# h_wind = 
# cross_wind = 
# vis = 
# cig = 
# temp = 
# due = 
# alt = 
# active_rwy = 
# pressure_alt
# density_alt
# rwy_len

print('< Takeoff Dataframe > \n\n')

wx = pd.DataFrame({'issue' : issue_time,
                    'wind_direction' : wind_dir,
                    'wind_velocity' : wind_vel,
                    'gust' : gust,
                    'temperature' : temp,
                    'due_point' : due,
                    'altimeter' : pres,
                    'pressure_altitude' : pa,
                    'density_altitude' : da,
                    }, index = [0])

print(wx)
print(fe)
print('\n\n\n')





print('CREDITS \n\n ============ \n\n Sanghyok Han \n\n ============ \n\n')