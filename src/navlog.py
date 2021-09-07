#import wb
import re
import pandas as pd
import numpy as np
import win32com.client
from os import system, path
from selenium import webdriver





def wca(tc, tas, wind_dir, wind_vel):
    alpha = tc
    beta = wind_dir
    sigma = alpha - (180 + beta)
    theta = np.arcsin(wind_vel / tas * np.sin(sigma / 180 * np.pi)) / np.pi * 180
    wca = theta
    th = alpha + theta
    return wca, th





"""
wb.time
wb.arpt1
wb.arpt2
wb.ac
timeoff = wb.time.hour + wb.time.minute
alt = input('')
dist = 

ias_climb1 = 
ias_climb2 = 
ias_cruise1 =

temp_climb1 = ****
temp_climb2 = 
alt_climb1 = ****
alt_climb2 = 

cas_climb1 = 78    # pa28 ****
cas_climb2 = 78    # pa28 ****

tas_climb1 = 
tas_climb2 = 
tas_cruise1 =
tas_cruise2 =  

wb.fuel_volume
gph = 
fuel_time = pd.to_datetime(str(round(wb.fuel_volume / gph,2)), unit='h')    # .hour, .minute만 쓰면 될듯

variation = 
deviation = ?
"""


print('----------------------------------------------------------------------\n\n\n')

#system('cls')
print('< Navigation Log>')
alt_cruise = float(input('\n\nCruise Altitude : '))
alt_climb = alt_cruise / 2
variation = float(input('\nMagetic Variation [ -E / +W ]: '))
tas = float(input('\nCruise TAS : '))




""" wintemp """

# load data
print('\n\n\n< Wind/Temp >')
options = webdriver.ChromeOptions()
options.add_argument("headless")
wintemp_url = 'https://www.aviationweather.gov/windtemp/data?region=mia'
driver = webdriver.Chrome(options=options)
driver.get(wintemp_url)
try:
    wintemp = driver.find_element_by_xpath("//*[@id='awc_main_content_wrap']/pre")
    wintemp = str(wintemp.text)
except:
    wintemp = ''

print ('\033[1A' + '\033[K')
print(wintemp + '\n')

print('METAR')
#print(wb.metar)    #############################################################################################
print('KSFB 070853Z AUTO 00000KT 10SM CLR 24/24 A2994 RMK AO2 SLP137 T02390239 55006')



# data input
pattern_wintemp = 'MLB\s[0-9][0-9][0-9][0-9]|MLB\s[0-9][0-9][0-9][0-9]...'
regex = re.compile(pattern_wintemp)
search = regex.search(wintemp)
temp_temp = float(wintemp[re.search(pattern_wintemp, wintemp).start()+14 : re.search(pattern_wintemp, wintemp).start()+16])
temp_wind_dir = float(wintemp[re.search(pattern_wintemp, wintemp).start()+4 : re.search(pattern_wintemp, wintemp).start()+6]) * 10
temp_wind_vel = float(wintemp[re.search(pattern_wintemp, wintemp).start()+6 : re.search(pattern_wintemp, wintemp).start()+8])
wintemp_dir_3000 = float(wintemp[re.search(pattern_wintemp, wintemp).start()+4 : re.search(pattern_wintemp, wintemp).start()+6]) * 10
wintemp_vel_3000 = float(wintemp[re.search(pattern_wintemp, wintemp).start()+6 : re.search(pattern_wintemp, wintemp).start()+8])
wintemp_dir_6000 = float(wintemp[re.search(pattern_wintemp, wintemp).start()+9 : re.search(pattern_wintemp, wintemp).start()+11]) * 10
wintemp_vel_6000 = float(wintemp[re.search(pattern_wintemp, wintemp).start()+11 : re.search(pattern_wintemp, wintemp).start()+13])
wintemp_dir_9000 = float(wintemp[re.search(pattern_wintemp, wintemp).start()+17 : re.search(pattern_wintemp, wintemp).start()+19]) * 10
wintemp_vel_9000 = float(wintemp[re.search(pattern_wintemp, wintemp).start()+19 : re.search(pattern_wintemp, wintemp).start()+21])
if wintemp_vel_3000 == 0:
    wintemp_dir_3000 == 0
if wintemp_vel_6000 == 0:
    wintemp_dir_6000 == 0
if wintemp_vel_9000 == 0:
    wintemp_dir_9000 == 0



# climb temperature
if alt_climb < 6000:
    temp_temp = temp_temp + ((6000 - alt_climb) / 1000 * 2)
elif alt_climb == 6000:
    temp_temp = temp_temp
else:
    temp_temp = temp_temp - ((6000 - alt_climb) / 1000 * 2)

print(f'\nClimb Temperature based on WinTemp = {temp_temp}')
temp_climb = input('Climb Temperatire : ')
if len(temp_climb) == 0:
    print ('\033[1A' + '\033[K')
    print(f'Climb Temperatire : {temp_temp}')
    temp_climb = temp_temp
else:
    temp_climb = float(temp_climb)



# climb pressure
pres1 = 29.89    # wb.pres1 
pres_climb_temp = pres1-(alt_climb/1000)
print(f'\nClimb QNH based on METAR = {pres_climb_temp}')
pres_climb = input('Climb QNH : ')
if len(pres_climb) == 0:
    print ('\033[1A' + '\033[K')
    print(f'Climb QNH : {pres_climb_temp}')
    pres_climb = pres_climb_temp
else:
    pres_climb = float(pres_climb)



# climb cas
cas_climb = input('Climb CAS : ')
if len(cas_climb) == 0:
    print ('\033[1A' + '\033[K')
    print(f'Climb CAS : 78')
    cas_climb = 78    # pa28
else:
    cas_climb = float(cas_climb)



# climb tas
tas_climb = round(cas_climb / (288.15/(temp_climb+273.15) * ((pres_climb / 100 * 33.8638866666667) / 1013.25)) ** (1/2) /10 , 1)
print('\nClimb TAS : '+ str(tas_climb))

print('----------------------------------------------------------------------\n\n\n')





"""  Checkpoints """
print('< Navlog >')
print('\n\nEnter Checkpoints from departing airport to the destination')
print('\nPress ENTER after the destination\n')

cp = 0
cp_df = pd.DataFrame()

while True:
    print('----------------------------------------------------------------------')
    cp = cp + 1
    temp_cp = input(f'\nCheckpoint {cp} : ').upper()

    if cp == 1:    # first checkpoint
        cp_df = cp_df.append(pd.DataFrame({'checkpoint' : temp_cp,
                                           'true_course' : 0,
                                           'wind_correction_angle' : 0,
                                           'true_heading' : 0,
                                           'magnetic_heading' : 0,
                                           'distance' : 0
                                            }, index = [0]))
                
        temp_dist = float(input('Distance to TOC [NM]: '))
        temp_crs = float(input('True Course to TOC [###]: '))

        first_ete = float(input('ETE to TOC [min] : '))                # datetime으로 바꿔야할지도
        first_fuel = float(input('Fuel consumption to TOC [gal] : '))

        if alt_climb <= 4500:
            wind_dir = wintemp_dir_3000
            wind_vel = wintemp_vel_3000
        elif (alt_climb > 4500) & (alt_climb <= 7500):
            wind_dir = wintemp_dir_6000
            wind_vel = wintemp_vel_6000
        else: # (alt_climb > 7500) & (alt_climb <= 10500):
            wind_dir = wintemp_dir_9000
            wind_vel = wintemp_vel_9000
        
        temp_wca = round(wca(temp_crs, tas_climb, wind_dir, wind_vel)[0], 0)
        temp_th = round(wca(temp_crs, tas_climb, wind_dir, wind_vel)[1], 0)
        temp_mh = temp_th + variation

        cp_df = cp_df.append(pd.DataFrame({'checkpoint' : 'TOC',
                                           'true_course' : temp_crs,
                                           'wind_correction_angle' : temp_wca,
                                           'true_heading' : temp_th,
                                           'magnetic_heading' : temp_mh,
                                           'distance' : temp_dist
                                            }, index = [cp]))
        print('\n')
    else: 
        if len(temp_cp) == 0:
            print ('\033[1A' + '\033[K')
            break
        else:
            temp_dist = input('Distance from last checkpoint : ')
            temp_dist = float(temp_dist)
            temp_crs = float(input('True course from last checkpoint [###]: '))

            if alt_cruise <= 4500:
                wind_dir = wintemp_dir_3000
                wind_vel = wintemp_vel_3000
            elif (alt_cruise > 4500) & (alt_cruise <= 7500):
                wind_dir = wintemp_dir_6000
                wind_vel = wintemp_vel_6000
            else: # (alt_cruise > 7500) & (alt_cruise <= 10500):
                wind_dir = wintemp_dir_9000
                wind_vel = wintemp_vel_9000
            
            temp_wca = round(wca(temp_crs, tas, wind_dir, wind_vel)[0], 0)
            temp_th = round(wca(temp_crs, tas, wind_dir, wind_vel)[1], 0)
            temp_mh = temp_th + variation

            cp_df = cp_df.append(pd.DataFrame({'checkpoint' : temp_cp,
                                               'true_course' : temp_crs,
                                               'wind_correction_angle' : temp_wca,
                                               'true_heading' : temp_th,
                                               'magnetic_heading' : temp_mh,
                                               'distance' : temp_dist
                                                }, index = [cp]))
            print('\n')

print(cp_df)




"""
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = True
fullpath = path.abspath('./flightplan.xlsx')
wb = excel.Workbooks.Open(fullpath)
ws3 = wb.Worksheets('flight_planning')
"""