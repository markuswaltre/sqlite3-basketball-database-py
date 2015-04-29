# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
from string import digits
import time

teamStats = open('teamStats.csv','w')
teamBasics = open('teamBasics.csv','w')
playerStats = open('playerStats.csv','w')
playerSalaries = open('playerSalaries.csv','w')

#URLs used
Base_URL = "http://www.basketball-reference.com"
Players_URL = "/leagues/NBA_2012_totals.html"
Teams_URL = "/teams"

## Find all the Players html
def getPlayersHtml():

    Players_html =  urlopen(Base_URL+Players_URL).read()
    soup = BeautifulSoup(Players_html)

    players_html = []

    for link in soup.find_all('a'):
        if (link.get('href').startswith("/players")):
            if Base_URL + str(link.get('href')) not in players_html:
                players_html.append(Base_URL + str(link.get('href')))

    players_html.remove("http://www.basketball-reference.com/players/")

    return players_html

def getPlayersHtml2():
    
    Players_html =  urlopen(Base_URL+Players_URL).read()
    players_html = []
    endHtml=re.findall('href="(/players/[a-z]/\S*.html)', Players_html)
    for element in endHtml:
        if Base_URL + element not in players_html:
            players_html.append(Base_URL + element)
   
    return players_html


## Find all the Teams html
def getTeamHtml():
    
    Teams_html = urlopen(Base_URL+Teams_URL).read()
    soup = BeautifulSoup(Teams_html)

    teams_html = []

    for link in soup.find_all('a',):
        if (link.get('href').startswith("/teams")):
            teams_html.append(Base_URL + str(link.get('href')))
            
    teams_html = set(teams_html)

    teams_html.remove("http://www.basketball-reference.com/teams/")
    
    return teams_html

#Strip everything from a string but didgets
def strip(string):
    return "".join(c for c in string if c in digits)

#Scraps player info from html file
def write_player_info_to_file(html):

    html = urlopen(html).read()
    soup = BeautifulSoup(html)
    #print(soup)

    #Scraps statistics table
    for i in soup.findAll("tr",{"id":"totals.2012"}):

        playerStats.write(html)                                           
        playerStats.write("".join(re.findall('<h1>(.*)</h1>', html))+",") #name
        playerStats.write("".join(re.findall('Weight:</span>\s*([0-9]+)\s*lbs', html))+",") #weight
        playerStats.write("".join(re.findall('Height:</span>\s([0-9]-[0-9]+)&nbsp', html))+",") #height
        playerStats.write("".join(re.findall('Position:</span>\s(.*?)&nbsp', html))+",") #position
        playerStats.write("".join(re.findall('Shoots:</span>\s(.*)<br>', html))+",") #shoots
        playerStats.write("".join(re.findall('Experience:</span>\s(.*)\syears', html))+",") #experience
        playerStats.write("".join(re.findall('Age:</span>\s(.*?)\syears', html))+",") #age

        for j in i.find_all("td", ):           
            playerStats.write(j.get_text().encode("utf-8")+",")

        
        playerStats.write("\n")

    if soup.find("table",{"id":"salaries"}) != None:
                for row in soup.find("table",{"id":"salaries"}).tbody.findAll('tr'):
                    playerSalaries.write(html)
                    playerSalaries.write("".join(re.findall('<h1>(.*)</h1>', html))+",")
                    playerSalaries.write(row.findAll('td')[0].getText()+",")
                    playerSalaries.write(row.findAll('td')[1].getText()+",")
                    playerSalaries.write(strip(row.findAll('td')[3].getText())+",")
                    playerSalaries.write("\n")
    

    return

#Scraps team info from html file
   
def write_team_info_to_file(html):

    html = urlopen(html).read()
    soup = BeautifulSoup(html)

    infoBox = soup.find("div", {"id":"info_box"})
    divMobileText = infoBox.find("div", {"class":"mobile_text"})
    string = divMobileText.text

    teamBasics.write(html)
    teamBasics.write("".join(re.findall('<h1>(.*)</h1>', html)).replace("Franchise Index","")+",") #name
    teamBasics.write(re.findall("Location:\s(.+?)\n", string)[0].replace(",","")+",")
#   teamBasics.write((re.findall("Team Name.+?\s(.+?)\n", string)[0]+",").replace(",",""))
    teamBasics.write(re.findall("Seasons:\s([0-9]+?).*?;", string)[0]+",")
#   teamStats.write(re.findall("[0-9]+?;\s(.+?).*?\s", string)[0]+",")
    teamBasics.write(re.findall("Record:\s(.+?),", string)[0]+",")
    teamBasics.write(re.findall("[0-9]+?,\s(.+?)W-L%", string)[0]+",")
    teamBasics.write(re.findall("Playoff Appearances:\s([0-9]+?).*?\s",string)[0]+",")
    teamBasics.write(re.findall("Championships:\s([0-9]+?)\s", string)[0]+",")
    teamBasics.write("\n")
    
    #Scraps statistics table
    tableData = soup.tbody.findAll("tr",)

    for i in tableData:
        teamStats.write(html)
        teamStats.write("".join(re.findall('<h1>(.*)</h1>', html)).replace("Franchise Index","")+",") #name
        for j in i.find_all("td"):
            teamStats.write(j.get_text().replace(",","")+",")
        teamStats.write("\n")
            
    

    return

def scrapToCsv(players_html, teams_html):
    i=0
    numberOfPlayers = str(len(players_html))
    for html in players_html:
        i+=1
        print str(i) + "/" + numberOfPlayers
        #print html
        write_player_info_to_file(html)
        time.sleep(0.5)

    numberOfTeams = str(len(teams_html))
    for html in teams_html:
        i+=1
        print str(i) + "/" + numberOfTeams
        write_team_info_to_file(html)
        time.sleep(1)
##        if i == 5:
##            break
    return

#Main method
def main():
    players_html = getPlayersHtml2()
    teams_html = getTeamHtml()
    scrapToCsv(players_html, teams_html)
    playerStats.close()
    playerSalaries.close()
    teamStats.close()
    teamBasics.close()
    print("close")
    return

main()


################################ Benchmarking

def benchmark():
    
    t0 = time.clock()
    getPlayersHtml() #BS method
    print time.clock() - t0, "seconds process time using BS"

    t0 = time.clock()
    getPlayersHtml2() #Regex method
    print time.clock() - t0, "seconds process time using Regex"

#benchmark()
    
##def procedure():
##    time.sleep(2.5)
##
### measure process time
##t0 = time.clock()
##procedure()
##print time.clock() - t0, "seconds process time"
##
### measure wall time
##t0 = time.time()
##procedure()
##print time.time() - t0, "seconds wall time"


##write_player_info_to_file("http://www.basketball-reference.com/players/c/cambyma01.html")
##playerStats.close()
##playerSalaries.close()
##print("klar")
