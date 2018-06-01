""" NOTES : The time.sleep() are for the system to have time to slow down before the next phase
Some genre changes happenned on 31 March 2018, complicating matters. Techno split into techno and melodic house & techno,
New Afro House genre, no doubt eating into house moniker. Unfortunately, new genres not added to bptoptracker."""

import os
import csv
import time
import sys
import linecache
from operator import itemgetter
from lxml import etree
from io import StringIO, BytesIO

#For printing Errors:
"""try :
     filt_and_export2("D2017-08-05.html" , 7)
except Exception as e: print(e)"""

#Examples of what is needed in for the code to run:
"""url_first = "http://www.bptoptracker.com/top/dance/39/2016-01-01" #Start URL
url_first = "http://www.bptoptracker.com/top/house/5/2017-01-01"
date_position = 48 #This is the index of the day marker on url_first.
genre = "\House" #The Genre Directory you want it to go in.
year = 2017
days = 364 #How many days there are in the year, accounting for leap years and database errors."""

genre_dict = { "\\Top-100" : [49, "/top100/0/"]
    ,"\\House" : [48 , "/house/5/" ]
    ,"\\Techno" : [49 , "/techno/6/"]
    ,"\\Trance" : [49 , "/trance/7/"]
    ,"\\Breaks" : [49 , "/breaks/9/"]
    ,"\\Dance" :  [49 , "/dance/39/"]
    ,"\\Dubstep" :  [51 , "/dubstep/18/"]
    ,"\\Indie-Dance-Nu-Disco" :  [64 , "/indie-dance-nu-disco/37/"]
    ,"\\DJ-Tools" :  [52 , "/dj-tools/16/"]
    ,"\\Hard-Dance" :  [53 , "/hard-dance/8/" ]
    ,"\\Tech-House" :  [54, "/tech-house/11/"]
    ,"\\Deep-House" :  [54, "/deep-house/12/" ]
    ,"\\Glitch-Hop" :  [54, "/glitch-hop/49/" ]
    ,"\\Psy-Trance" :  [54, "/psy-trance/13/"]
    ,"\\Drum-Bass" :  [56, "/drum-and-bass/1/"]
    ,"\\Future-House" :  [56, "/future-house/65/"]
    ,"\\Electro-House" :  [57, "/electro-house/17/"]
    ,"\\Funk-Soul-Disco" :  [59, "/funk-soul-disco/40/"]
    ,"\\Hip-Hop-R-B" : [59, "/hip-hop-r-and-b/38/"]
    ,"\\Minimal-Deep-Tech" :  [61 , "/minimal-deep-tech/14/"] 
    ,"\\Progressive-House" :  [61 , "/progressive-house/15/"]
    ,"\\Hardcore-Hard-Techno" :  [63, "/hardcore-hard-techno/2/"]
    ,"\\Big-Room" :  [52, "/big-room/79/"]
    ,"\\Reggae-Dancehall-Dub" :  [64, "/reggae-dancehall-dub/41/"]
    ,"\\Electronica-Downtempo" :  [64, "/electronica-downtempo/3/"] 
    ,"\\Funky-Groove-Jackin-House" :  [69, "/funky-groove-jackin-house/81/"]
    ,"\\Leftfield-House-Techno" :  [70, "/leftfield-house-and-techno/80/"] }

genre_list = ["\\Top-100"
    ,"\\House"
    ,"\\Techno"
    ,"\\Trance"
    ,"\\Breaks" 
    ,"\\Dance" 
    ,"\\Dubstep"
    ,"\\Indie-Dance-Nu-Disco"
    ,"\\DJ-Tools" 
    ,"\\Hard-Dance"
    ,"\\Tech-House" 
    ,"\\Deep-House" 
    ,"\\Glitch-Hop"
    ,"\\Psy-Trance"
    ,"\\Drum-Bass"
    ,"\\Future-House"
    ,"\\Electro-House"
    ,"\\Funk-Soul-Disco"
    ,"\\Hip-Hop-R-B"
    ,"\\Minimal-Deep-Tech"
    ,"\\Progressive-House"
    ,"\\Hardcore-Hard-Techno"
    ,"\\Big-Room"
    ,"\\Reggae-Dancehall-Dub"
    ,"\\Electronica-Downtempo"
    ,"\\Funky-Groove-Jackin-House" 
    ,"\\Leftfield-House-Techno" ]
 
os.system("mode con: cols=150 lines=40")

def initialize() : #Sets all necessary initial values.
    genre_input = raw_input(("\nWe should start with the genre. This is the genre you want to download. I will print\n"
    + "out a list of genres, and you can pick (by typing in their code). \nPlease be careful to type in the correct code! "
    + "\nTop 100 - 0 \n"
    + "House - 1 \n"
    + "Techno - 2                       \n"
    + "Trance - 3                       \n"
    + "Breaks - 4                       \n"
    + "Dance - 5                        \n"
    + "Dubstep - 6                      \n"
    + "Indie - Dance & Nu Disco - 7          \n"
    + "DJ Tools - 8                      \n"
    + "Hard Dance - 9                    \n"
    + "Tech House - 10                   \n"
    + "Deep House - 11                   \n"
    + "Glitch Hop - 12                   \n"
    + "Psy Trance - 13                   \n"
    + "Drum & Bass - 14                  \n"
    + "Future House - 15                 \n"
    + "Electro House - 16                \n"
    + "Funk, Soul & Disco - 17           \n"
    + "Hip - Hop / R&B - 18              \n"
    + "Minimal/Deep Tech - 19            \n"
    + "Progressive  House - 20           \n"
    + "Harccore/Hard Techno - 21         \n"
    + "Big Room - 22                     \n"
    + "Reggae/Dancehall/Dub - 23         \n"
    + "Electronica/Downtempo - 24        \n"
    + "Funky Groove/Jackin House - 25    \n"
    + "Leftfield House & Techno - 26     \n"
    + "\n\nWhat genre are we dealing with?\n\n"))
    year = raw_input(("\n\nThis is a small thing. What year are these charts from?\n\n"))
    resume = raw_input(("\nThanks for all the info. I will now try my best! The time I take is largely dependent on network speed, \nso thanks "
    + "in advance for your patience.\nPress Enter to continue or if you think you made a mistake, we can start again, simply press R.\n\n"))
    if (resume is "R" or resume is "r" ) is True :
        return initialize()
    else:
        return (year, genre_input)

def initialize_simplified(year, genre) :#Sets all initial values with minimal input needed.
    os.system("mkdir C:\ProgramData\BeatportData" + "\\" + str(year) + genre )
    os.system("mkdir C:\ProgramData\BeatportData" + "\\" + str(year) + genre + "\Data" )
    os.chdir("C:\ProgramData\BeatportData" + "\\" + str(year) +  genre + "\Data" )

def progress_bar(value, total) :#Literally a progress bar, largely useful for part I, not so much for the other parts.
        sys.stdout.write("\r" + str(value * 100 / total) + 
        " Percent Complete [{0}{1}]".format("|" * int(value *100 / total), " " * (100 - int(value *100 / total))))
        sys.stdout.flush()

def seek_to_genre_data(genre) :
    os.chdir("C:\ProgramData\BeatportData" + "\\" + str(year) +  genre + "\Data" )

def seek_to_genre(genre) :
    os.chdir("C:\ProgramData\BeatportData" + "\\" + str(year) +  genre)

"""Beginning of Part One"""

"""This part saves the html for the charts for all the days of the year, each month being assigned 31 days for consistency."""

def html_open(h, month, date_position, genre, year) :  #Saves the 31 days of the month
    i = 0
    prep = ("Invoke-WebRequest " + h +  " -OutFile 'C:\ProgramData\BeatportData" + "\\" + str(year) + genre + 
    "\Data" +"\D"  + h[date_position - 8:] + ".html'" )
    os.system("Powershell " + prep)
    i = i + 1
    k = 2
    while i < 9 and i > 0 :
        pre = h[:date_position + 1] + str(k)
        prep = ("Invoke-WebRequest " + pre +  " -OutFile 'C:\ProgramData\BeatportData" + "\\" + str(year) + genre + 
        "\Data" + "\D"  + pre[date_position - 8:] + ".html'" )
        os.system("Powershell " + prep)
        position = int((31 * (month - 1)) + k)
        #progress_bar(position, 372)
        i = i + 1
        k = k + 1
    while i >= 9 and i < 31  :
        pre = h[:date_position] + str(k)
        prep = ("Invoke-WebRequest " + pre +  " -OutFile 'C:\ProgramData\BeatportData" + "\\" + str(year) + genre + 
        "\Data" + "\D"  + pre[date_position - 8:] + ".html'" )
        os.system("Powershell " + prep)
        position = int((31 * (month - 1)) + k)
        progress_bar(position, 372)
        i = i + 1
        k = k + 1     
 
def rest_month(url_first, date_position, genre, year) : #Initiates the saving script for all 12 months
    l = 1
    first = url_first
    while l >= 1 and l < 10 :
        second = first[:date_position - 2] + str(l) + first[date_position - 1:]
        html_open(second, l, date_position, genre, year)
        l = l + 1
        second = first[:date_position - 2] + str(1) + first[date_position - 1:]
    while l >= 10 and l < 13 :
        second = first[:date_position - 3] + str(l) + first[date_position - 1:]
        html_open(second, l, date_position, genre, year)
        l = l + 1
        second = first[:date_position - 3] + str(01) + first[date_position - 1:]

"""BEGINNING OF SECOND PART"""

""" This code takes a text file containing all the chart positions and exports a txt
file nicely formatted with all the details arranged in 10 row groupings by 
Position>Change>Title>Artist>Remixer>BPM>Key>Label>Release Date>Empty 1. 
The empties are jus neat seperators of entries."""

"""Previously used Beautiful Soup in a sluggish way (extract, unwrap etc.) Now uses etree and lxml and takes advantage of some 
of the regularity in bptoptrackers html."""

def filt_and_export(site, j, genre, year) :

    seek_to_genre_data(genre)

    set = str(j) + ".txt"
    j_set = open( set , "a")
    html_empty = "This is a surplus day. Ignore."
      
    if os.path.getsize(site) > 20000 :  #Check if the day is for a fake day like Feb. 29th or not.
      
    
        html_file = open(site , "r" )
        parser = etree.HTMLParser()
        html_parse = etree.parse(html_file , parser)#Returns an ElementTree object
        root = html_parse.getroot()
        #tbody = root[1][5][5][1] #Position of tbody, used in case the iter loop does not work.
        for tbody in root.iter("tbody") :
            tbody = tbody
        
        #Getting the info out.
        pos_index = 0
        while pos_index < 100:
            artist_final = 0
            remixer_final = 0
            artist = 0 
            remixer = 0
            song_1 = []
            artist_list = []
            remixer_list = []
            if (genre == "\\Top-100" ) is False :
                while remixer < len(tbody[pos_index][5]) :#Handling varying number of remixers and artists.
                    try :
                        remixer_list.append(tbody[pos_index][5][remixer].text.replace("\n" , "").encode("utf-8"))
                    except :
                        pass
                    remixer = remixer + 1
                while artist < len(tbody[pos_index][4]) :
                    if (tbody[pos_index][4][artist].text is None ) is False :
                        artist_list.append(tbody[pos_index][4][artist].text.replace("\n" , "").encode("utf-8"))
                    if (tbody[pos_index][4][artist].text is None ) is True :
                        pass
                    artist = artist + 1
                song_1.append(tbody[pos_index][0].text.replace("\n" , "").encode("utf-8"))#Position
                song_1.append(tbody[pos_index][1][0].text.replace("\n" , "").encode("utf-8"))#Movement
                song_1.append(tbody[pos_index][3][0].text.replace("\n" , "").encode("utf-8"))#Title
                song_1.append(artist_list)#Artist
                song_1.append(remixer_list)#Remixer
                if (tbody[pos_index][6].text is None ) is False :#Sometimes there is no BPM, Label, Key or Release Date.
                    song_1.append((tbody[pos_index][6].text.encode("utf-8")))#BPM
                if (tbody[pos_index][6].text is None ) is True :
                    song_1.append("")#BPM
                if (tbody[pos_index][7].text is None ) is False :
                    song_1.append(tbody[pos_index][7].text.replace("\n" , "").encode("utf-8"))#Key
                if (tbody[pos_index][7].text is None ) is True :
                    song_1.append("")#Key
                if (tbody[pos_index][8][0].text is None ) is False :
                    song_1.append(tbody[pos_index][8][0].text.replace("\n" , "").encode("utf-8"))#Label
                if (tbody[pos_index][8][0].text is None ) is True :
                    song_1.append("")#Label
                if (tbody[pos_index][9].text is None ) is False :
                    song_1.append(tbody[pos_index][9].text.replace("\n" , "").encode("utf-8"))#Release Date
                if (tbody[pos_index][9].text is None ) is True :
                    song_1.append("")#Release Date
                
            if (genre == "\\Top-100" ) is True :
                while remixer < len(tbody[pos_index][5]) :#Handling varying number of remixers and artists.
                    try :
                        remixer_list.append(tbody[pos_index][5][remixer].text.replace("\n" , "").encode("utf-8"))
                    except :
                        pass
                    remixer = remixer + 1
                while artist < len(tbody[pos_index][4]) :
                    if (tbody[pos_index][4][artist].text is None ) is False :
                        artist_list.append(tbody[pos_index][4][artist].text.replace("\n" , "").encode("utf-8"))
                    if (tbody[pos_index][4][artist].text is None ) is True :
                        pass
                    artist = artist + 1
                song_1.append(tbody[pos_index][0].text.replace("\n" , "").encode("utf-8"))#Position
                song_1.append(tbody[pos_index][1][0].text.replace("\n" , "").encode("utf-8"))#Movement
                song_1.append(tbody[pos_index][3][0].text.replace("\n" , "").encode("utf-8"))#Title
                song_1.append(artist_list)#Artist
                song_1.append(remixer_list)#Remixer
                if (tbody[pos_index][6][0].text is None ) is False :#Sometimes there is no Genre, Label, or Release Date.
                    song_1.append((tbody[pos_index][6][0].text.encode("utf-8")))#Genre
                if (tbody[pos_index][6][0].text is None ) is True :
                    song_1.append("")#Genre
                if (tbody[pos_index][7][0].text is None ) is False :
                    song_1.append(tbody[pos_index][7][0].text.replace("\n" , "").encode("utf-8"))#Label
                if (tbody[pos_index][7][0].text is None ) is True :
                    song_1.append("")#Label
                if (tbody[pos_index][8].text is None ) is False :
                    song_1.append(tbody[pos_index][8].text.replace("\n" , "").encode("utf-8"))#Release Date
                if (tbody[pos_index][8].text is None ) is True :
                    song_1.append("")#Release Date
                

            #Exporting the mess
            j_set.write(song_1[0] + "\n")
            j_set.write(song_1[1] + "\n")
            j_set.write(song_1[2] + "\n")
            if len(song_1[3]) != 0 :
                while artist_final < len(song_1[3]) - 1 :
                    j_set.write(song_1[3][artist_final])
                    artist_final = artist_final + 1
                    j_set.write(" , ")
                j_set.write(song_1[3][artist_final] + "\n")
            if len(song_1[3]) == 0 :
                j_set.write("\n")
            while remixer_final < len(song_1[4]) - 1 :
                j_set.write(song_1[4][remixer_final])
                remixer_final = remixer_final + 1
                j_set.write(" , ")
            if len(song_1[4]) != 0 :
                j_set.write(song_1[4][remixer_final] + "\n")
            if len(song_1[4]) == 0 :
                j_set.write("\n")
            j_set.write(song_1[5] + "\n")
            j_set.write(song_1[6] + "\n")
            j_set.write(song_1[7] + "\n")
            if (genre == "\\Top-100" ) is False :
                j_set.write(song_1[8] + "\n\n")
            if (genre == "\\Top-100" ) is True :
                j_set.write("N/A" + "\n\n" )
            
            pos_index = pos_index + 1

        progress_bar(j, 372)
          
    if os.path.getsize(site) < 20000 :
        j_set.write( html_empty )  
        progress_bar(j, 372)

def full_filt_and_export(genre, year) : #To run it through all saved websites.
    start_site = "D" + str(year) + "-01-01.html"
    month_site_position = 6
    day_= 1
    month_ = 1
    day_index = 1

    while month_ <= 9 :
        month_site = start_site[:month_site_position + 1] + str(month_) + start_site[month_site_position + 2:]
        while day_ <= 9 : 
            now_site =  month_site[:month_site_position + 4] + str(day_) + month_site[month_site_position + 5:]
            filt_and_export(now_site , day_index, genre, year)
            day_index = day_index + 1
            day_ = day_ + 1
        while day_ < 31 and day_ > 9 :
            now_site = month_site[:month_site_position + 3] + str(day_) + month_site[month_site_position + 5:]
            filt_and_export(now_site , day_index, genre, year)
            day_index = day_index + 1
            day_ = day_ + 1
        if day_ == 31 : 
            now_site = month_site[:month_site_position + 3] + str(day_) + month_site[month_site_position + 5:]
            filt_and_export(now_site , day_index, genre, year)
            day_index = day_index + 1
            day_ = 1
        month_ = month_ + 1

    while month_ <= 12 and month_ > 9 :
        month_site = start_site[:month_site_position] + str(month_) + start_site[month_site_position + 2:]
        while day_ <= 9 : 
            now_site =  month_site[:month_site_position + 4] + str(day_) + month_site[month_site_position + 5:]
            filt_and_export(now_site , day_index, genre, year)
            day_index = day_index + 1
            day_ = day_ + 1
        while day_ < 31 and day_ > 9 :
            now_site = month_site[:month_site_position + 3] + str(day_) + month_site[month_site_position + 5:]
            filt_and_export(now_site , day_index, genre, year)
            day_index = day_index + 1
            day_ = day_ + 1
        if day_ == 31 : 
            now_site = month_site[:month_site_position + 3] + str(day_) + month_site[month_site_position + 5:]
            filt_and_export(now_site , day_index, genre, year)
            day_index = day_index + 1
            day_ = 1
        month_ = month_ + 1

"""BEGINNING OF THIRD PART"""

"""This part of the code goes through the list of songs and their weighted positions from the previous part, selectively 
picks what song data to keep (Artist, Remixer, Weighted Rank and Label) and collects all this into one big file.
The write_tags function is reading from the \Genre\Data directory but outputting to the \Genre directory."""

def days_check(genre, year) : #This returns the number of days that actually have charts.
    seek_to_genre_data(genre)
    day_count = 0
    day_index = 1
    while day_index <= 372: 
        if os.path.getsize(str(day_index) + ".txt") > 5000 :
            day_count = day_count + 1
            day_index = day_index + 1
        else :
            day_index = day_index + 1
    
    return day_count
        
def write_tags(rep, text_file, genre, year) : #Writes the necessary tags into the document, leaving a line between each entry.
    a = 0
    current_file = str(rep) + ".txt"
    seek_to_genre_data(genre)
    if  linecache.getline(current_file , 1) == "1\n" :
        while a < 100:
            seek_to_genre_data(genre)
            current_linea = linecache.getline( current_file , a *10 + 10) #Blank
            current_lineb = linecache.getline( current_file , a *10 + 1) #Position
            int_current_lineb = str(101 - int(current_lineb) ) + "\n" #101 - Position to give weight of rank
            current_linec = linecache.getline( current_file , a *10  + 3)#Title
            current_lined = linecache.getline( current_file , a *10 + 4)#Artist
            current_linee = linecache.getline( current_file , a *10 + 5)#Remixer
            if (genre == "\\Top-100" ) is False :
                current_linef = linecache.getline( current_file , a *10 + 8)#Label
            if (genre == "\\Top-100" ) is True :
                current_linef = linecache.getline( current_file , a *10 + 6)#Label
            if current_linee != "/n" : #Sometimes there is no remixer
                seek_to_genre(genre)
                text_file.write( current_linea + int_current_lineb + current_linec + 
                current_lined + current_linee + current_linef )

            else : 
                seek_to_genre(genre)
                text_file.write( current_linea + int_current_lineb + current_linec + 
                current_lined + " " + current_linef )                     

            a = a + 1
            #os.chdir("C:\ProgramData\BeatportData" + "\\" + str(year) +  genre + "\Data" )
            linecache.clearcache()
  
def full_write(genre, year) : 
    """Files are labelled from 1-372. Luckily, the bonus days come out as None,
    so do not affect the overall file structure."""
    seek_to_genre(genre)
    text_file = open( "Position_Title_Artist_Remixer_Label.txt" , "a" )
    if days_check(genre, year) != 0:
        rep_day = 1 
        while rep_day <= 372 : 
            write_tags(rep_day, text_file, genre, year)
            progress_bar(rep_day, 372)
            rep_day = rep_day + 1
        seek_to_genre(genre)
        text_file.close()
    if days_check(genre, year) == 0:
        text_file.write("This is a surplus genre. Ignore.")
        text_file.close()

"""Beginning of Part 4"""

"""This part takes the big file and creates defines a dictionary from it, then using that dictionary, compares different chart
entries, summing their weighted rank and then sorts the final list, outputting to a text file in a neat format."""

def make_dict(k, genre) :#Makes the dictionary from the big file from part 3. K is the amount of lines divide by 5
    a = 0
    song_dict = {}
    while a < k : #indexing starts at 0
        seek_to_genre(genre)
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
    linecache.clearcache()
    return song_dict

def summation(track, days, song_dict) : #Sums all the weighted ranks for a particular song.
    a = 0
    total = 0
    while a < 100 * days :
        if (song_dict[a][1] == song_dict[track][1] and song_dict[a][2] == song_dict[track][2] and 
        song_dict[a][3] == song_dict[track][3] ) :
            total = total + song_dict[a][0]
        a = a + 1
    return total

def duplicate_check(current, song_dict) : #This checks how many times a song has charted before a particular instance.
    check = 0 
    check_sum = 0
    while check < current :
        if (song_dict[check][1] == song_dict[current][1] and song_dict[check][2] == song_dict[current][2] 
        and song_dict[check][3] == song_dict[current][3])  :  
            check_sum = check_sum + 1
        check = check + 1 
    return check_sum

def make_summed_dict(days, song_dict) : #Creates the filtered dictionary with the summed weighted ranks.
    sum_dict = {}
    current_index = 0
    d = 1
    while current_index < 100 * days :
        if duplicate_check(current_index, song_dict) == 0 :
            final_total = summation(current_index, days, song_dict)
            sum_dict[d] = [ final_total, song_dict[current_index][1], song_dict[current_index][2],
            song_dict[current_index][3], song_dict[current_index][4] ]
            d = d + 1
        current_index = current_index + 1
    return sum_dict

def write_to_text(genre, year) :#Prints without the largely useless remixer tag.
    d = 0
    summed_dict = sorted(make_summed_dict(days_check(genre, year), make_dict(100 * days_check(genre, year), genre)).values(), key=itemgetter(0), reverse = True)
    while d < len(summed_dict) :
        seek_to_genre(genre)
        with open(genre[1:] + " in " + str(year) + ".txt" , "a" ) as text_file :
            text_file.write(str(d + 1) + "=" + str(summed_dict[d][0]) + "=" + str(summed_dict[d][2]) + 
            "=" +  str(summed_dict[d][1]) + "=" + str(summed_dict[d][4]) + "\n")
        d = d + 1
    summed_dict = {}

#Running the code


tic2 = time.clock()
(year, genre_input) = initialize()
genre = genre_list[int(genre_input)]
url_first = "http://www.bptoptracker.com/top" + genre_dict[genre][1] + str(year) + "-01-01"
print "STAGE 1/4 : \n"
initialize_simplified(year, genre)
rest_month(url_first, genre_dict[genre][0], genre, year)
print "\n\nSTAGE 2/4 : \n"
full_filt_and_export(genre,year)
print "\n\nSTAGE 3/4 : \n"
full_write(genre, year)
print "\n\nSTAGE 4/4 : "
print "\nProcessing..."
if days_check(genre,year) != 0 :
    write_to_text(genre, year)
else :
    seek_to_genre(genre)
    with open(genre[1:] + " in " + str(year) + ".txt" , "a" ) as text_file :
        text_file.write("Nothing to See Here")
toc2 = time.clock()

os.chdir("C:\ProgramData\BeatportData" + "\\" + str(year))
with open( "Timer.txt" , "a" ) as text_file :
    text_file.write( str(toc2 - tic2) )

raw_input(("\n\nThe process is finally done! The sorted and ranked charts have been outputted as a .txt file in "
+ "C:ProgramData\BeatportData\Year\Genre.\nIt is called Genre in 20XX.txt.\nAlso stored are two files, one called timer.txt "
+ "that recorded how long this process took.\nThe other one is called Position_Title_Arist_Remixer_Label.txt "
+ "that is a list of all the songs that charted, and in what weighted ranking\nthey charted in.\n\n\nOn the structure "
+"of the main file, each line is read as such:\nRank=Total Points=Title=Artist=Label   seperated by equal signs.\nThe Top-100 "
+ "entry is a bit different, read as Rank=Total Points=Title=Artist=Genre. \n\n"
+ "Thanks for giving the program a whirl. Press enter to exit."))

os.system("start explorer.exe " + "C:\ProgramData\BeatportData" + "\\" + str(year) + "\\" + genre[1:])