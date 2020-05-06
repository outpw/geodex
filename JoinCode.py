import pandas as pd
import glob, os
import geopandas 

os.getcwd()

workDirect = 'D:\ForPhil\\'
savePath = 'results\\'
workPath = 'data\\' #place the unjoined sanborn maps within 
workPathCSV = 'SanbornCSV\\'
os.chdir(workDirect + workPath)

sanbornList = []
csvList = []
try:
    os.mkdir(workDirect + "results")
except:
    print "results folder already created"

print ("gathering files into a list") 
for file in glob.glob("*.geojson"):
    sanbornList.append(file)
os.chdir(workDirect + workPathCSV)

for file in glob.glob("*.csv"):
    csvList.append(file)

os.chdir(workDirect + savePath)


print ("conducting the join") 
csvName = ''
volumeName = ''

for i in sanbornList:
    sanbornName = i.split('.')
#for volumes the dot gets eliminated
    if len(sanbornName) == 3:
        volumeName = sanbornName[0] + '.' + sanbornName[1]
        volumeName = volumeName.split('_')
#continuting with creating names to match csv with geojson
    sanbornName = sanbornName[0].split('_')
    
    if len(sanbornName) == 4: #towns with two names
        sanbornName = sanbornName[1] + sanbornName[2] + sanbornName[3]
        
    elif len(sanbornName) == 3: #towns with one name
        sanbornName = sanbornName[1] + sanbornName[2]
        
    if len(volumeName) == 4: #towns with one name and a volume 
        volumeName = volumeName[1] + volumeName[2] + volumeName[3] + '.csv'

    elif len(volumeName) == 5: #towns with two names and a volume 
        # hopefully they name all their volumes like this because its missing the "_meta" so I can't Split
        volumeName = volumeName[1] + volumeName[2] + volumeName[3] + volumeName[4] + '.csv'   
    for z in csvList:
        csvName = z.split('_')
        csvName = csvName[0]
        if sanbornName == csvName:
            jsonJoin = geopandas.read_file(workDirect + workPath + i)
            jsonJoin = jsonJoin.rename(columns = {'Sheet Number':'sheet number'})
            jsonJoin = jsonJoin.rename(columns = {'Set Title':'Set_Title'})
            
            csvJoin = pd.read_csv(workDirect + workPathCSV + z)
            try:
                join_json_csv = jsonJoin.merge(csvJoin, on = 'sheet number')
                join_json_csv.to_file(i, driver = 'GeoJSON')
                print ("Joining", i, "and", z)
            except:
                join_json_csv = jsonJoin.merge(csvJoin, on = 'sheet number')
                
                print ("Did not join", i, "and", z)
        elif volumeName == csvName:
            jsonJoin = geopandas.read_file(workDirect + workPath + i)
            jsonJoin = jsonJoin.rename(columns = {'Sheet Number':'sheet number'})
            csvJoin = pd.read_csv(workDirect + workPathCSV + z)
            join_json_csv = jsonJoin.merge(csvJoin, on = 'sheet number')
            join_json_csv.to_file(i, driver = 'GeoJSON')
            print ("Joining", i, "and", z)
            volumeName = ''
            
    print ("\n")
    