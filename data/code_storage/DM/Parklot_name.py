from firebase import firebase
import json
import os

fb = firebase.FirebaseApplication('https://potent-result-406711-ebf47.asia-southeast1.firebasedatabase.app/', None)

if __name__ == "__main__":
    with open (os.getcwd()+'/info.json','r',encoding='utf-8') as f:
        file = json.load(f)
        i=0
        while(True):
            try:
                fb.put(f'PA/{file["CarParks"][i]["CarParkID"]}','name',file["CarParks"][i]["CarParkName"]["Zh_tw"])
                i+=1
            except IndexError:
                print('done')
                break
            except Exception as e:
                print(e)
                break