import json 
import os
import time
import pandas as pd
import re
from firebase import firebase
import datetime


class Colorfill:
    OK = "\033[92m"  # GREEN
    WARNING = "\033[93m"  # YELLOW
    FAIL = "\033[91m"  # RED
    RESET = "\033[0m"  # RESET COLOR


num_list = open(f'{os.getcwd()}//data//data_storage//Parklot_Available//raw_data//_0.txt',mode = 'r',encoding = 'utf-8').read().split('\n') 
num_list.remove('')
fb = firebase.FirebaseApplication('https://potent-result-406711-48d96.firebaseio.com', None)

def restruct(file_num):
    df = pd.read_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//raw_data//{file_num}.json')
    name = []
    spaces = []

    for i in range(len(df['ParkingAvailabilities'])):
            name.append(df['ParkingAvailabilities'][i]['CarParkName']['Zh_tw'].strip())
            spaces.append([df['ParkingAvailabilities'][i]['AvailableSpaces']])

    date = re.split('[T/+]',df.loc[i,'UpdateTime'])[0]
    week = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()+1
    clock = file_num.split('_')[3]
    #print(date)
    
    ############################################################################################################
    

    for location,lot_num in zip(name,spaces):
        #print(f"{location}:{week}_{clock}")
        #print(f"{location} {lot_num}")
        lot_num=lot_num[0]
        if(lot_num==-1):  # case with bad data
            try: 
                #fb.put(f'parklot_available/{location}/{week}-{clock}','current_space', -1)
                with open (f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//{location}.json','r+',encoding='utf-8') as f:
                    base_file = json.load(f)
                    base_file[f'{week}-{clock}'].update({'current_space':-1})
                    f.truncate(0)
                    f.seek(0)
                    json.dump(base_file,f)
                
                
            except Exception as e:
                print(f"{Colorfill.OK}New file_tick added: {Colorfill.WARNING}{location}|{week}-{clock}{Colorfill.RESET}//problem: {e}")
                try:
                    #fb.put(f'parklot_available/{location}/{week}-{clock}','current_space', -1)
                    with open(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//{location}.json','r+',encoding='utf-8') as f:
                        base_file = json.load(f)
                        base_file[f'{week}-{clock}']={"current_space": -1, "avg_space": 0, "dataset_quantity": 0}
                        f.truncate(0)
                        f.seek(0)
                        json.dump(base_file,f)
                    
                except Exception as e :
                    print(f"{Colorfill.OK}New location added: {Colorfill.WARNING}{location}{Colorfill.RESET}//problem: {e}")
                    #fb.put(f'parklot_available/{location}/{week}-{clock}','current_space', -1)
                    with open(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//{location}.json','r+',encoding='utf-8') as f:
                        base_file=dict()
                        base_file[f'{week}-{clock}']={"current_space": -1, "avg_space": 0, "dataset_quantity": 0}
                        f.truncate(0)
                        f.seek(0)
                        json.dump(base_file,f)
                    
                    #base_file = pd.DataFrame()
                    #base_file[f'{week}-{clock}'] = {'current_space': -1, 'avg_space': 0, 'dataset_quantity': 0}
                    
        
        else: ###########case with well data
            try:
                with open(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//{location}.json','r+',encoding='utf-8') as f:
                    base_file = json.load(f)
                    
                    base_file[f'{week}-{clock}'].update({'current_space': int(lot_num)})
                    base_file[f'{week}-{clock}'].update({'avg_space':(base_file[f'{week}-{clock}']['dataset_quantity']*base_file[f"{week}-{clock}"]["avg_space"]+lot_num)/(base_file[f"{week}-{clock}"]["dataset_quantity"]+1)})
                    base_file[f'{week}-{clock}'].update({'dataset_quantity':int(base_file[f'{week}-{clock}']['dataset_quantity']) + 1})
                    f.truncate(0)
                    f.seek(0)
                    json.dump(base_file,f)
                #fb.put(f'parklot_available/{location}/{week}-{clock}','current_space', lot_num)
                #fb.put(f'parklot_available/{location}/{week}-{clock}','avg_space',int(base_file[f'{week}-{clock}']['avg_space']))
                #fb.put(f'parklot_available/{location}/{week}-{clock}','dataset_quantity', int(base_file[f'{week}-{clock}']['dataset_quantity']))
            except Exception as e:
                print(f"{Colorfill.OK}New file_tick added: {Colorfill.WARNING}{location}|{week}-{clock}{Colorfill.RESET}//problem: {e}")
                try:
                    with open(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//{location}.json','r+',encoding='utf-8') as f:
                        base_file = json.load(f)
                        base_file[f"{week}-{clock}"]={"current_space": int(lot_num), "avg_space": int(lot_num), "dataset_quantity": 1}
                        f.truncate(0)
                        f.seek(0)
                        json.dump(base_file,f)

                    #fb.put(f'parklot_available/{location}/{week}-{clock}','current_space', int(lot_num))
                    #fb.put(f'parklot_available/{location}/{week}-{clock}','avg_space',int(base_file[f'{week}-{clock}']['avg_space']))
                    #fb.put(f'parklot_available/{location}/{week}-{clock}','dataset_quantity', int(base_file[f'{week}-{clock}']['dataset_quantity']))
                except Exception as e :
                    print(f"{Colorfill.OK}New location added: {Colorfill.WARNING}{location}{Colorfill.RESET}//problem: {e}")
                    with open (f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//{location}.json','r+',encoding='utf-8') as f:
                        base_file=dict()
                        base_file[f"{week}-{clock}"]={"current_space": int(lot_num), "avg_space": int(lot_num), "dataset_quantity": 1}
                        json.dump(base_file,f)
                    #fb.put(f'parklot_available/{location}/{week}-{clock}','current_space', int(lot_num))
                    #fb.put(f'parklot_available/{location}/{week}-{clock}','avg_space',int(base_file[f'{week}-{clock}']['avg_space']))
                    #fb.put(f'parklot_available/{location}/{week}-{clock}','dataset_quantity', int(base_file[f'{week}-{clock}']['dataset_quantity']))
    ############################################################################################################
    

if __name__ == '__main__':
    print(f"{Colorfill.FAIL}Working{Colorfill.RESET}")
    for i in num_list[0:3]:
        restruct(i)
    print(f"{Colorfill.OK}File {num_list[-1]} has been restructed.{Colorfill.RESET}")
    print(f"{Colorfill.OK}All files has been restructed.{Colorfill.RESET}")