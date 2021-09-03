import re
import pandas as pd
import numpy as np
import win32com.client
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
print('press ENTER for default setting')
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
cs_df = cs_df.reset_index(drop = True)
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
    print('  TAF not reported\n')
else:
    print('  ' + taf + '\n\n')

print('- Arrival METAR') 
if len(metar2) == 0:
    print('  METAR not reported\n')
else:
    print('  ' + metar2 + '\n')
print('- Arrival TAF')
if len(taf2) == 0:
    print('  TAF not reported\n')
else:
    print('  ' + taf2)





""" weather """
# pattern
pattern_issue = '[0-9].....Z'
pattern_date = '[0-9]+/[0-9]{2,4}|[0-9][0-9][0-9][0-9][0-9][0-9]\s'
pattern_wind = '\s[0-9]...[0-9][A-Z]|\sV...[0-9][A-Z]'              # limited below 100kt
pattern_temp = '\s[0-9][0-9]/[0-9][0-9]\s|\sM[0-9][0-9]/[0-9][0-9]\s|\s[0-9][0-9]/M[0-9][0-9]\s|\sM[0-9][0-9]/M[0-9][0-9]\s'
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



# departure data
chg = list(re.finditer(pattern_chg, taf))
dep_taf_df = pd.DataFrame()
dep_taf_df = dep_taf_df.append(pd.DataFrame({issue_time : metar}, index = ['taf']).T)
taftaf = taf
for change in range(len(chg)):
    try:
        temp_taf = taftaf[chg[change].start():chg[change+1].start()]
    except:
        temp_taf = taftaf[chg[change].start():]
        
    if taftaf[chg[change].start():chg[change].start()+2] == 'FM':
        temp_time = datetime.strptime(yyyymm+temp_taf[2:8], '%Y%m%d%H%M')
        dep_taf_df = dep_taf_df.append(pd.DataFrame({temp_time : temp_taf}, index = ['taf']).T)
    elif taftaf[chg[change].start():chg[change].start()+5] == 'BECMG':
        temp_time = datetime.strptime(yyyymm+temp_taf[6:10], '%Y%m%d%H')
        dep_taf_df = dep_taf_df.append(pd.DataFrame({temp_time : temp_taf}, index = ['taf']).T)
    elif taftaf[chg[change].start():chg[change].start()+5] == 'TEMPO':           
        temp_time_s = datetime.strptime(yyyymm+temp_taf[6:10], '%Y%m%d%H')
        temp_time_e = datetime.strptime(yyyymm+temp_taf[11:15], '%Y%m%d%H')
        dep_taf_df = dep_taf_df.append(pd.DataFrame({temp_time_s : temp_taf}, index = ['taf']).T)
        dep_taf_df = dep_taf_df.append(pd.DataFrame(dep_taf_df.iloc[-2,:].values, index = [temp_time_e], columns = ['taf']))

wx1 = pd.DataFrame({issue_time : metar}, index = ['taf']).T
for i in range(1, len(dep_taf_df)):
    if dep_taf_df.index[1] > time:
        if time - datetime.utcnow() + timedelta(minutes = 5) > timedelta(hours = 1):    # 1시간 이상이면
            wx1 = taf[:chg[0].start()]
        else:
            wx1 = dep_taf_df['taf'][0]
        break
    elif dep_taf_df.index[i] < time:
        wx1 = dep_taf_df['taf'][i]
    else:
        break



# arrival data
issue_2 = metar2[re.search(pattern_issue, metar2).start() : re.search(pattern_issue, metar2).start()+6]
if datetime.utcnow().day > int(issue_2[:2]):
    yyyymm = datetime.utcnow().strftime('%Y') + (datetime.utcnow() + timedelta(days = 1)).strftime('%m')    # 달 넘어가는 것
else: 
    yyyymm = datetime.utcnow().strftime('%Y') + datetime.utcnow().strftime('%m')
issue_time_2 = datetime.strptime(yyyymm + issue_2, '%Y%m%d%H%M')
chg2 = list(re.finditer(pattern_chg, taf2))
taf_df = pd.DataFrame()    # taf_df = arr_taf_df
taf_df = taf_df.append(pd.DataFrame({issue_time_2 : metar2}, index = ['taf']).T)
taftaf2 = taf2
for change in range(len(chg2)):
    try:
        temp_taf = taftaf2[chg2[change].start():chg2[change+1].start()]
    except:
        temp_taf = taftaf2[chg2[change].start():]
        
    if taftaf2[chg2[change].start():chg2[change].start()+2] == 'FM':
        temp_time = datetime.strptime(yyyymm+temp_taf[2:8], '%Y%m%d%H%M')
        taf_df = taf_df.append(pd.DataFrame({temp_time : temp_taf}, index = ['taf']).T)
    elif taftaf2[chg2[change].start():chg2[change].start()+5] == 'BECMG':
        temp_time = datetime.strptime(yyyymm+temp_taf[6:10], '%Y%m%d%H')
        taf_df = taf_df.append(pd.DataFrame({temp_time : temp_taf}, index = ['taf']).T)
    elif taftaf2[chg2[change].start():chg2[change].start()+5] == 'TEMPO':           
        temp_time_s = datetime.strptime(yyyymm+temp_taf[6:10], '%Y%m%d%H')
        temp_time_e = datetime.strptime(yyyymm+temp_taf[11:15], '%Y%m%d%H')
        taf_df = taf_df.append(pd.DataFrame({temp_time_s : temp_taf}, index = ['taf']).T)
        taf_df = taf_df.append(pd.DataFrame(taf_df.iloc[-2,:].values, index = [temp_time_e], columns = ['taf']))

wx2 = pd.DataFrame({issue_time_2 : metar2}, index = ['taf']).T
for i in range(1, len(taf_df)):
    if taf_df.index[1] > time2:
        wx2 = taf2[:chg2[0].start()]
        break
    elif taf_df.index[i] < time2:
        wx2 = taf_df['taf'][i]
    else:
        break

issue2 = taf2[re.search(pattern_issue, taf2).start() : re.search(pattern_issue, taf2).start()+6]
issue_time2 = datetime.strptime(yyyymm + issue2, '%Y%m%d%H%M')



# wind
try:
    wind_dir = wx1[re.search(pattern_wind, wx1).start()+1 : re.search(pattern_wind, wx1).start()+4].zfill(3)
    wind_vel = wx1[re.search(pattern_wind, wx1).start()+4 : re.search(pattern_wind, wx1).start()+6].zfill(2)
    if wx1[re.search(pattern_wind, wx1).start()+6] == 'G':
        gust = wx1[re.search(pattern_wind, wx1).start()+6 : re.search(pattern_wind, wx1).start()+9]
    else:
        gust = str(0)
except:
    wind_dir = metar[re.search(pattern_wind, metar).start()+1 : re.search(pattern_wind, metar).start()+4].zfill(3)
    wind_vel = metar[re.search(pattern_wind, metar).start()+4 : re.search(pattern_wind, metar).start()+6].zfill(2)
    if metar[re.search(pattern_wind, metar).start()+6] == 'G':
        gust = metar[re.search(pattern_wind, metar).start()+6 : re.search(pattern_wind, metar).start()+9]
    else:
        gust = str(0)



# wind2
try:
    wind_dir2 = wx2[re.search(pattern_wind, wx2).start()+1 : re.search(pattern_wind, wx2).start()+4].zfill(3)
    wind_vel2 = wx2[re.search(pattern_wind, wx2).start()+4 : re.search(pattern_wind, wx2).start()+6].zfill(2)

    if wx2[re.search(pattern_wind, wx2).start()+6] == 'G':
        gust2 = wx2[re.search(pattern_wind, wx2).start()+6 : re.search(pattern_wind, wx2).start()+9]
    else:
        gust2 = str(0)
except: 
    wind_dir2 = 'X'
    wind_vel2 = 'X'
    gust2 = 'X'



# vis
try:
    vis =  int(wx1[re.search(pattern_vis, wx1).start()+1 : re.search(pattern_vis, wx1).end()-3])
except:
    vis =  int(metar[re.search(pattern_vis, metar).start()+1 : re.search(pattern_vis, metar).end()-3])



# vis2
try:
    vis2 = int(wx2[re.search(pattern_vis, wx2).start()+1 : re.search(pattern_vis, wx2).end()-3])
except:
    vis2 = 'X'



# cloud
try:
    cloud_list = list(re.finditer(pattern_cloud, wx1))
except:
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
try: 
    if wx1[re.search(pattern_temp, wx1).start()] == 'M':
        temp = int(wx1[re.search(pattern_temp, wx1).start()+2 : re.search(pattern_temp, wx1).start()+4]) * (-1)
    else:
        temp = int(wx1[re.search(pattern_temp, wx1).start()+1 : re.search(pattern_temp, wx1).start()+3])
    if wx1[re.search(pattern_temp, wx1).end()-3] == 'M':
        due = int(wx1[re.search(pattern_temp, wx1).end()-3 : re.search(pattern_temp, wx1).end()-1]) * (-1)
    else:
        due = int(wx1[re.search(pattern_temp, wx1).end()-3 : re.search(pattern_temp, wx1).end()-1])
except:
    if metar[re.search(pattern_temp, metar).start()] == 'M':
        temp = int(metar[re.search(pattern_temp, metar).start()+2 : re.search(pattern_temp, metar).start()+4]) * (-1)
    else:
        temp = int(metar[re.search(pattern_temp, metar).start()+1 : re.search(pattern_temp, metar).start()+3])
    if metar[re.search(pattern_temp, metar).end()-3] == 'M':
        due = int(metar[re.search(pattern_temp, metar).end()-3 : re.search(pattern_temp, metar).end()-1]) * (-1)
    else:
        due = int(metar[re.search(pattern_temp, metar).end()-3 : re.search(pattern_temp, metar).end()-1])



# temp2, due2
try:
    if wx2[re.search(pattern_temp, wx2).start()] == 'M':
        temp2 = int(wx2[re.search(pattern_temp, wx2).start()+2 : re.search(pattern_temp, wx2).start()+4]) * (-1)
    else:
        temp2 = int(wx2[re.search(pattern_temp, wx2).start()+1 : re.search(pattern_temp, wx2).start()+3])
    if wx2[re.search(pattern_temp, wx2).end()-3] == 'M':
        due2 = int(wx2[re.search(pattern_temp, wx2).end()-3 : re.search(pattern_temp, wx2).end()-1]) * (-1)
    else:
        due2 = int(wx2[re.search(pattern_temp, wx2).end()-3 : re.search(pattern_temp, wx2).end()-1])
except:
    if metar2[re.search(pattern_temp, metar2).start()] == 'M':
        temp2 = int(metar2[re.search(pattern_temp, metar2).start()+2 : re.search(pattern_temp, metar2).start()+4]) * (-1)
    else:
        temp2 = int(metar2[re.search(pattern_temp, metar2).start()+1 : re.search(pattern_temp, metar2).start()+3])
    if metar2[re.search(pattern_temp, metar2).end()-3] == 'M':
        due2 = int(metar2[re.search(pattern_temp, metar2).end()-3 : re.search(pattern_temp, metar2).end()-1]) * (-1)
    else:
        due2 = int(metar2[re.search(pattern_temp, metar2).end()-3 : re.search(pattern_temp, metar2).end()-1])



# pressure
try:
    pres = float(wx1[re.search(pattern_pres, wx1).start()+1 : re.search(pattern_pres, wx1).start()+5])/100
except:
    pres = float(metar[re.search(pattern_pres, metar).start()+1 : re.search(pattern_pres, metar).start()+5])/100



# pressure2
try:
    pres2 = float(wx2[re.search(pattern_pres, wx2).start()+1 : re.search(pattern_pres, wx2).start()+5])/100
except:
    pres2 = float(metar2[re.search(pattern_pres, metar2).start()+1 : re.search(pattern_pres, metar2).start()+5])/100



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



# additional arrival airport info
print('\n\n- Arrival Information')

input_temp2 = input('  Arrival Airport Temperature [##] : ')
print ('\033[1A' + '\033[K')
while True :
    if len(input_temp2) == 0:
        print(f'  Arrival Airport Temperature [##] : {temp2}')
        break
    else:
        temp2 = float(input_temp2)
        print(f'  Arrival Airport Temperature [##] : {temp2}')
        break

input_due2 = input('  Arrival Airport Due point [##] : ')
print ('\033[1A' + '\033[K')
while True :
    if len(input_due2) == 0:
        print(f'  Arrival Airport Due point [##] : {due2}')
        break
    else:
        due2 = float(input_due2)
        print(f'  Arrival Airport Due point [##] : {due2}')
        break

input_pres2 = input('  Arrival Airport Altimeter Setting [##.##] : ')
print ('\033[1A' + '\033[K')
while True :
    if len(input_pres2) == 0:
        print(f'  Arrival Airport Altimeter Setting [##.##] : {pres2}')
        break
    else:
        pres2 = float(input_pres2)
        print(f'  Arrival Airport Altimeter Setting [##.##] : {pres2}')
        break
#input_temp2 = float(input('  Arrival Airport Temperature [##] : '))
#input_due2 = float(input('  Arrival Airport Due point [##] : '))
#input_pres2 = float(input('  Arrival Airport Altimeter Setting [##.##] : '))
print('\n-------------------------------------------------------------------------------------\n')






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
    headwind = abs(round(headwind,1))
    crosswind = np.sin(abs(int(wind_dir) - active_rwy_heading[0]) * np.pi/180) * float(wind_vel)
    crosswind = abs(round(crosswind,1))

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
    headwind2 = abs(round(headwind2,1))
    crosswind2 = np.sin(abs(int(wind_dir2) - active_rwy_heading2[0]) * np.pi/180) * float(wind_vel2)
    crosswind2 = abs(round(crosswind2,1))
print('\n-------------------------------------------------------------------------------------\n')





""" Weight & Balance """
print('< Weight and Balance > \n')
# arm은 기종에 따라 달라지도록
basic_empty_weight = cs_df['BEW'][0]
basic_empty_arm = cs_df['CG'][0]
basic_empty_moment = cs_df['BEW Moment'][0]
basic_empty = pd.DataFrame({'Weight' : basic_empty_weight, 'Arm' : basic_empty_arm, 'Moment' : basic_empty_moment}, index = ['Basic Empty Weight'])

pilot_weight = float(input('Pilot and Passenger Weight : '))
pilot_arm = 80.5
pilot_moment = pilot_weight * pilot_arm
pilot = pd.DataFrame({'Weight' : pilot_weight, 'Arm' : pilot_arm, 'Moment' : pilot_moment}, index = ['Pilot and Passenger'])

passenger_weight = float(input('Rear Passenger Weight : '))
passenger_arm = 118.1
passenger_moment = passenger_weight * passenger_arm
passenger = pd.DataFrame({'Weight' : passenger_weight, 'Arm' : passenger_arm, 'Moment' : passenger_moment}, index = ['Rear Passenger'])

baggage_a_weight = float(input('Baggage Weight : '))
baggage_a_arm = 142.8
baggage_a_moment = baggage_a_weight * baggage_a_arm
baggage_a = pd.DataFrame({'Weight' : baggage_a_weight, 'Arm' : baggage_a_arm, 'Moment' : baggage_a_moment}, index = ['Baggage'])

baggage_b_weight = 0
baggage_b_arm = 0
baggage_b_moment = baggage_b_weight * baggage_b_arm
# baggage_b = pd.DataFrame({'Weight' : baggage_b_weight, 'Arm' : baggage_b_arm, 'Moment' : baggage_b_moment}, index = ['Baggage B'])

zero_fuel_weight = basic_empty_weight + pilot_weight + passenger_weight + baggage_a_weight + baggage_b_weight
zero_fuel_moment = basic_empty_moment + pilot_moment + passenger_moment + baggage_a_moment + baggage_b_moment
zero_fuel_arm = round(zero_fuel_moment / zero_fuel_weight, 1)
zero_fuel = pd.DataFrame({'Weight' : zero_fuel_weight, 'Arm' : zero_fuel_arm, 'Moment' : zero_fuel_moment}, index = ['Zero Fuel Weight'])

fuel_100ll = 6
fuel_volume = input('Fuel [gal] : ')
print ('\033[1A' + '\033[K')
while True :
    if len(fuel_volume) == 0:
        fuel_volume = 48
        print(f'Fuel [gal] : {fuel_volume}')
        break
    else:
        fuel_volume = float(fuel_volume)
        print(f'Fuel [gal] : {fuel_volume}')
        break

fuel_weight = fuel_volume * fuel_100ll    
fuel_arm = 95
fuel_moment = fuel_weight * fuel_arm
fuel = pd.DataFrame({'Weight' : fuel_weight, 'Arm' : fuel_arm, 'Moment' : fuel_moment}, index = ['Fuel'])

ramp_weight = zero_fuel_weight + fuel_weight
ramp_moment = zero_fuel_moment + fuel_moment 
ramp_arm = round(ramp_moment / ramp_weight, 1)
ramp = pd.DataFrame({'Weight' : ramp_weight, 'Arm' : ramp_arm, 'Moment' : ramp_moment}, index = ['Ramp Weight'])

start_weight = -8
start_arm = 95
start_moment = start_weight * start_arm
start = pd.DataFrame({'Weight' : start_weight, 'Arm' : start_arm, 'Moment' : start_moment}, index = ['Start/Taxi/Run-up'])

takeoff_weight = ramp_weight + start_weight
takeoff_moment = ramp_moment + start_moment
takeoff_arm = round(takeoff_moment / takeoff_weight, 1)
takeoff = pd.DataFrame({'Weight' : takeoff_weight, 'Arm' : takeoff_arm, 'Moment' : takeoff_moment}, index = ['Takeoff Weight'])

fuel_to_use = float(input('Fuel Burn [gal] : '))
fuel_burn_volume = (-1) * fuel_to_use
fuel_burn_weight = fuel_burn_volume * fuel_100ll
fuel_burn_arm = 95
fuel_burn_moment = fuel_burn_weight * fuel_burn_arm
fuel_burn = pd.DataFrame({'Weight' : fuel_burn_weight, 'Arm' : fuel_burn_arm, 'Moment' : fuel_burn_moment}, index = ['Fuel Burn'])

landing_weight = takeoff_weight + fuel_burn_weight
landing_moment = takeoff_moment + fuel_burn_moment
landing_arm = landing_moment / landing_weight
landing = pd.DataFrame({'Weight' : landing_weight, 'Arm' : landing_arm, 'Moment' : landing_moment}, index = ['Landing Weight'])


takeoff_data = pd.concat([basic_empty, pilot, passenger, baggage_a, zero_fuel, fuel, ramp, start, takeoff, fuel_burn, landing])
print('\n\n')
print(takeoff_data)
print('\n-------------------------------------------------------------------------------------\n')





""" takeoff data """

print('< Takeoff Data > \n')
print('Current Time : ' + str(datetime.utcnow()) + '\n')

wx = pd.DataFrame({'issue(Z)' : issue_time,
                    'time' : time,
                    'airport' : arpt,
                    'wind' : wind_dir + wind_vel,
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
                    'wind' : wind_dir2 + wind_vel2,
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
print('\n\n')






""" V Speed """

vs0 = 45
vs1 = 50
vr = round(((takeoff_weight / 2550)**(1/2)) * 60, 1)
vr_short = round(((takeoff_weight / 2550)**(1/2)) * 55, 1)
vx = 64
cruise_climb_v = 87
vlo = 'X'
vy = 76
vfe = 102
v_man = round(((landing_weight/2550)**(1/2))*113, 1)
vno = 125
vle = 'X'
vne = 154
vg_to = round(((takeoff_weight/2550)**(1/2))*76, 1)
vg_ld = round(((landing_weight/2550)**(1/2))*76, 1)
va = round(((landing_weight/2550)**(1/2))*66, 1)
maxwind = 17

vspeed = pd.DataFrame({'Vso' : vs0,
                       'Vs1' : vs1,
                       'Vr' : vr,
                       'Vr - Short Field' : vr_short,
                       'Vx' : vx,
                       'Vy' : vy,
                       'Vfe' : vfe,
                       'Va' : v_man,
                       'Vno' : vno,
                       'Vne' : vne,
                       'takeoff Vg' : vg_to,
                       'landing Vg' : vg_ld,
                       'Approach Speed' : va,
                       'Max. Crosswind' : maxwind,
                       'Cruise Climb' : cruise_climb_v,
                       'Vlo' : vlo,
                       'Vle' : vle
                       }, index = ['Speed'])
print(vspeed.T)
print('\n-------------------------------------------------------------------------------------\n')




print('<ICAO Flight Plan information>\n')
print('7  -  Aircraft ID : ' + cs_df['ID'][0])
print('8  -  FLight Plan : I')
print('      Type of Flight : G')
print('9  -  Number : 1')
print('      Type of Aircraft : PA28')
print('      Wake Turbulence : F/L')
print('10 -  Equipment : ' + cs_df['Equip'][0])
print('      SURV : ' + cs_df['SURV'][0])
print('18 -  Other : B2')


print('\n-------------------------------------------------------------------------------------\n')
print('CREDITS \n ============ \n\n Sanghyok Han \n\n ============ \n\n')





""" import to flightplan.xlsx """
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = True
wb = excel.Workbooks.Open('C:/Users/user/proj/flight/result/flightplan.xlsx')
ws = wb.Worksheets('takeoff_data')
ws2 = wb.Worksheets('flight_planning')

ws.Cells(3, 2).Value = cs

#ws.Cells(1, 2).Value = issue_time
#ws.Cells(2, 2).Value = time
#ws.Cells(3, 2).Value = arpt
if gust == '0':
    ws.Cells(5, 4).Value = wind_dir + wind_vel
elif gust == 'X':
    ws.Cells(5, 4).Value = wind_dir + wind_vel
else:
    ws.Cells(5, 4).Value = wind_dir + wind_vel + 'G' + gust
ws.Cells(6, 4).Value = vis
ws.Cells(8, 4).Value = cig
ws.Cells(10, 4).Value = str(temp) + '/' + str(due)
ws.Cells(11, 4).Value = pres
ws.Cells(13, 4).Value = active_rwy
ws.Cells(17, 4).Value = pa
ws.Cells(18, 4).Value = da
ws.Cells(20, 4).Value = str(active_rwy_length)
ws.Cells(22, 4).Value = headwind
ws.Cells(23, 4).Value = crosswind

#ws.Cells(1, 3).Value = issue_time2
#ws.Cells(2, 3).Value = time2
#ws.Cells(3, 3).Value = arpt2
if gust2 == '0':
    ws.Cells(5, 7).Value = wind_dir2 + wind_vel2
elif gust2 == 'X':
    ws.Cells(5, 7).Value = wind_dir2 + wind_vel2
else:
    ws.Cells(5, 7).Value = wind_dir2 + wind_vel2 + 'G' + gust2
ws.Cells(6, 7).Value = vis2
ws.Cells(8, 7).Value = cig2
ws.Cells(10, 7).Value = str(temp2) + '/' + str(due2)
ws.Cells(11, 7).Value = pres2
ws.Cells(13, 7).Value = active_rwy2
ws.Cells(17, 7).Value = pa2
ws.Cells(18, 7).Value = da2
ws.Cells(20, 7).Value = str(active_rwy_length2)
ws.Cells(22, 7).Value = headwind2
ws.Cells(23, 7).Value = crosswind2

ws.Cells(30, 2).Value = vs0
ws.Cells(31, 2).Value = vs1
ws.Cells(33, 2).Value = str(vr) + '/' + str(vr_short)
ws.Cells(35, 2).Value = vx
ws.Cells(36, 2).Value = vlo
ws.Cells(30, 5).Value = vy
ws.Cells(31, 5).Value = vfe
ws.Cells(33, 5).Value = v_man
ws.Cells(35, 5).Value = vno
ws.Cells(36, 5).Value = vle
ws.Cells(30, 8).Value = vne
ws.Cells(31, 8).Value = str(vg_to) + '/' + str(vg_ld)
ws.Cells(33, 8).Value = va
ws.Cells(35, 8).Value = maxwind
ws.Cells(36, 8).Value = cruise_climb_v
#ws.Cells(20, 5).Value = 


ws.Range("L3:N3").Value = basic_empty.values
ws.Range("L4:N4").Value = pilot.values
ws.Range("L5:N5").Value = passenger.values
ws.Range("L7:N7").Value = baggage_a.values
ws.Range("L9:N9").Value = zero_fuel.values
ws.Range("L12:N12").Value = fuel.values
ws.Range("L14:N14").Value = ramp.values
ws.Range("L16:N16").Value = start.values
ws.Range("L19:N19").Value = takeoff.values
ws.Range("L30:N30").Value = fuel_burn.values
ws.Range("L32:N32").Value = landing.values


# print(ws.Cells(1,1).Value)
#wb.Close(True)    #wb.SaveAs('C:/Users/user/proj/flight/result/flightplan.xlsx')
#excel.Quit()
