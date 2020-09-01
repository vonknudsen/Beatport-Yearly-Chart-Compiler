import os
import csv
import requests
from lxml import html
import calendar
import sqlite3
from datetime import datetime
import pandas as pd
import time

#Examples of what is needed in for the code to run:
"""
genre = "\\House" #The Genre Directory you want it to go in.
year = 2017
username = "my_username"
password = "my_password"
"""

genre_dict = { "\\Top-100" : ["Global","/global/"],
              "\\Afro-House": ["Afro House","/afro-house/"],
              "\\Bass-House": ["Bass House","/bass-house/"],
              "\\Big-Room":["Big Room,""/big-room/"],
              "\\Breaks":["Breaks","/breaks/"],
              "\\Dance" :  ["Dance","/dance/"],
              "\\House" : ["House", "/house/" ],
              "\\Deep-House" :  ["Deep House","/deep-house/"],
              "\\DJ-Tools" :  ["DJ Tools","/dj-tools/"],
              "\\Drum-Bass" :  ["Drum & Bass", "/drum-and-bass/"],
              "\\Dubstep" :  ["Dubstep" , "/dubstep/"],
              "\\Electro-House" :  ["Electro House", "/electro-house/"],
              "\\Electronica-Downtempo" :  ["Electronica / Downtempo", "/electronica-downtempo/"] ,
              "\\Funky-Groove-Jackin-House" :  ["Funky / Groove / Jackin' House", "/funky-groove-jackin-house/"],
              "\\Future-House" :  ["Future House", "/future-house/"],
              "\\Garage-Bassline-Grime": ["Garage / Bassline / Grime","/garage-bassline-grime/"],
              "\\Hard-Dance-Hardcore" :  ["Hard Dance / Hardcore", "/hard-dance-hardcore/" ],
              "\\Hard-Techno" :  ["Hard Techno", "/hard-techno/"],
              "\\Hip-Hop-R-B" : ["Hip Hop / R&B", "/hip-hop-r-and-b/"],
              "\\Indie-Dance":["Indie Dance","/indie-dance/"],
              "\\Leftfield-Bass":["Leftfield Bass","/leftfield-bass/"],
              "\\Leftfield-House-Techno":["Leftfield House & Techno","/leftfield-house-techno/"],
              "\\Melodic-House-Techno":["Melodic House & Techno","/melodic-house-and-techno/"],
              "\\Minimal-Deep-Tech":["Minimal / Deep Tech","/minimal-deep-tech/"],
              "\\Nu-Disco-Disco":["Nu Disco / Disco","/nu-disco-disco/"],
              "\\Progressive-House":["Progressive House","/progressive-house/"],
              "\\Psy-Trance":["Psy-Trance","/psy-trance/"],
              "\\Reggae-Dancehall-Dub":["Reaggae / Dancehall / Dub","/reggae-dancehall-dub/"],
              "\\Tech-House":["Tech House","/tech-house/"],
              "\\Techno" : ["Techno" , "/techno/"],
              "\\Trance" : ["Trance" , "/trance/"],
              "\\Trap-Future-Bass":["Trap / Future Bass","/trap-future-bass/"]
              }

def Initialize() : #Sets all necessary initial values.
    part1  = [("\nWe should start with the genre. This is the genre you want to download. I will print\n"
    + "out a list of genres, and you can pick (by typing in their code). \nPlease be careful to type in the correct code! \n\n")]
    part2 = [genredet[0] + " - "+ str(indexno) + "\n" for indexno,genredet in enumerate(genre_dict.values())]
    part3 = ["\n\nWhat genre are we dealing with?\n\n"]
    genre_input = input(str.join("",part1+part2+part3))
    year = input(("\n\nWhat year are these charts from?\n\n"))
    username = input(("\n\nLogin Details:\n\nType in your email and press enter\n\n"))
    password = input(("\n\nType in your password and press enter\n\n"))
    resume = input(("\nThanks for all the info. I will now try my best! The time I take is largely dependent on network speed, \nso thanks "
    + "in advance for your patience.\nPress Enter to continue or if you think you made a mistake, we can start again, simply press R.\n\n"))
    if resume.lower() == "r":
        return Initialize()
    else:
        return (int(year), list(genre_dict.keys())[int(genre_input)],username,password)


def FilePathAndURLGeneration(genre,year):
    bpurl = "https://www.bptoptracker.com/top/track"
    toplevelpath = "C:\ProgramData\BeatportData\\"+str(year)+genre+"\\Data"
    fileinfodict = {}
    daysinmonth = lambda x : calendar.monthrange(year,x)[1]
    for month in range(1,13):
        for day in range(1,daysinmonth(month)):
            ymd = "{}-{}-{}".format(year,month,day)
            url = bpurl+genre_dict[genre][1]+ymd
            filepath = toplevelpath+"\\D"+ymd+".csv"
            fileinfodict[filepath] = {'url':url,
                                  'date':datetime.strptime(ymd,"%Y-%m-%d")}
    return fileinfodict

def LoginAndDownloadFiles(genre,year,email,password,fileinfodict):    
    session_requests = requests.session()
    login_url = 'https://www.bptoptracker.com/login'
    result = session_requests.get(login_url)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='_token']/@value")))[0]
    payload = {'email':email,
               'password':password,
               '_token':authenticity_token}
    result = session_requests.post(
        login_url,
        data=payload,
        headers = dict(referer=login_url))
    data_present = False
    toplevelpath = "C:\ProgramData\BeatportData\\"+str(year)+genre+"\\Data"
    dbpath = toplevelpath+"\\Charts_Year.db"
    cols = ["Unnamed: 0","Title", "Artists", "Genre","Label", "Released"]
    colsrename = ["Chart Position","Title", "Artists", "Genre","Label", "Released"]
    dbcon = sqlite3.connect(dbpath)
    for filepath,info in fileinfodict.items():
        trytimes = 0 ; trylimit = 500
        connection_made= False
        result = None
        while (trytimes < trylimit) and (connection_made == False) :
            try:
                result = session_requests.get(
                            info['url'], 
                            headers = dict(referer = info['url'])
                            )
                connection_made = True
            except requests.exceptions.ConnectionError:
                time.sleep(2)
                trytimes = trytimes + 1                
                
        if not type(result) is type(None):
            try:
                pandas_read = pd.read_html(result.content)
                table_present = True
                data_present = True
            except ValueError:
                table_present = False
            if table_present:
                chart = pandas_read[0].loc[:,cols]
                chart.columns = colsrename
                chart.loc[:,'Chart Date'] = datetime.strftime(info['date'],"%Y-%m-%d")
                chart.to_sql(genre_dict[genre][0],dbcon,index=False,if_exists="append")
                chart.to_csv(filepath,index=False,mode="w+",
                             quoting=csv.QUOTE_ALL)

    dbcon.close()
            
    if not data_present:
        os.remove(dbpath)
        os.rmdir(toplevelpath)
        os.rmdir("C:\ProgramData\BeatportData\\"+str(year)+genre)
        return None
    
    if data_present:
        return dbpath

    
def RankedYearlyChart(dbpath,genre,year):
    if not type(dbpath) is type(None):
        genrename = genre_dict[genre][0]
        csvpath = ("C:\ProgramData\BeatportData\\"+str(year)+genre+"\\"+genrename+
                   " in "+str(year)+".csv")
        txtpath = ("C:\ProgramData\BeatportData\\"+str(year)+genre+"\\"+genrename+
                   " in "+str(year)+".txt")
        dbcon = sqlite3.connect(dbpath)
        sqlforrankedchart = """SELECT 
                            	SUM(101-"Chart Position") "Points",
                                "Title",
                                "Artists",
                                "Genre",
                                "Label"
                            FROM "%s"
                            GROUP BY "Title","Artists","Genre","Label"
                            ORDER BY "Points" DESC;""" % (genrename,)
        rankedchart = pd.read_sql(sqlforrankedchart,dbcon)
        rankedchart.loc[:,"Rank"] = [x+1 for x in rankedchart.index]
        rankedchart = rankedchart.loc[:,["Rank","Points","Title",
                                         "Artists","Genre","Label"]]
        rankedchart.to_csv(csvpath,index=False,mode="w+",quoting=csv.QUOTE_ALL)
        rankedchart.to_csv(txtpath,index=False,mode="w+",sep="=",
                           quoting=csv.QUOTE_NONE,header=False)
    return dbpath



def Finalize(dbstatus,year,genre):
    if type(dbstatus) is type(None):
        input(("\n\nUnfortunately there was no data for the genre in that year.\n\n"
                + "Thanks for giving the program a whirl. Press enter to exit."))

    if not type(dbstatus) is type(None):
        input(("\n\nThe process is finally done! The sorted and ranked charts have been outputted as a .txt file in "
                + "C:ProgramData\BeatportData\Year\Genre.\nIt is called Genre in 20XX.txt.\nAlso stored is a csv of the same.\n "
                + "\n\n\nOn the structure "
                +"of the main file, each line is read as such:\nRank=Total Points=Title=Artist=Label   seperated by equal signs.\n"
                + "Thanks for giving the program a whirl. Press enter to exit."))
                
        os.system("start explorer.exe " + "C:\ProgramData\BeatportData" + "\\" + str(year) + "\\" + genre[1:])
                    
def EndToEndRun():
    in_year,in_genre,in_mail,in_pass = Initialize()
    os.makedirs("C:\ProgramData\BeatportData" + "\\" + str(in_year)+in_genre)
    os.makedirs("C:\ProgramData\BeatportData"+"\\"+str(in_year)+in_genre +"\Data")
    in_fileinfodict = FilePathAndURLGeneration(in_genre,in_year)
    in_dbpath = LoginAndDownloadFiles(in_genre,in_year,
                                      in_mail,in_pass,in_fileinfodict)
    RankedYearlyChart(in_dbpath,in_genre,in_year)
    Finalize(in_dbpath,in_year,in_genre)
    return True

os.system("mode con: cols=150 lines=40")
EndToEndRun()