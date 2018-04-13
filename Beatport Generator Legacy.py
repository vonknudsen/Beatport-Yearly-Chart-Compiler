""" NOTES : The time.sleep() are for the system to have time to slow down before the next phase"""
"""Use Invoke-WebRequest http://www.bptoptracker.com/top/dance/39/2016-02-02 -OutFile E:\Downloads\2016-02
-02.html instead of vivaldi"""

import os
from bs4 import BeautifulSoup
import csv
import time
import pyautogui
import linecache
from operator import itemgetter


#url_first = "http://www.bptoptracker.com/top/dance/39/2016-01-01"
url_first = "http://www.bptoptracker.com/top/tech-house/11/2017-01-01"
date_position = 54 #This is the index of the day marker on url_first.
genre = "\Tech-House" #The Genre Directory you want it to go in.
year = 2017
days = 364 #How many days there are in the year
os.system("mkdir C:\ProgramData\BeatportData" + genre)
os.chdir("C:\ProgramData\BeatportData" + genre )

def initialize() :
    os.system("start cmd.exe")
    pyautogui.hotkey("ctrl")
    time.sleep(3)
    pyautogui.typewrite("powershell.exe")
    pyautogui.hotkey("enter")

def html_open(h) :  #Saves the 31 days of the month
    i = 0
    time.sleep (1)
    prep = "Invoke-WebRequest " + h +  " -OutFile 'C:\ProgramData\BeatportData" + genre + "\D"  + h[date_position - 8:] + ".html'"
    pyautogui.typewrite(prep)
    pyautogui.hotkey("enter")    
    i = i + 1
    k = 2
    while i < 9 and i > 0 :
        time.sleep (4)
        pre = h[:date_position + 1] + str(k)
        prep = "Invoke-WebRequest " + pre +  " -OutFile 'C:\ProgramData\BeatportData" + genre + "\D"  + pre[date_position - 8:] + ".html'"
        pyautogui.typewrite(prep)
        time.sleep (0.3)
        pyautogui.hotkey("enter")
        i = i + 1
        k = k + 1
    while i >= 9 and i < 31  :
        time.sleep (4)
        pre = h[:date_position] + str(k)
        prep = "Invoke-WebRequest " + pre +  " -OutFile 'C:\ProgramData\BeatportData" + genre + "\D"  + pre[date_position - 8:] + ".html'"
        pyautogui.typewrite(prep)
        time.sleep (0.3)
        pyautogui.hotkey("enter")
        i = i + 1
        k = k + 1     
 
def html_save() : #saves all 31 tabs
    j = 0   
    while j < 31 :
        pyautogui.hotkey("ctrl" , "pagedown")
        time.sleep(0.5)
        pyautogui.hotkey("ctrl" , "s")
        time.sleep(0.5)
        pyautogui.hotkey("enter")
        time.sleep(0.5)
        j = j + 1

def html_close()  : #closes all 31 tabs and starts afresh
    time.sleep(0.5)
    pyautogui.hotkey("ctrl" , "pagedown" )
    time.sleep(0.3)
    ct = 0
    while ct <= 30 :
        pyautogui.hotkey("ctrl" , "w" )
        time.sleep(0.3)
        ct = ct + 1

def rest_month() : # full script run once only
    l = 1
    first = url_first
    while l >= 1 and l < 10 :
        second = first[:date_position - 2] + str(l) + first[date_position - 1:]
        html_open(second)
        time.sleep(5)
        l = l + 1
        second = first[:date_position - 2] + str(1) + first[date_position - 1:]
    while l >= 10 and l < 13 :
        second = first[:date_position - 3] + str(l) + first[date_position - 1:]
        html_open(second)
        time.sleep(5)
        l = l + 1
        second = first[:date_position - 3] + str(01) + first[date_position - 1:]
    if l == 13 :
        pyautogui.typewrite("stop-process -Id $PID")
        time.sleep(0.3)
        pyautogui.hotkey("enter")
        time.sleep(0.3)
        pyautogui.typewrite("exit \B")
        pyautogui.hotkey("enter")

"""BEGINNING OF SECOND PART"""


"""ipp.td.unwrap() removes the wrapper of the FIRST td tag
ipp.td.extract()  completely deletes the FIRST td tag"""

"""td_tag = ipp.td               Literally prints out the "4" in the first td tag
for string in td_tag.string :
    print (string) 
#print (ipp)"""

#for string in ipp.stripped_strings :   gets rid of empty strings (for example, songs without remixes) and also gets rid of whitespaces before and after strings

#for string in ipp.strings :
#    print (string)


""" This code takes a text file containing all the chart positions and exports a txt
file nicely formatted with all the details arranged in 13 row groupings by Position>Change>Artist>>>>>Empty 1>Empty 2. 
The empties represent two lines of html that are links to the beatport store and the play button on the website.


while ipp.find("tr") != None :   
    ipp.tr.unwrap()

while ipp.find("i") != None :
    ipp.i.extract()

while ipp.find("td") != None :
    ipp.td.unwrap()

while ipp.find("a") != None :
    ipp.a.unwrap()

while ipp.find("span") != None :
    ipp.span.unwrap()

ipp2 = ipp.encode(formatter=None)

with open("value_output.txt" , "w" ) as text_file :
    text_file.write( str(ipp2) )

print (ipp2)

time.sleep(150)     """

"""<img alt="" src="/images/covers/tracks/8610144_50x50.jpg"/> that image id 8610144 might be the best way to identify between tracks, or something similar! """


"""#Now we remove the first head tag
html_soup.head.extract()

Next I will try something ballsy, I suspect there are no div tags in the table, so I will remove all div tags.
That did not work. The data is nested within a div tag. I then find the suspecting div tag and stop extraction 
right before I hit that div tag. The last div tag before the suspect has class (gap gap-small)
while html_soup.find("div") != None and html_soup.find(class_="gap gap-small") != None :
    html_soup.div.extract()

#Now we unwrap that horrible div tag
html_soup.div.unwrap()

#Remove all subsequent div tags
while html_soup.find("div") != None :
    html_soup.div.extract()

#Remove all li, tags
while html_soup.find("li") != None :
    html_soup.li.extract()"""

def filt_and_export(site , j) :
    html = open( site , "r+" )
    html_soup = BeautifulSoup(html , "lxml")
    """While doing all that, I noticed a shortcut. All the data is contained within a tbody tag. 
    Why not unwrap that, and only that, instead of eating our way towards it?"""
    html_soup_tbody = html_soup.tbody
    html_empty = "This is a surplus day. Ignore."
    """Filtering out the bonus days like Feb. 31st and
    Getting the data out into nice, 13 line blocks."""
    if html_soup_tbody != None :
        m = 0
        n = 0
        while n < 100 :
            html_soup_tbody.tr.unwrap()
            html_soup_tbody.i.extract()
            html_soup_tbody.i.extract()
            html_soup_tbody.span.unwrap()
            html_soup_tbody.a.unwrap()
            html_soup_tbody.a.unwrap()
            html_soup_tbody.a.unwrap()
            html_soup_tbody.a.unwrap()
            html_soup_tbody.a.unwrap()
            html_soup_tbody.a.unwrap()
            l = 0
            while l < 12 :
                html_soup_tbody.td.unwrap()
                l = l+1
            n = n + 1

        while html_soup_tbody.find("tr") != None :
            html_soup_tbody.tr.unwrap()
            html_soup_tbody.i.extract()
            html_soup_tbody.i.extract()
            html_soup_tbody.span.unwrap()
            html_soup_tbody.a.unwrap()
            html_soup_tbody.a.unwrap()
            html_soup_tbody.a.unwrap()
            html_soup_tbody.a.unwrap()
            html_soup_tbody.a.unwrap()
            html_soup_tbody.a.unwrap()
            l = 0
            while l < 12 :
                html_soup_tbody.td.unwrap()
                l = l+1

        while html_soup_tbody.find("a") != None :
            html_soup_tbody.a.unwrap()
        
        
        #Now to export the mess.
        html_ready = html_soup_tbody.encode(formatter = None)
        j_set = str(j) + ".txt"
        with open( j_set , "w" ) as text_file :
            text_file.write( str(html_ready) )
        
        print "day" + str(j) + "complete"
    
    else :
        j_set = str(j) + ".txt"
        with open( j_set , "w" ) as text_file :
            text_file.write( html_empty )
    

#To run it through all websites
def full_filt_and_export() :
    start_site = "D" + str(year) + "-01-01.html"
    month_site_position = 6
    day_= 1
    month_ = 1
    day_index = 1

    while month_ <= 9 :
        month_site = start_site[:month_site_position + 1] + str(month_) + start_site[month_site_position + 2:]
        while day_ <= 9 : 
            now_site =  month_site[:month_site_position + 4] + str(day_) + month_site[month_site_position + 5:]
            filt_and_export(now_site , day_index)
            day_index = day_index + 1
            day_ = day_ + 1
        while day_ < 31 and day_ > 9 :
            now_site = month_site[:month_site_position + 3] + str(day_) + month_site[month_site_position + 5:]
            filt_and_export(now_site , day_index)
            day_index = day_index + 1
            day_ = day_ + 1
        if day_ == 31 : 
            now_site = month_site[:month_site_position + 3] + str(day_) + month_site[month_site_position + 5:]
            filt_and_export(now_site , day_index)
            day_index = day_index + 1
            day_ = 1
        month_ = month_ + 1

    while month_ <= 12 and month_ > 9 :
        month_site = start_site[:month_site_position] + str(month_) + start_site[month_site_position + 2:]
        while day_ <= 9 : 
            now_site =  month_site[:month_site_position + 4] + str(day_) + month_site[month_site_position + 5:]
            filt_and_export(now_site , day_index)
            day_index = day_index + 1
            day_ = day_ + 1
        while day_ < 31 and day_ > 9 :
            now_site = month_site[:month_site_position + 3] + str(day_) + month_site[month_site_position + 5:]
            filt_and_export(now_site , day_index)
            day_index = day_index + 1
            day_ = day_ + 1
        if day_ == 31 : 
            now_site = month_site[:month_site_position + 3] + str(day_) + month_site[month_site_position + 5:]
            filt_and_export(now_site , day_index)
            day_index = day_index + 1
            day_ = 1
        month_ = month_ + 1


"""BEGINNING OF THIRD PART"""


def write_tags(current_file) : #Writes the necessary tags into the document, leaving a line between each entry.
    a = 0
    if  linecache.getline(current_file , 3) == "1\n" :
        while a < 100 :
            current_linea = linecache.getline( current_file , a *15 + 2) #Blank
            current_lineb = linecache.getline( current_file , a *15 + 3) #Position
            int_current_lineb = str(101 - int(current_lineb) ) + "\n" #101 - Position to give weight of rank
            current_linec = linecache.getline( current_file , a *15  + 6)#Title
            current_lined = linecache.getline( current_file , a *15 + 8)#Artist
            current_linee = linecache.getline( current_file , a *15 + 9)#Remixer
            current_linef = linecache.getline( current_file , a *15 + 12)#Label
            if current_linee != None : #Sometimes there is no remixer
                with open( "Position_Title_Artist_Remixer_Label.txt" , "a" ) as text_file :
                    text_file.write( current_linea + int_current_lineb + current_linec + 
                    current_lined + current_linee + current_linef )  

            else :
                with open( "Position_Title_Artist_Remixer_Label.txt" , "a" ) as text_file :
                    text_file.write( current_linea + int_current_lineb + current_linec + 
                    current_lined + " " + current_linef ) 
            a = a + 1
            linecache.clearcache()

   
"""tic = time.clock()
toc = time.clock()
print (tic - toc) * 10**7"""

def full_write() : 
    """Files are labelled from 1-372. Luckily, the bonus days come out as None,
    so do not affect the overall file structure."""
    rep = 1 
    while rep <= 372 :
        open_file = str(rep) + ".txt"
        write_tags(open_file)
        print str(rep) + "/372 Done"
        rep = rep + 1

"""Beginning of Part 4"""

def make_dict(k) :#K is the amount of lines divide by 5
    a = 0
    song_dict = {}
    while a < k : #indexing starts at 0
        position = int(linecache.getline("Position_Title_Artist_Remixer_Label.txt", 6 * a + 2 ))
        title = str(linecache.getline("Position_Title_Artist_Remixer_Label.txt", 6 * a + 4))
        title_n = title[:len(title) - 1]
        artist = str(linecache.getline("Position_Title_Artist_Remixer_Label.txt", 6 * a + 3))
        artist_n = artist[:len(artist) - 1]
        remixer = str(linecache.getline("Position_Title_Artist_Remixer_Label.txt", 6 * a + 5))
        remixer_n = remixer[:len(remixer) - 1]
        label = str(linecache.getline("Position_Title_Artist_Remixer_Label.txt", 6 * a + 6))
        label_n = label[:len(label) - 1]
        if remixer == "\n" :
            song_dict[a] = [position, title_n, artist_n, " ", label_n ]
        else :
            song_dict[a]= [position, title_n, artist_n, remixer_n, label_n]
        a = a + 1
    return song_dict

def summation(track) :
    a = 0
    total = 0
    while a < 100 * days:
        if (song_dict[a][1] == song_dict[track][1] and song_dict[a][2] == song_dict[track][2] and 
        song_dict[a][3] == song_dict[track][3] ) :
            total = total + song_dict[a][0]
        a = a + 1
    return total

def duplicate_check(current) :
    check = 0 
    check_sum = 0
    while check < current :
        if (song_dict[check][1] == song_dict[current][1] and song_dict[check][2] == song_dict[current][2] 
        and song_dict[check][3] == song_dict[current][3])  :  
            check_sum = check_sum + 1
        check = check + 1 
    return check_sum

def make_summed_dict() :
    sum_dict = {}
    current_index = 0
    d = 1
    while current_index < 100 * days :
        if duplicate_check(current_index) == 0 :
            final_total = summation(current_index)
            sum_dict[d] = [ final_total, song_dict[current_index][1], song_dict[current_index][2],
            song_dict[current_index][3], song_dict[current_index][4] ]
            d = d + 1
        current_index = current_index + 1
    return sum_dict

def write_to_text() :#Prints without the largely useless remixer tag.
    d = 0
    while d < len(summed_dict) :
        with open(genre[1:] + " in 2017.txt" , "a" ) as text_file :
            text_file.write(str(d + 1) + "=" + str(summed_dict[d][0]) + "=" + str(summed_dict[d][2]) + 
            "=" +  str(summed_dict[d][1]) + "=" + str(summed_dict[d][4]) + "\n")
        d = d + 1
    


"""Actually Running the code"""
#Include Progress reports
tic = time.clock()
initialize()
rest_month()
full_filt_and_export()
full_write()
song_dict = make_dict(100 * days)
summed_dict = sorted(make_summed_dict().values(), key=itemgetter(0), reverse = True)
write_to_text()
toc = time.clock()

with open( "Timer.txt" , "a" ) as text_file :
    text_file.write( str(toc - tic) )
print "Done!"
time.sleep(10)

