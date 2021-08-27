import re
import pandas as pd
import numpy as np
from os import system
from datetime import datetime, timedelta
from selenium import webdriver





""" load data """
total_cs = pd.read_csv('../input/weight_and_balance.csv')
rwy_df = pd.read_csv('../input/rwy_info.csv')





""" input """
system('cls')
print('This program comes with ABSOLUTELY NO WARRANTY. This is free software, and you are welcome to redistribute it under certain conditions. \n')
print('------------------------------------------------------------------------------------- \n')
print('< Weight & Balance > \n\n')
print('ENTER for default setting')
print('* Default airport : KSFB')
print('* Default time : Current Time \n')



# airport id
arpt = input('- Departing Airport [ICAO] : ').upper()
print ('\033[1A' + '\033[K')
while True :
    if len(arpt) == 0:
        arpt = 'KSFB'
        print('- Departing Airport [ICAO] : KSFB')
        break
    elif len(arpt) != 4:
        print('\nERROR : Enter ICAO aiport codes with 4 letters\n')
        arpt = input('- Departing Airport [ICAO] : ').upper()
        print ('\033[1A' + '\033[K')
    else:
        print(f'- Departing Airport [ICAO] : {arpt}')
        break

arpt2 = input('- Arrival Airport [ICAO] : ').upper()
print ('\033[1A' + '\033[K')
while True :
    if len(arpt2) == 0:
        arpt2 = 'KSFB'
        print('- Arrival Airport [ICAO] : KSFB')
        break
    elif len(arpt2) != 4:
        print('\nERROR : Enter ICAO aiport codes with 4 letters\n')
        arpt2 = input('- Arrival Airport [ICAO] : ').upper()
        print ('\033[1A' + '\033[K')
    else:
        print(f'- Arrival Airport [ICAO] : {arpt2}')
        break



# time
time = input('- Estimated Time Departing(Z) [YYYYMMDD HHMM] , or Flight after [HH] : ')
print ('\033[1A' + '\033[K')
if len(time) == 0:
    time = datetime.utcnow()
    print(f'- Estimated Time Departing(Z) : {time}Z')
elif len(time) == 2:
    time = datetime.utcnow() + timedelta(hours = int(time))
    print(f'- Estimated Time Departing(Z) : {time}Z')
elif len(time) == 1:
    time = datetime.utcnow() + timedelta(hours = int(time))
    print(f'- Estimated Time Departing(Z) : {time}Z')
else:
    time = datetime.strptime(time, '%Y%m%d %H%M')
    print(f'- Estimated Time Departing(Z) [YYYYMMDD HHMM] : {time}Z')

time2 = input('- Estimated Time Arrival(Z) [YYYYMMDD HHMM] , or Flight Time [HH] : ')
print ('\033[1A' + '\033[K')
if len(time2) == 0:
    time2 = datetime.utcnow()
    print(f'- Estimated Time Arrival(Z) : {time2}Z')
elif len(time2) == 2:
    time2 = time + timedelta(hours = int(time2))
    print(f'- Estimated Time Arrival(Z) : {time2}Z')
elif len(time2) == 1:
    time2 = time + timedelta(hours = int(time2))
    print(f'- Estimated Time Arrival(Z) : {time2}Z')
else:
    time2 = datetime.strptime(time2, '%Y%m%d %H%M')
    print(f'- Estimated Time Arrival(Z) [YYYYMMDD HHMM] : {time2}Z')



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
print('\n-------------------------------------------------------------------------------------\n')





""" Wx data"""
print('< Weather >')



# webdriver
options = webdriver.ChromeOptions()
options.add_argument("headless")
url = f'https://www.aviationweather.gov/metar/data?ids={arpt}&format=raw&hours=0&taf=on&layout=on'
url2 = f'https://www.aviationweather.gov/metar/data?ids={arpt2}&format=raw&hours=0&taf=on&layout=on'
driver = webdriver.Chrome(options=options)
driver.get(url)



# metar
try:
    metar = driver.find_element_by_xpath(f"//*[@id='awc_main_content_wrap']/code[1]")
    metar = str(metar.text)
except:
    metar = ''



# taf
try:
    taf = driver.find_element_by_xpath(f"//*[@id='awc_main_content_wrap']/code[2]")
    taf = str(taf.text)
except: 
    taf = ''
driver.quit()
print ('\033[1A' + '\033[K')



# webdriver2
driver = webdriver.Chrome(options=options)
driver.get(url2)



# metar2
try:
    metar2 = driver.find_element_by_xpath(f"//*[@id='awc_main_content_wrap']/code[1]")
    metar2 = str(metar2.text)
except:
    metar2 = ''



# taf2
try:
    taf2 = driver.find_element_by_xpath(f"//*[@id='awc_main_content_wrap']/code[2]")
    taf2 = str(taf2.text)
except: 
    taf2 = ''
driver.quit()



# print wx
print ('\033[1A' + '\033[K')
print('- Departure METAR') 
if len(metar) == 0:
    print('  METAR not reported\n')
else:
    print('  ' + metar + '\n')
print('- Departure TAF')
if len(taf) == 0:
    print('  TAF not reported')
else:
    print('  ' + taf + '\n\n')

print('- Arrival METAR') 
if len(metar2) == 0:
    print('  METAR not reported\n')
else:
    print('  ' + metar2 + '\n')
print('- Arrival TAF')
if len(taf2) == 0:
    print('  TAF not reported')
else:
    print('  ' + taf2)



# additional arrival airport info
print('\n\n- Arrival Information')
temp2 = float(input('  Arrival Airport Temperature [##] : '))
due2 = float(input('  Arrival Airport Due point [##] : '))
pres2 = float(input('  Arrival Airport Altimeter Setting [##.##] : '))
print('\n-------------------------------------------------------------------------------------\n')





""" weather """
# pattern
pattern_issue = '[0-9].....Z'
pattern_date = '[0-9]+/[0-9]{2,4}|[0-9][0-9][0-9][0-9][0-9][0-9]\s'
pattern_wind = '\s[0-9]...[0-9][A-Z]|\sV...[0-9][A-Z]'              # limited below 100kt
pattern_temp = '[0-9][0-9]/[0-9][0-9]|M[0-9][0-9]/[0-9][0-9]|[0-9][0-9]/M[0-9][0-9]|M[0-9][0-9]/M[0-9][0-9]'
pattern_pres = 'A[0-9][0-9][0-9][0-9]'
pattern_vis = '\s.[0-9]SM\s|\s[0-9]SM\s'               
pattern_cloud = '[FSBO][ECKV][WTNC][0-9][0-9][0-9]|CLR|SKC|VV[0-9][0-9][0-9]'
pattern_cavok = '\sC[A-Z][A-Z][A-Z][A-Z]\s'
pattern_wc = 'NSW|TS|DZ|RA|SN|SG|IC|PL|GR|GS|BR|FG|FU|VA|DU|SA|HZ|SQ|FC|SS|DS'
pattern_chg = 'BECMG\s[0-9][0-9][0-9][0-9]/[0-9][0-9][0-9][0-9]|TEMPO\s[0-9][0-9][0-9][0-9]/[0-9][0-9][0-9][0-9]|FM[0-9][0-9][0-9][0-9][0-9][0-9]'
regex = re.compile(pattern_date)
search = regex.search(metar)



# issue time
issue = metar[re.search(pattern_issue, metar).start() : re.search(pattern_issue, metar).start()+6]
if datetime.utcnow().day > int(issue[:2]):
    yyyymm = datetime.utcnow().strftime('%Y') + (datetime.utcnow() + timedelta(days = 1)).strftime('%m')    # 달 넘어가는 것
else: 
    yyyymm = datetime.utcnow().strftime('%Y') + datetime.utcnow().strftime('%m')
issue_time = datetime.strptime(yyyymm + issue, '%Y%m%d%H%M')



# arrival data
issue_2 = metar2[re.search(pattern_issue, metar2).start() : re.search(pattern_issue, metar2).start()+6]
if datetime.utcnow().day > int(issue_2[:2]):
    yyyymm = datetime.utcnow().strftime('%Y') + (datetime.utcnow() + timedelta(days = 1)).strftime('%m')    # 달 넘어가는 것
else: 
    yyyymm = datetime.utcnow().strftime('%Y') + datetime.utcnow().strftime('%m')
issue_time_2 = datetime.strptime(yyyymm + issue_2, '%Y%m%d%H%M')
chg2 = list(re.finditer(pattern_chg, taf2))
taf_df = pd.DataFrame()
taf_df = taf_df.append(pd.DataFrame({issue_time_2 : metar2}, index = ['taf']).T)
taftaf = taf
for change in range(len(chg2)):
    try:
        temp_taf = taftaf[chg2[change].start():chg2[change+1].start()]
    except:
        temp_taf = taftaf[chg2[change].start():]
        
    if taftaf[chg2[change].start():chg2[change].start()+2] == 'FM':
        temp_time = datetime.strptime(yyyymm+temp_taf[2:8], '%Y%m%d%H%M')
        taf_df = taf_df.append(pd.DataFrame({temp_time : temp_taf}, index = ['taf']).T)
    elif taftaf[chg2[change].start():chg2[change].start()+5] == 'BECMG':
        temp_time = datetime.strptime(yyyymm+temp_taf[6:10], '%Y%m%d%H')
        taf_df = taf_df.append(pd.DataFrame({temp_time : temp_taf}, index = ['taf']).T)
    elif taftaf[chg2[change].start():chg2[change].start()+5] == 'TEMPO':           
        temp_time_s = datetime.strptime(yyyymm+temp_taf[6:10], '%Y%m%d%H')
        temp_time_e = datetime.strptime(yyyymm+temp_taf[11:15], '%Y%m%d%H')
        taf_df = taf_df.append(pd.DataFrame({temp_time_s : temp_taf}, index = ['taf']).T)
        taf_df = taf_df.append(pd.DataFrame(taf_df.iloc[-2,:].values, index = [temp_time_e], columns = ['taf']))

wx2 = pd.DataFrame({issue_time_2 : metar2}, index = ['taf']).T
for i in range(1, len(taf_df)):
    if taf_df.index[1] > time2:
        wx2 = taf[:chg2[0].start()]
        break
    elif taf_df.index[i] < time2:
        wx2 = taf_df['taf'][i]
    else:
        break

issue2 = taf[re.search(pattern_issue, taf).start() : re.search(pattern_issue, taf).start()+6]
issue_time2 = datetime.strptime(yyyymm + issue2, '%Y%m%d%H%M')



# wind
wind_dir = metar[re.search(pattern_wind, metar).start()+1 : re.search(pattern_wind, metar).start()+4].zfill(3)
wind_vel = metar[re.search(pattern_wind, metar).start()+4 : re.search(pattern_wind, metar).start()+6].zfill(2)
if metar[re.search(pattern_wind, metar).start()+6] == 'G':
    gust = metar[re.search(pattern_wind, metar).start()+6 : re.search(pattern_wind, metar).start()+9]
else:
    gust = 0



# wind2
try:
    wind_dir2 = wx2[re.search(pattern_wind, wx2).start()+1 : re.search(pattern_wind, wx2).start()+4].zfill(3)
    wind_vel2 = wx2[re.search(pattern_wind, wx2).start()+4 : re.search(pattern_wind, wx2).start()+6].zfill(2)

    if wx2[re.search(pattern_wind, wx2).start()+6] == 'G':
        gust2 = wx2[re.search(pattern_wind, wx2).start()+6 : re.search(pattern_wind, wx2).start()+9]
    else:
        gust2 = 0
except: 
    wind_dir2 = 'X'
    wind_vel2 = 'X'
    gust2 = 'X'



# vis
vis =  int(metar[re.search(pattern_vis, metar).start()+1 : re.search(pattern_vis, metar).end()-3])



# vis2
try:
    vis2 = int(wx2[re.search(pattern_vis, wx2).start()+1 : re.search(pattern_vis, wx2).end()-3])
except:
    vis2 = 'X'



# cloud
cloud_list = list(re.finditer(pattern_cloud, metar))
for cld in range(len(cloud_list)):
    if (cloud_list[cld][0][:3] == 'BKN') or (cloud_list[cld][0][:3] == 'OVC'):
        cig = cloud_list[cld][0]
        break
    else:
        cig = 'X'



# cloud2
try:
    cloud_list2 = list(re.finditer(pattern_cloud, wx2))
    for cld in range(len(cloud_list2)):
        if (cloud_list2[cld][0][:3] == 'BKN') or (cloud_list2[cld][0][:3] == 'OVC'):
            cig2 = cloud_list2[cld][0]
            break
        else:
            cig2 = 'X'
except:
    cig2 = 'X'



# temp, due
if metar[re.search(pattern_temp, metar).start()] == 'M':
    temp = int(metar[re.search(pattern_temp, metar).start()+1 : re.search(pattern_temp, metar).start()+3]) * (-1)
else:
    temp = int(metar[re.search(pattern_temp, metar).start() : re.search(pattern_temp, metar).start()+2])
if metar[re.search(pattern_temp, metar).end()-3] == 'M':
    due = int(metar[re.search(pattern_temp, metar).end()-2 : re.search(pattern_temp, metar).end()]) * (-1)
else:
    due = int(metar[re.search(pattern_temp, metar).end()-2 : re.search(pattern_temp, metar).end()])



# temp2, due2
#if wx2[re.search(pattern_temp, wx2).start()] == 'M':
#    temp2 = int(wx2[re.search(pattern_temp, wx2).start()+1 : re.search(pattern_temp, wx2).start()+3]) * (-1)
#else:
#    temp2 = int(wx2[re.search(pattern_temp, wx2).start() : re.search(pattern_temp, wx2).start()+2])
#if wx2[re.search(pattern_temp, wx2).end()-3] == 'M':
#    due2 = int(wx2[re.search(pattern_temp, wx2).end()-2 : re.search(pattern_temp, wx2).end()]) * (-1)
#else:
#    due2 = int(wx2[re.search(pattern_temp, wx2).end()-2 : re.search(pattern_temp, wx2).end()])
#temp2 = float(input('temp2'))
#due2 = float(input('due2'))



# pressure
pres = int(metar[re.search(pattern_pres, metar).start()+1 : re.search(pattern_pres, metar).start()+5])/100



# pressure2
#pres2 = int(wx2[re.search(pattern_pres, wx2).start()+1 : re.search(pattern_pres, wx2).start()+5])/100
#pres2 = float(input('pres2'))



# station pressure (https://www.weather.gov/media/epz/wxcalc/stationPressure.pdf)
temp_rwy_df = rwy_df[rwy_df['arpt'] == arpt].reset_index(drop=True)
temp_rwy_df2 = rwy_df[rwy_df['arpt'] == arpt2].reset_index(drop=True)
fe = temp_rwy_df['fe'][0] * 0.3048    # field elevation(ft) into meters
fe2 = temp_rwy_df2['fe'][0] * 0.3048
station_pressure_inHg = pres * (((288 - (0.0065 * fe))/288)**(5.2561))
station_pressure_mil = station_pressure_inHg * 33.8639
station_pressure_inHg2 = pres2 * (((288 - (0.0065 * fe2))/288)**(5.2561))
station_pressure_mil2 = station_pressure_inHg2 * 33.8639



# pressure altitude(https://www.weather.gov/media/epz/wxcalc/pressureAltitude.pdf)
pa = (1 - (station_pressure_mil/1013.25)**(0.190284)) * 145366.45
pa = round(pa)
pa2 = (1 - (station_pressure_mil2/1013.25)**(0.190284)) * 145366.45
pa2 = round(pa2)



# density altitude (https://www.weather.gov/media/epz/wxcalc/densityAltitude.pdf)
vapor_pressure = 6.11 * (10 **((7.5 * due) / (237.7 + due)))
tv_kelvin = (temp + 273.15) / (1 - ((vapor_pressure / station_pressure_mil) * (1 - 0.622)))  # Kelvin
tv_rankine = (tv_kelvin * 9 / 5)
da = 145366 * ( 1 - ((17.326 * station_pressure_mil * 0.029530 / tv_rankine )**(0.235)))
da = round(da)
vapor_pressure2 = 6.11 * (10 **((7.5 * due2) / (237.7 + due2)))
tv_kelvin2 = (temp2 + 273.15) / (1 - ((vapor_pressure2 / station_pressure_mil2) * (1 - 0.622)))  # Kelvin
tv_rankine2 = (tv_kelvin2 * 9 / 5)
da2 = 145366 * ( 1 - ((17.326 * station_pressure_mil2 * 0.029530 / tv_rankine2 )**(0.235)))
da2 = round(da2)

#####################################################################################################################

# 현천 나오게 하기

###################################################################################################################





""" runway information """
# rwy
temp_rwy_df = rwy_df[rwy_df['arpt'] == arpt].reset_index(drop=True)
print('< Runway Information > \n\n')
print('- Departing Airpot : ' + temp_rwy_df['arpt'][0])

rwy_hdg = []
rwy_name = []
for rwy_info in range(1,(len(temp_rwy_df.T.dropna())-2)//4+2):
    print('  Runway ' + temp_rwy_df[f'rwy{rwy_info}'][0] 
          + ' = HDG : ' + str(int(temp_rwy_df[f'heading{rwy_info}'][0])).zfill(3) + '/' + str(180+int(temp_rwy_df[f'heading{rwy_info}'][0])).zfill(3)
          + '  Length : ' + str(int(temp_rwy_df[f'length{rwy_info}'][0])) + "'")
    rwy_hdg.append(int(temp_rwy_df[f'heading{rwy_info}'][0]))
    rwy_name.append(temp_rwy_df[f'rwy{rwy_info}'][0])
    


# favored runway
if wind_dir == 'VRB':
    fav_rwy = np.array(rwy_name)
elif wind_dir == 'X':
    fav_rwy = np.array(rwy_name)
else:
    fav_rwy_array = list(np.array(rwy_hdg) - np.ones(len(rwy_hdg)) * int(wind_dir))
    fav_rwy_value = min(fav_rwy_array)
    rwy_name = np.array(rwy_name)
    fav_rwy = rwy_name[fav_rwy_array == fav_rwy_value]
print('\n- Wind Direction : ' + wind_dir)
print('\n- Favored Runway')
for fav in range(len(fav_rwy)):
    print('  ' + fav_rwy[fav])
    


# active runway
active_rwy = input(f'\n- {arpt} Active Runway [##]: ')
act_rwy_array = list(np.array(rwy_hdg) - np.ones(len(rwy_hdg)) * int(active_rwy))
act_rwy_value = min(act_rwy_array)
active_rwy_length = []
active_rwy_heading = []
for i in range(1, len(act_rwy_array)):
    if act_rwy_array[i-1] == act_rwy_value:
        active_rwy_length.append(temp_rwy_df[f'length{i}'][0])
        active_rwy_heading.append(temp_rwy_df[f'heading{i}'][0])



# headwind, crosswind
if wind_dir == 'VRB':
    headwind = wind_vel
    crosswind = wind_vel
elif wind_dir == 'VRB':
    headwind = wind_vel
    crosswind = wind_vel
else:
    headwind = np.cos(abs(int(wind_dir) - active_rwy_heading[0]) * np.pi/180) * float(wind_vel)
    headwind = round(headwind,1)
    crosswind = np.sin(abs(int(wind_dir) - active_rwy_heading[0]) * np.pi/180) * float(wind_vel)
    crosswind = round(crosswind,1)

print('\n\n')



# rwy2
temp_rwy_df2 = rwy_df[rwy_df['arpt'] == arpt2].reset_index(drop=True)
print('- Arrival Airpot : ' + temp_rwy_df2['arpt'][0])

rwy_hdg2 = []
rwy_name2 = []
for rwy_info in range(1,(len(temp_rwy_df2.T.dropna())-2)//4+2):
    print('  Runway ' + temp_rwy_df2[f'rwy{rwy_info}'][0] 
          + ' = HDG : ' + str(int(temp_rwy_df2[f'heading{rwy_info}'][0])).zfill(3) + '/' + str(180+int(temp_rwy_df2[f'heading{rwy_info}'][0])).zfill(3)
          + '  Length : ' + str(int(temp_rwy_df2[f'length{rwy_info}'][0])) + "'")
    rwy_hdg2.append(int(temp_rwy_df2[f'heading{rwy_info}'][0]))
    rwy_name2.append(temp_rwy_df2[f'rwy{rwy_info}'][0])
    


# favored runway2
if wind_dir2 == 'VRB':
    fav_rwy2 = np.array(rwy_name2)
elif wind_dir2 == 'X':
    fav_rwy2 = np.array(rwy_name2)
else:
    fav_rwy_array2 = list(np.array(rwy_hdg2) - np.ones(len(rwy_hdg2)) * int(wind_dir2))
    fav_rwy_value2 = min(fav_rwy_array2)
    rwy_name2 = np.array(rwy_name2)
    fav_rwy2 = rwy_name2[fav_rwy_array2 == fav_rwy_value2]
print('\n- Wind Direction : ' + wind_dir2)
print('\n- Favored Runway')
for fav in range(len(fav_rwy2)):
    print('  ' + fav_rwy2[fav])
    


# active runway2
active_rwy2 = input(f'\n- {arpt2} Active Runway [##]: ')
act_rwy_array2 = list(np.array(rwy_hdg2) - np.ones(len(rwy_hdg2)) * int(active_rwy2))
act_rwy_value2 = min(act_rwy_array2)
active_rwy_length2 = []
active_rwy_heading2 = []
for i in range(1, len(act_rwy_array2)):
    if act_rwy_array2[i-1] == act_rwy_value2:
        active_rwy_length2.append(temp_rwy_df2[f'length{i}'][0])
        active_rwy_heading2.append(temp_rwy_df2[f'heading{i}'][0])



# headwind2, crosswind2
if wind_dir2 == 'VRB':
    headwind2 = wind_vel2
    crosswind2 = wind_vel2
elif wind_dir2 == 'X':
    headwind2 = wind_vel2
    crosswind2 = wind_vel2
else:
    headwind2 = np.cos(abs(int(wind_dir2) - active_rwy_heading2[0]) * np.pi/180) * float(wind_vel2)
    headwind2 = round(headwind2,1)
    crosswind2 = np.sin(abs(int(wind_dir2) - active_rwy_heading2[0]) * np.pi/180) * float(wind_vel2)
    crosswind2 = round(crosswind2,1)
print('\n-------------------------------------------------------------------------------------\n')





""" takeoff data """

print('< Takeoff Dataframe > \n')

wx = pd.DataFrame({'issue(Z)' : issue_time,
                    'time' : time,
                    'airport' : arpt,
                    'wind_direction' : wind_dir,
                    'wind_velocity' : wind_vel,
                    'gust' : gust,
                    'visibility' : vis,
                    'ceiling' : cig,
                    'temperature' : temp,
                    'due_point' : due,
                    'altimeter' : pres,
                    'active_runway' : active_rwy,
                    'pressure_altitude' : pa,
                    'density_altitude' : da,
                    'available_runway_length' : str(active_rwy_length),
                    'headwind_component' : headwind,
                    'crosswind_component' : crosswind
                    }, index = ['Departure'])
wx = wx.append(pd.DataFrame({'issue(Z)' : issue_time2,
                    'time' : time2,
                    'airport' : arpt2,
                    'wind_direction' : wind_dir2,
                    'wind_velocity' : wind_vel2,
                    'gust' : gust2,
                    'visibility' : vis2,
                    'ceiling' : cig2,
                    'temperature' : temp2,
                    'due_point' : due2,
                    'altimeter' : pres2,
                    'active_runway' : active_rwy2,
                    'pressure_altitude' : pa2,
                    'density_altitude' : da2,
                    'available_runway_length' : str(active_rwy_length2),
                    'headwind_component' : headwind2,
                    'crosswind_component' : crosswind2
                    }, index = ['Arrival']))
print(wx.T)
print('\n-------------------------------------------------------------------------------------\n')
print('CREDITS \n ============ \n\n Sanghyok Han \n\n ============ \n\n')