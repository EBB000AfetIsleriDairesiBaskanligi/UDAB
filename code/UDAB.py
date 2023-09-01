import os
import requests
from time import sleep
from bs4 import BeautifulSoup
from gtts import gTTS
import folium
import webbrowser
import variables

def startMessages():
    print(variables.startMsg)
    print(variables.firstConnectMsg)
    sleep(3)
    print(variables.controlMsg)
    sleep(3)

def mapProcesses(coordinates, attention):
    map_center = coordinates
    my_map = folium.Map(location=map_center, zoom_start=13)
    marker_1 = folium.Marker(location=coordinates, popup=attention)
    my_map.add_child(marker_1)
    my_map.save(variables.exportMapFile)
    webbrowser.open_new_tab(variables.exportMapFile)

def takeDataWithScrapping():
    response = requests.get(variables.url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find(variables.scrappingTag)

def setDataLinesFromScrapping(pre_tag):
    earthquake_data = pre_tag.get_text()
    keyword = variables.cutScrappingDataKeyword
    keyword_index = earthquake_data.index(keyword)
    return earthquake_data[keyword_index + len(keyword):]

def openVoiceFile(fileName):
    os.system(f"start {fileName}")
    sleep(3)

def createVoiceFile(message, voiceType):
    tts = gTTS(message, lang=variables.languageCode, slow=True)
    tts.save(voiceType)

def printMessagesForSuccess():
    print(variables.controlSuccessMsg)
    print(variables.controlAgain)
    sleep(30)

def setDictionaryForEarthquakeData(line):
    columns = line.split()
    date = columns[0]
    time = columns[1]
    latitude = columns[2] # enlem
    longitude = columns[3] # boylam
    depth = columns[4]
    MD = columns[5]
    ML = columns[6]
    Mw = columns[7]
    area = columns[8]
    other = " ".join(columns[9:])
    return {
        "date": date, 
        "time": time, 
        "latitude": latitude, 
        "longitude": longitude,
        "depth": depth,
        "MD":MD,
        "ML":ML,
        "Mw": Mw,
        "area": area,
        "other": other
        }

def importantEarthquake(coordinates, attention):
    mapProcesses(coordinates, attention) 
    createVoiceFile(variables.alertMsg, variables.exportAlertVoice)
    voiceAgain=0
    while voiceAgain<3:
        openVoiceFile(variables.exportAlertVoice)
        sleep(3)
        voiceAgain+=1

def app():
    try:
        controlNo = 0
        earthquakeInfo = None
        while True:
            pre_tag = takeDataWithScrapping()
            if pre_tag:
                lines = setDataLinesFromScrapping(pre_tag).strip().split('\n')
                for line in lines[1:2]:
                    lastEarthquake = setDictionaryForEarthquakeData(line)
                    attention = f"Tarih: {lastEarthquake['date']} ==> {lastEarthquake['area']} bölgesinde {lastEarthquake['ML']} büyüklüğünde ve {lastEarthquake['depth']}km derinliğinde deprem oldu."
                    if earthquakeInfo != attention:
                        earthquakeInfo = attention
                        print(f"Kontrol No: {controlNo+1}" ,attention)
                        if float(lastEarthquake['ML']) > 1:
                            coordinates = [lastEarthquake['latitude'], lastEarthquake['longitude']]
                            importantEarthquake(coordinates, attention)
                        else: pass
                    else: print(f"Kontrol No: {controlNo+1} Yeni Deprem Bilgisi Bulunmamakta.")    
                printMessagesForSuccess()
            else:
                print(variables.dataScrappingErrorMsg)
            controlNo+= 1
    except :
        print(variables.bannedMsg)
        createVoiceFile(variables.bannedMsg, variables.exportBannedVoice)
        y=0
        while y<2:
            openVoiceFile(variables.exportBannedVoice)
            y+=1

startMessages()
app()
