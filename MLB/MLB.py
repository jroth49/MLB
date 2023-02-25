#imports
import time as t
from datetime import datetime as dt
from bs4 import BeautifulSoup as bs
import requests as r
import csv as c
import os as os
import html
import sys
import random
import threading as t

proxies = []


#util functions
def convertDateURL(date):
    #needs to convert from Thurday, September 8, 2022 -> 202209080.shtml
    newDate = date[date.index(',') + 2: len(date)] #removes day of the week
    newDt = dt.strptime(newDate, '%B %d, %Y').date()
    return str(newDt.year) + str(newDt.strftime('%m')) + str(newDt.strftime('%d'))

def convertDateFile(date):
    newDate = date[date.index(',') + 2: len(date)] #removes day of the week
    newDt = dt.strptime(newDate, '%B %d, %Y').date()
    return str(newDt.year) + '-' + str(newDt.month) + '-' + str(newDt.day)

def getTeamAbrv(team):

    if team == 'Cleveland Indians': #pre PC bullshit
        return 'CLE'

    match team:
        case 'Arizona D\'Backs':
            return 'ARI'
        case 'Arizona Diamondbacks':
            return 'ARI'
        case 'Atlanta Braves':
            return 'ATL'
        case 'Baltimore Orioles':
            return'BAL'
        case 'Boston Red Sox':
            return'BOS'
        case 'Chicago White Sox':
            return'CHA'
        case 'Chicago Cubs':
            return'CHN'
        case 'Cincinnati Reds':
            return'CIN'
        case 'Cleveland Guardians':
            return'CLE'
        case 'Colorado Rockies':
            return'COL'
        case 'Detroit Tigers':
            return'DET'
        case 'Houston Astros':
            return'HOU'
        case 'Kansas City Royals':
            return'KCA'
        case 'Los Angeles Angels':
            return'ANA'
        case 'Los Angeles Dodgers':
            return'LAN'
        case 'Miami Marlins':
            return'MIA'
        case 'Milwaukee Brewers':
            return'MIL'
        case 'Minnesota Twins':
            return'MIN'
        case 'New York Yankees':
            return'NYA'
        case 'New York Mets':
            return'NYN'
        case 'Oakland Athletics':
            return'OAK'
        case 'Philadelphia Phillies':
            return'PHI'
        case 'Pittsburgh Pirates':
            return'PIT'
        case 'San Diego Padres':
            return'SDN'
        case 'San Francisco Giants':
            return'SFN'
        case 'Seattle Mariners':
            return'SEA'
        case 'St. Louis Cardinals':
            return'SLN'
        case 'St Louis Cardinals':
            return 'SLN'
        case 'Tampa Bay Rays':
            return'TBA'
        case 'Texas Rangers':
            return'TEX'
        case 'Toronto Blue Jays':
            return'TOR'
        case 'Washington Nationals':
            return'WAS'

def getTeamNameESPN(team):
    #setup for espn depth chart grabber
    return team

def parseTeamOdds(team):
    match team:
        case 'CUB':
            return 'CHN'
        case 'NYM':
            return 'NYN'
        case 'STL':
            return 'SLN'
        case 'SDG':
            return 'SDN'
        case 'KAN':
            return 'KCA'
        case 'LAA':
            return 'ANA'
        case 'LAD':
            return 'LAN'
        case 'SFO':
            return 'SFN'
        case 'CWS':
            return 'CHA'
        case 'TAM':
            return 'TBA'
        case 'NYY':
            return 'NYA'
    
    return team

def setupProxies():
    with open('proxylist.txt', 'r') as f:
        prefix = 'http://'
        for proxy in f:
            proxySplit = proxy.replace('\n', '').split(':');
            proxies.append(prefix + proxySplit[2] + ':' + proxySplit[3] + '@' + proxySplit[0] + ':' + proxySplit[1])

def checkWinner(score1, score2):
    if score1 > score2:
        return 1
    else:
        return -1

def popCheck(list):
    try:
        item = list.pop(0)
        if 'B - ' in item or 'HP - ' in item:
            item = item[5:]
        
        if '(none)' in item:
            return 'N/A';
    
        if 'Wind' in item:
            item = item[6:];

        return item
    except:
        return '';





#actually doing something functions
def getSeasonGameInfo(year):

    gameInfoHeaders = ['Home Team', 'Home Team Record', 'Visitor Team', 'Visitor Team Record', 'Final Score', 'Winner', 'H/V Win', 'Game Time', 'Winning Pitcher', 'Visiting Pitcher', 'Winning Pitcher (Team)', 'Losing Pitcher (Team)', 'Game Time', 'Attendance', 'Field Condition', 'Temperature', 'Wind Direction', 'Cloud Coverage', 'Precipitation', 'HP Umpire', '1B Umpire', '2B Umpire', '3B Umpire', 'LF Umpire', 'RF Umpire']
    HittingHeaders = ['', 'AB', 'R', 'H', 'RBI', 'BB', 'SO', 'PA', 'BA', 'OBP', 'SLG', 'OPS', 'PIT', 'STR', 'WPA', 'aLI', 'WPA+', 'WPA-', 'cWPA', 'acLI', 'RE24', 'PO', 'A', 'Details']
    PitchingHeaders = ['', 'IP', 'H', 'R', 'ER', 'BB', 'SO', 'HR', 'ERA', 'BF', 'PIT', 'STR', 'CTCT', 'STS', 'STL', 'GB', 'FB', 'LD', 'UNK', 'GSC', 'IR', 'IS', 'WPA', 'aLI', 'cWPA', 'acLI', 'RE24']


    proxy = random.choice(proxies)
    gamesList = r.get('https://www.baseball-reference.com/leagues/majors/' + str(year) + '-schedule.shtml', proxies={'http': proxy, 'https': proxy})
    print(gamesList.url + ' ' + str(gamesList) + ' ' + proxy);
    gList = bs(gamesList.text, features='html.parser')
    
    #all_7103833340 - 2022
    dates = gList.find_all('h3') #parent grabs games from date 

    for d in dates:
        gamesFromDate = d.parent.find_all('a') #a tags hold team names and box score (links included)
        gamesFromDate.pop() #removes last link we don't need
        totalGamesFromDate = len(gamesFromDate) / 3 #get total games for date
        print(str(d) + ' - ' + str(totalGamesFromDate));

        q = 0
        while(q < totalGamesFromDate): #till will loop through all the games popping the names of the 3 items: vis, home, boxscore link
            visitor = gamesFromDate.pop(0).text
            home = gamesFromDate.pop(0).text
            gamesFromDate.pop(0).text
            q = q + 1;

            #get data from individual team and save/write to csv or txt whatever is prefferable
            #figure out home team and convert date to create link
            urlNumber = 0
            gameBoxScoreURL = 'https://www.baseball-reference.com/boxes/' + getTeamAbrv(home) + '/' + getTeamAbrv(home) + convertDateURL(d.text) + str(urlNumber) + '.shtml'


            #this is where we pull the juicy information
            #GameInfo Row
            proxy = random.choice(proxies)

            boxScorePage = r.get(gameBoxScoreURL, proxies={'http': proxy, 'https': proxy})
            while boxScorePage.status_code == 404:
                urlNumber = urlNumber + 1
                if urlNumber == 10:
                    print('Page Not Found');
                    sys.exit()

                print('Incorrect Number. Trying again ... ' + str(urlNumber))
                gameBoxScoreURL = 'https://www.baseball-reference.com/boxes/' + getTeamAbrv(home) + '/' + getTeamAbrv(home) + convertDateURL(d.text) + str(urlNumber) + '.shtml'
                boxScorePage = r.get(gameBoxScoreURL, proxies={'http': proxy, 'https': proxy})


            print(gameBoxScoreURL + ' ' + str(boxScorePage) + ' ' + proxy);
            boxScoreInfo = bs(boxScorePage.text, features='html.parser')
            
            #How to get scoring information
            scores = boxScoreInfo.find_all('div', {'class': 'score'})
            visitorScore = scores[0].text;
            homeScore = scores[1].text;
            
            #recordPostGame
            teamRecords = boxScoreInfo.find_all('div', {'class': 'scorebox'})
            
            visitorTeamRecord = teamRecords[0].find_all('div')[0].find_all('div')[4].text;
            homeTeamRecord = teamRecords[0].find_all('div')[7].find_all('div')[4].text;

            #How to get game information
            gameInfo = boxScoreInfo.find_all('div', {'class': 'scorebox_meta'})[0]
            info = gameInfo.find_all('div');

            
            
            
            dateOfGame = info[0].text; #date of game
            firstPitchTime = info[1].text[12:len(info[1].text) - 6]; #game start time
            gameAttendance = info[2].text; #attendance
            gameVenue = info[3].text; #venue
            gameDuration = info[4].text; #game duration

            #Get the box score info per inning
            box = boxScoreInfo.find_all('div', {'class': 'linescore_wrap'})[0]
            inningsInfo = box.find('table').find('thead').find('tr').find_all('th'); #this will be used to know how many innings were played
            
            howManyInningsPlayed = inningsInfo[len(inningsInfo) - 4].text #gets the last inning that was played

            #this has score by inning ex (0, 0, 0, 0, 1, 3, 0, 4)
            visitorScoreByInning = box.find('table').find('tbody').find_all('tr')[0].find_all('td'); #visitor is 0
            visitorScoreByInning.pop(0); visitorScoreByInning.pop(0);
            vsbi = [];
            for v in visitorScoreByInning:
                vsbi.append(v.text);

            homeScoreByInning = box.find('table').find('tbody').find_all('tr')[1].find_all('td'); #home is 0
            homeScoreByInning.pop(0); homeScoreByInning.pop(0);

            hsbi = [];
            for h in homeScoreByInning:
                hsbi.append(h.text);

            #[1] = WinPFname, [2] = WinPLastName, [5] LosePFname, [6] LosePLname
            gamePitchingResults = box.find('table').find('tfoot').find('tr').find('td').text;
            gamePitchingResults = gamePitchingResults.replace('•', '').split();


            #the data loads to the page as a comment so it must be sanitized of comment tags and then put into a new soup obj
            sanitizeThatJoint = boxScorePage.text.replace('<!--', '')
            sanitizeThatJoint = sanitizeThatJoint.replace('-->', '')
            
            with open('The_Sanitizer/sanitized.html', 'w') as f:
                f.write(sanitizeThatJoint);
            #make note to close this process when complete with reading it
            readThatJoint = open('The_Sanitizer/sanitized.html', 'r');    
            tables = bs(readThatJoint, features='html.parser')

            # Some vary in how many rows of otherInfo there are ex https://www.baseball-reference.com/boxes/TBA/TBA202204080.shtml. Will need to grab all the divs and based on length provide information
            otherInfo = tables.find_all('div', {'class': 'section_content'})[2]
            whatsListed = [];
            umpires = [];
            weather = [];
            
            try:    #this is implemented because some games might not contain this data and it will throw an error;
                for o in otherInfo:
                    if 'Umpires' in o.text:
                        umpires = o.text.replace('Umpires: ', '').split(',')
                        continue;
                    elif 'Time of' in o.text:
                        whatsListed.append(o.text.replace('Time of Game: ', '').replace('.', ''))
                        continue
                    elif 'Attendance' in o.text:
                        whatsListed.append(o.text.replace('Attendance: ', '').replace('.', ''))
                    elif 'Field Condition' in o.text:
                        whatsListed.append(o.text.replace('Field Condition: ', '').replace('.', ''))
                    elif 'Start Time Weather' in o.text:
                        weather = o.text.replace('Start Time Weather: ', '').replace('.', '').split(',');
            except:
                print('NO EXTRA GAME DATA');

            

            #0 - ump #1 - game time #2 - attendance, 3 - fieldCondition, 4 - weatherInfo
            #fieldCondition = otherInfo.find_all('div')[3].text.replace('Field Condition: ', '').replace('.', '')
            #weatherInfo = otherInfo.find_all('div')[4].text.replace('Start Time Weather: ', '').replace('.', '').split(',')
            #umpires = otherInfo.find_all('div')[0].text.replace('Umpires: ', '').split(',')
            #attendance = otherInfo.find_all('div')[2].text.replace('Attendance: ', '').replace('.', '')
            



            if home == 'Arizona D\'Backs':
                home = 'Arizona Diamondbacks';
            
            if home == 'St. Louis Cardinals':
                home = 'St Louis Cardinals'
            
            if visitor == 'St. Louis Cardinals':
                visitor = 'St Louis Cardinals';
            
            if visitor == 'Arizona D\'Backs':
                visitor = 'Arizona Diamondbacks';
            

            visitorBattingTable = tables.find(id='div_' + visitor.replace(' ', '') + 'batting').find('table')  #tables.find_all('table')[8];
            vBattingStats = [];
            for rv in visitorBattingTable.find('tbody').find_all('tr'):
                if (rv.has_attr('class')):
                    rv.decompose()
                    continue

                if rv.find('a') is not None:
                    vBattingStats.append(rv.find('a').text)
                
                individualStats = rv.find_all('td');
                for ids in individualStats:
                    if ids.text != '' or len(ids.text) > 0:
                        vBattingStats.append(ids.text)
                    else:
                        vBattingStats.append('-')

            ''' totals weren't working I believe its because they are reusing a bs4 object potentially? Can just try opening another bs object itself and grabbing this individually
            vBattingTotals = tables.find_all('table')[8].find('tfoot').find('tr').find_all('td')
            vBattingStats.append('Team Totals')

            for v in vBattingTotals:
                if v.text != '' or len(v.text) > 0:
                    vBattingStats.append(v.text)
                else:
                    vBattingStats.append('-')
            '''

            

            homeBattingTable = tables.find(id='div_' + home.replace(' ', '') + 'batting').find('table')

            hBattingStats = [];
            for rv in homeBattingTable.find('tbody').find_all('tr'):
                if (rv.has_attr('class')):
                    rv.decompose()
                    continue

                if rv.find('a') is not None:
                    hBattingStats.append(rv.find('a').text)
                
                individualStats = rv.find_all('td');
                for ids in individualStats:
                    if ids.text != '' or len(ids.text) > 0:
                        hBattingStats.append(ids.text)
                    else:
                        hBattingStats.append('-')

            '''
            hBattingTotals = homeBattingTable.find('tfoot').find('tr').find_all('td');
            hBattingStats.append('Team Totals')

            for h in hBattingTotals:
                if h.text != '' or len(h.text) > 0:
                    hBattingStats.append(h.text)
                else:
                    hBattingStats.append('-')
            '''
            
            visitorPitchingTable = tables.find(id='div_' + visitor.replace(' ', '') + 'pitching').find('table')
            vPitchingStats = [];
            for rv in visitorPitchingTable.find('tbody').find_all('tr'):
                if rv.find('a') is not None:
                    vPitchingStats.append(rv.find('a').text)
                
                individualStats = rv.find_all('td');
                for ids in individualStats:
                    if ids.text != '' or len(ids.text) > 0:
                        vPitchingStats.append(ids.text)
                    else:
                        vPitchingStats.append('-')
            
            '''
            vPitchingTotals = visitorPitchingTable.find('tfoot').find('tr').find_all('td');
            vPitchingStats.append('Team Totals')

            for v in vPitchingTotals:
                if v.text != '' or len(v.text) > 0:
                    vPitchingStats.append(v.text)
                else:
                    vPitchingStats.append('-')

            '''


            homePitchingTable = tables.find(id='div_' + home.replace(' ', '') + 'pitching').find('table')
            hPitchingStats = [];
            for rv in homePitchingTable.find('tbody').find_all('tr'):
                if rv.find('a') is not None:
                    hPitchingStats.append(rv.find('a').text)
                
                individualStats = rv.find_all('td');
                for ids in individualStats:
                    if ids.text != '' or len(ids.text) > 0:
                        hPitchingStats.append(ids.text)
                    else:
                        hPitchingStats.append('-')
            
            '''
            hPitchingTotals = homePitchingTable.find('tfoot').find('tr').find_all('td');
            hPitchingStats.append('Team Totals')

            for v in hPitchingTotals:
                if v.text != '' or len(v.text) > 0:
                    hPitchingStats.append(v.text)
                else:
                    hPitchingStats.append('-');
            '''


            #check for directory if it doesn't have one create one - thank you!
            if not os.path.exists('MLB_Box_Scores/' + str(year) + '/' + convertDateFile(d.text)):
                os.makedirs('MLB_Box_Scores/' + str(year) + '/' + convertDateFile(d.text))

            #uncomment this to debug in case a team name/abbr is incorrect or outdated
            #print(visitor); print(getTeamAbrv(visitor)); print(home); print(getTeamAbrv(home));
            fileName = 'MLB_Box_Scores/' + str(year) + '/' + convertDateFile(d.text) + '/' + convertDateFile(d.text) + getTeamAbrv(visitor) + getTeamAbrv(home) + '.csv'

            winner = home if int(homeScore) > int(visitorScore) else visitor
            hv = 'H' if winner == home else 'V'
            loser = visitor if int(homeScore) > int(visitorScore) else home

            with open(fileName, 'w', newline='') as f:
                csv = c.writer(f, delimiter=',')
                csv.writerow(gameInfoHeaders)
                csv.writerow([home, ' ' + homeTeamRecord, visitor, ' ' + visitorTeamRecord, ' ' + visitorScore + '-' + homeScore, winner, hv, firstPitchTime, gamePitchingResults[1] + ' ' + gamePitchingResults[2], gamePitchingResults[5] + ' ' + gamePitchingResults[6], getTeamAbrv(winner), getTeamAbrv(loser), popCheck(whatsListed), popCheck(whatsListed), popCheck(whatsListed), popCheck(weather), popCheck(weather), popCheck(weather), popCheck(umpires), popCheck(umpires), popCheck(umpires), popCheck(umpires), popCheck(umpires), popCheck(umpires)]) 
                csv.writerow(['']); # spacer


                inningHeaders = ['Inning'];
                i = 1
                while i < int(howManyInningsPlayed) + 1:
                    inningHeaders.append(i)
                    i = i + 1
                inningHeaders.append('R')
                inningHeaders.append('H')
                inningHeaders.append('E')
                csv.writerow(inningHeaders) 

               
                vsbi.insert(0, visitor);
                csv.writerow(vsbi);

                hsbi.insert(0, home);
                csv.writerow(hsbi)

                csv.writerow(['']); # spacer


                csv.writerow([visitor + '\'s Batting Statistics']); # spacer
                csv.writerow(HittingHeaders);
                vHittingFormat = [];
                i = 1
                vBRows = (len(vBattingStats) + 1) / 24
                while i < vBRows:
                    csv.writerow([vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0), vBattingStats.pop(0)])
                    i = i + 1

                csv.writerow(['']) # more spacing yikers
                csv.writerow([''])

                csv.writerow([home + '\'s Batting Statistics']); # spacer
                csv.writerow(HittingHeaders);
                hHittingFormat = [];
                i = 1
                hBRows = (len(hBattingStats) + 1) / 24
                while i < hBRows:
                    csv.writerow([hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0), hBattingStats.pop(0)])
                    i = i + 1

                csv.writerow(['']);
                csv.writerow([''])

                csv.writerow([visitor + '\'s Pitching Statistics']); # spacer
                csv.writerow(PitchingHeaders);
                vPitchingFormat = [];
                i = 1
                vPRows = (len(vPitchingStats) + 1) / 27
                while i < vPRows:
                    csv.writerow([vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0), vPitchingStats.pop(0)])
                    i = i + 1

                csv.writerow(['']);
                csv.writerow([''])


                
                csv.writerow([home + '\'s Pitching Statistics']); # spacer
                csv.writerow(PitchingHeaders);
                hPitchingFormat = [];
                i = 1
                hPRows = (len(hPitchingStats) + 1) / 27
                while i < hPRows:
                    csv.writerow([hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0), hPitchingStats.pop(0)])
                    i = i + 1


                csv.writerow(['']);
                csv.writerow(['']);
        
                #sys.exit(); #if you want it to run for one game good for testing
        
        i = 0 #resets for next date
        
def getDepthCharts():
    teamAbrv = ['ari', 'bal', 'bos', 'chc', 'chw', 'cin', 'cle', 'col', 'det', 'hou', 'kc', 'laa', 'lad', 'mia', 'mil', 'min', 'nym', 'nyy', 'oak', 'phi', 'pit', 'sd', 'sf', 'sea', 'stl', 'tb', 'tex', 'tor', 'wsh'];

    for t in teamAbrv:
        espnDepth = r.get('https://www.espn.com/mlb/team/depth/_/name/' + t)
        depthChart = bs(espnDepth.text, features='html.parser')
        table = depthChart.find_all('tbody')[1]
        rows = table.find_all('tr')

        depthList = []
        for pos in rows:
            depth = pos.find_all('td')
            for d in depth:
                depthList.append(d.text);


        if not os.path.exists('MLB_Depth_Charts/' + t):
            os.makedirs('MLB_Depth_Charts/' + t)

        fileName = 'MLB_Depth_Charts/' + t + '/' + str(dt.today())[0:10] + '.csv'

        #We don't need to write anything while we try and figure out the game info
        with open(fileName, 'w', newline='') as f:
            csv = c.writer(f)
            csv.writerow(['P', depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0)])
            csv.writerow(['RP', depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0)])
            csv.writerow(['CL', depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0)])
            csv.writerow(['C', depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0)])
            csv.writerow(['1B', depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0)])
            csv.writerow(['2B', depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0)])
            csv.writerow(['3B', depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0)])
            csv.writerow(['SS', depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0)])
            csv.writerow(['LF', depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0)])
            csv.writerow(['CF', depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0)])
            csv.writerow(['RF', depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0)])
            csv.writerow(['DH', depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0), depthList.pop(0)])

def writeExcel(year):
    #plan is to write one giant csv file, so it contains all information. Will need to open historical odds get that information, then get gameday info individual stats and then write to new file
    print('Writing to File...');
    extractData = [];
    oddResults = [];

    with open('MLB_Historical_Odds/' + str(year) + '.csv', 'r') as h:
        hFile = c.reader(h);
        for line in hFile:
            #line [0] = date
            #line[2] = V/H (visitor is always first)
            #line[3] = team name
            #line[14] = final score
            #line[15] = ml at open
            #line[16] = ml at close
            #line [17] = runline#
            #line[18] = runline odds
            #line[19] = OU open
            #line[20] = OU close
            extractData.append([line[0], line[2], line[3], line[14], line[15], line[16], line[17], line[18], line[19], line[20]])
        
        
        extractData.pop(0);
        i = 0;
        while i < len(extractData):
            vRuns = extractData[i][3];
            hRuns = extractData[i + 1][3];
            
            mlHit = "";
            rlHit = "";
            rlRunDifference = "";
            ouHit = "";
            ouOdds = "";

            if(int(vRuns) > int(hRuns)):
                mlHit = extractData[i][4];
            else:
                mlHit = extractData[i + 1][4];

            if("-" in extractData[i][6]):
                if(float(vRuns) + -1.5 > float(hRuns)):
                    rlHit = extractData[i][7] 
                else:
                    rlHit = extractData[i + 1][7]
            else: 
                if(float(vRuns) + 1.5 > float(hRuns)):
                    rlHit = extractData[i][7] 
                else:
                    rlHit = extractData[i + 1][7]
            
            rlRunDifference = abs(int(vRuns) - int(hRuns));

            if (float(vRuns) + float(hRuns) > float(extractData[i][8])):
                ouHit = "Over";
                ouOdds = extractData[i][9];
            else: 
                ouHit = "Under";
                ouOdds = extractData[i + 1][9];
  
            #this goes date, visitor, home, v ml odds, h ml odds, v runline odds, h runline odds, v over under odds, h over under odds, which ml hit, which run line hit, run difference, which ou hit (over under), which ou odds hits
            oddResults.append([extractData[i][0], extractData[i][2], extractData[i + 1][2], extractData[i][4], extractData[i + 1][4], extractData[i][7], extractData[i + 1][7], extractData[i][8], extractData[i + 1][8],  mlHit, rlHit, str(rlRunDifference), ouHit, ouOdds]);

            i = i + 2;
        
        boxScoreData = [];

        #now we want to open up the game specific csv and pull information from that
        for o in oddResults:
            day = "";
            month = "";
            if(len(o[0]) == 3):
                day = o[0][1:];
                month = o[0][:1];
            else:
                day = o[0][2:];
                month = o[0][:2];     

            if int(day) != 10 and int(day) != 20 and int(day) != 30:
                day = day.replace('0', '');


            dateSearch = month + '-' + day;
            vTeamSearch = o[1];
            hTeamSearch = o[2];

            gameDayDate = str(year) + '-' + dateSearch;
            o.append(gameDayDate);
            
            #o.append('test'); this is where you can add on to the spreadsheet i.e. (MORE CRAZY STATS CALC HERE) will need to do a loop bc append can't use arrays(lists)

            p = 'MLB_Box_Scores/' + str(year) + '/' + str(year) + '-' + dateSearch + '/' + str(year) + '-' + dateSearch + parseTeamOdds(vTeamSearch) + parseTeamOdds(hTeamSearch) + '.csv';
            holder = [];
            #print(p); can use this for debugging for team name


            #this will allow to pull specific details from game
            with open(p, 'r') as file:
                f = c.reader(file);

                line = next(f); #headers
                line2 = next(f);  #game info
                holder = line2;

            #not sure why this s*** was being difficult
            for item in o[3:]:
                holder.append(item);
            boxScoreData.append(holder);
            if len(boxScoreData) > 200:
                break;

        

        with open('TheBigOne/test.csv', 'w', newline='') as f:
            csv = c.writer(f, delimiter=',')
            csv.writerow(['Home Team', 'Home Team Record (After the Game)', 'Visitor Team', 'Visitor Team Record (After the Game)', 'Final Score', 'Winning Team', 'Home/Victory Win', 'Game Time', 'Winning Pitcher', 'Visiting Pitcher', 'Winning Pitcher Team', 'Losing Pitcher Team', 'Game Time (Duration)', 'Attendance', 'Field Conditions', 'Temperature', 'Wind Direction', 'Cloud Coverage', 'HP Umpire', '1B Umpire', '2B Umpire', '3B Umpire', 'LF Umpire', 'RF Umpire', 'Visitor ML', 'Home ML Odds', 'Visitor Runline Odds', 'Home Runline Odds', 'Visitor Over/Under Odds', 'Home Over/Under Odds', 'ML Odds Hit', 'Runline Odds Hit', 'Run Difference', 'Over/Under', 'Over/Under Odds Hit'])
            for data in boxScoreData:
                csv.writerow(data);

        
    



#main and testing below
def testing():
    proxies = [];

    with open ('proxies.txt', 'r') as f:
        proxies = f.read().split('\n');
    
    for p in proxies:
        try:
            request = r.get('https://www.baseball-reference.com/boxes/ANA/ANA202204070.shtml', proxies={'http': p, 'https': p}, timeout=3)
            if request.status_code == 200:
                print(p + ' - WORKED!');
            else:
                print(p + ' ' + str(request.status_code)) 
        except Exception as e:
            print(e)
        

def main():
    setupProxies(); #reads proxies and formats them for requests
    getSeasonGameInfo(2022); #gets every game of the season's box score and game stats
    #getDepthCharts() #gets the team's depth chart from ESPN.com
    #testing(); #test functions of the program
    writeExcel(2022); #combines states with odds
    

main();
