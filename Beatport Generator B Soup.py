""" NOTES : The time.sleep() are for the system to have time to slow down before the next phase"""

import os
from bs4 import BeautifulSoup
import csv
import time
import sys
import linecache
from operator import itemgetter

#For printing Errors:
"""try :
     filt_and_export2("D2017-08-05.html" , 7)
except Exception as e: print(e)"""


#Examples of what is needed in for the code to run:
#url_first = "http://www.bptoptracker.com/top/dance/39/2016-01-01" #Start URL
url_first = "http://www.bptoptracker.com/top/deep-house/12/2017-01-01"
date_position = 48 #This is the index of the day marker on url_first.
genre = "\House" #The Genre Directory you want it to go in.
year = 2017
days = 217 #How many days there are in the year, accounting for leap years and database errors.


def initialize() : #Sets all necessary initial values.
    url = raw_input(("I, the generator, will need five things from you. First, a start url so that "
    + "I know where to start generating from!\nA start url usually looks something like "
    + "http://www.bptoptracker.com/top/dance/39/2016-01-01 "
    + "\nThis is the first day of the dance charts in 2016. So, where should I start?\n\n"))
    index = (raw_input(("\nThe second thing is the most technical. There is a value I call the date index that "
    + "I need.\nYou can get it from the start url. It is the index (counting from zero!)of the first digit if the "
    + "day date.\nAs an example, in http://www.bptoptracker.com/top/dance/39/2016-01-[0]1 , the index of the bracketed"
    + "zero is 49.\nNow, simply type in the index, or type Y and I will bring up a list of recommended indexes!\n\n"))) 
    if (index is "Y" or index is "y" ) is True :
        index = (raw_input("\nHere is a hopefully helpful list:\n" + "House = 48\n" + 
        "Techno, Trance, Breaks, Dance = 49\n" + 
        "Dubstep = 51\n" +
        "Big-Room, DJ-Tools = 52\n" + 
        "Hard-Dance = 53\n" + 
        "Tech-House, Deep-House, Glitch-Hop, Psy-Trance = 54\n" + 
        "Drum&Bass = 56\n" + 
        "Electro-House, Future House = 57\n" +
        "Funk-Soul-Disco, Hip-Hop-R&B = 59\n" + 
        "Minimal-Deep-Tech, Progressive-House = 61\n" + 
        "Hardcore-Hard-Techno = 63\n" + 
        "Indie-Dance-Nu-Disco, Reggae-Dancehall, Electronica-Downtempo = 64\n" + 
        "Funky-Groove-Jackin-House = 69\n" + 
        "Leftfield-House&Techno = 70\n\n" + "What index would you like to use?\n\n"))
    genre = "\\" + raw_input(("\nNow for the third thing. The genre. In the example I gave in the start url,"
    + "the genre was Dance. \nPlease be careful not to include any spaces in your genre, as that would be "
    + "too much for me to handle! \nWhat genre are we dealing with?\n\n"))
    year = raw_input(("\nFourth is a small thing. What year are these charts from?\n\n"))
    days = raw_input(("\nThe last thing will seem a bit silly, but how many days are there in this year?"
    + "\nThis helps me account for leap years, and other oddities, such as the charts for 05 October 2017 not existing."
    + "\nIf anything goes awry along the way, this is the likely culprit, and if possible, please run me again with this "
    + "reduced by one.\n\n"))
    raw_input(("\nThanks for all that info. I will now try my best! I usually take about two hours to finish, so thanks "
    + "in advance for your patience.\nPress enter to continue.\n"))
    if ( not " " in genre and str.isdigit(year) and str.isdigit(index) and str.isdigit(days)) is True :    
            return (url, int(index), genre, int(year), int(days))
    if ( not " " in genre and str.isdigit(year) and str.isdigit(index) and str.isdigit(days)) is False :
        raw_input(("You seemed to have accidentally put in a space in your genre, or typed what is not a number in the " 
        + "year or days fields.\nPlease take some time to find the offending culprit, and we can start again.\n"))
        return initialize()

os.system("mode con: cols=150 lines=30")
#(url_first, date_position, genre, year, days) = initialize()
os.system("mkdir C:\ProgramData\BeatportData" + "\\" + str(year) + genre )
os.system("mkdir C:\ProgramData\BeatportData" + "\\" + str(year) + genre + "\Data" )
os.chdir("C:\ProgramData\BeatportData" + "\\" + str(year) +  genre + "\Data" )

def progress_bar(value, total) :
        sys.stdout.write("\r" + str(value * 100 / total) + 
        " Percent Complete [{0}{1}]".format("|" * int(value *100 / total), " " * (100 - int(value *100 / total))))
        sys.stdout.flush()

def html_open(h, month) :  #Saves the 31 days of the month
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
        progress_bar(position, 372)
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
 

def rest_month() : # full script run once only
    l = 1
    first = url_first
    while l >= 1 and l < 10 :
        second = first[:date_position - 2] + str(l) + first[date_position - 1:]
        html_open(second, l)
        l = l + 1
        second = first[:date_position - 2] + str(1) + first[date_position - 1:]
    while l >= 10 and l < 13 :
        second = first[:date_position - 3] + str(l) + first[date_position - 1:]
        html_open(second, l)
        l = l + 1
        second = first[:date_position - 3] + str(01) + first[date_position - 1:]

"""BEGINNING OF SECOND PART"""

""" This code takes a text file containing all the chart positions and exports a txt
file nicely formatted with all the details arranged in 13 row groupings by Position>Change>Artist>>>>>Empty 1>Empty 2. 
The empties represent two lines of html that are links to the beatport store and the play button on the website."""

"""The way unwrap or extract work is that tey act on the first instance of that particular tag, and only on the first instance.
The find function also stops at the first instance, but there is a find all that can find multiple instances."""

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
        
        progress_bar(j, 372)
    
    else :
        j_set = str(j) + ".txt"
        with open( j_set , "w" ) as text_file :
            text_file.write( html_empty )

        progress_bar(j, 372)
    

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

"""This part of the code goes through the list of songs and their weighted positions from th eprevious part, selectively 
picks what song data to keep (Artist, Remixer, Weighted Rank and Label) and collects all this into one big file.
The write_tags function is reading from the \Genre\Data directory but outputting to the \Genre directory."""


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
                text_file.write( current_linea + int_current_lineb + current_linec + 
                current_lined + current_linee + current_linef )  

            else : 
                text_file.write( current_linea + int_current_lineb + current_linec + 
                current_lined + " " + current_linef ) 
                
            a = a + 1
            #os.chdir("C:\ProgramData\BeatportData" + "\\" + str(year) +  genre + "\Data" )
            linecache.clearcache()

   

def full_write() : 
    """Files are labelled from 1-372. Luckily, the bonus days come out as None,
    so do not affect the overall file structure."""
    rep = 1 
    while rep <= 372 : 
        open_file = str(rep) + ".txt"
        write_tags(open_file)
        progress_bar(rep, 372)
        rep = rep + 1
    text_file.close()

"""Beginning of Part 4"""

"""This part takes the big file and creates defines a dictionary from it, then using that dictionary, compares different chart
entries, summing their weightd rank and then sorts the final list, outputting to a text file in a neat format."""

def make_dict(k) :#Makes the dictionary from the bif file from part 3. K is the amount of lines divide by 5
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

def summation(track) : #Sums all the weighted ranks for a particular song.
    a = 0
    total = 0
    while a < 100 * days:
        if (song_dict[a][1] == song_dict[track][1] and song_dict[a][2] == song_dict[track][2] and 
        song_dict[a][3] == song_dict[track][3] ) :
            total = total + song_dict[a][0]
        a = a + 1
    return total

def duplicate_check(current) : #This checks how many times a song has charted before a particular instance.
    check = 0 
    check_sum = 0
    while check < current :
        if (song_dict[check][1] == song_dict[current][1] and song_dict[check][2] == song_dict[current][2] 
        and song_dict[check][3] == song_dict[current][3])  :  
            check_sum = check_sum + 1
        check = check + 1 
    return check_sum

def make_summed_dict() : #Creates the filtered dictionary with the summed weighted ranks.
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
tic = time.clock()
"""print "STAGE 1/4 : \n"
rest_month()
print "\n STAGE ONE COMPLETE \n"
print "STAGE 2/4 : \n"
full_filt_and_export()
print "\n STAGE TWO COMPLETE \n"
print "STAGE 3/4 : \n"
os.chdir("C:\ProgramData\BeatportData" + "\\" + str(year) +  genre )
text_file = open( "Position_Title_Artist_Remixer_Label.txt" , "a" )
os.chdir("C:\ProgramData\BeatportData" + "\\" + str(year) +  genre + "\Data" )
full_write()
print "\n STAGE THREE COMPLETE \n"""
print "STAGE 4/4 : "
print "Processing..."
os.chdir("C:\ProgramData\BeatportData" + "\\" + str(year) +  genre )
song_dict = make_dict(100 * days)
summed_dict = sorted(make_summed_dict().values(), key=itemgetter(0), reverse = True) #Sorting needed for neat output.
write_to_text()
print "\n STAGE FOUR COMPLETE"
toc = time.clock()

with open( "Timer.txt" , "a" ) as text_file :
    text_file.write( str(toc - tic) )

raw_input(("\n\nThe process is finally done! The sorted and ranked chart has been outputted as a .txt file in "
+ "C:ProgramData\BeatportData\Year\Genre.\nIt is called Genre in 2017.txt.\nAlso stored are two files, one called timer.txt "
+ "that recorded how long this process took.\nThe other one is called Position_Title_Arist_Remixer_Label.txt "
+ "that is a list of all the songs that charted, and in what weighted ranking they charted in.\n\n\nOn the structure "
+"of the main file, each line is read as such:\nRank=Total Points=Title=Artist=Label   seperated by equal signs.\n\n"
+ "Thanks for giving the program a whirl. Press enter to exit."))
#os.system("start explorer.exe " + "C:\ProgramData\BeatportData" + "\\" + str(year) +  genre)

