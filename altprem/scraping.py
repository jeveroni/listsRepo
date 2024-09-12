import requests
from bs4 import BeautifulSoup
from .models import Game, Team, Season
from .forms import GameForm
from datetime import datetime

#1- scan season page

#The 2016-17 year would be Year = 16
Year = 24


SeasonResultsUrl = "https://www.skysports.com/premier-league-results/20{:}-{:}".format(Year, Year+1)
StatsPageBaseUrl = "https://www.skysports.com/football/"

def mainScrape():
    print("URL is {:}".format(SeasonResultsUrl))
    ParsedSeasonResults = BeautifulSoup(requests.get(SeasonResultsUrl).content, "html.parser")

    script = ParsedSeasonResults.select_one('[type="text/show-more"]')
    if( script != None ):
        script.replace_with(BeautifulSoup(script.contents[0], "html.parser"))

    div_containing_matches = ParsedSeasonResults.find_all("div", class_="fixres__item")

    for match in div_containing_matches:
        gameId = match.a['data-item-id']
        # at this point we should check if we've already got the game id, and ignore it if so
        if( Game.objects.filter(game_id=gameId).exists()):
            print( "GameId {:} already exists, skipping...".format( gameId ) )
            continue
        
        teams = match.find_all('span', class_="swap-text__target")
        scores = match.find_all( 'span', class_="matches__teamscores-side")
        date = match.find_previous('h4')
        time = match.find( 'span', class_="matches__date")
        year = match.find_previous('h3')
        
        print("GameId is {:}. Home team is {:}. Away team is {:}. Scores are {:}-{:}. Date is {:} {:}. Time is {:}".format(
                        gameId,
                        "-".join(teams[0].text.split()),
                        "-".join(teams[1].text.split()),
                        "".join(scores[0].text.split()), 
                        "".join(scores[1].text.split()), 
                        "{:} {:}".format("".join(x for x in date.text if x.isdigit()), 
                            year.text),
                        "".join(time.text.split()),
                        "{:}-{:}".format( Year, Year+1 ) ))
        
        createdGame = Game( game_id = gameId )
        homeScore = int( scores[0].text.split()[0] )
        awayScore = int( scores[1].text.split()[0] )
        createdGame.home_score = homeScore
        createdGame.away_score = awayScore
        #Datetime stuff, work that out later?
        homeTeam, created = Team.objects.get_or_create(name="-".join(teams[0].text.split()))
        createdGame.home_team = homeTeam
        awayTeam, created = Team.objects.get_or_create(name="-".join(teams[1].text.split()))
        createdGame.away_team = awayTeam
        
        datetime_object = datetime.strptime( 
                            "{:} {:} {:}".format("".join(x for x in date.text if x.isdigit()), year.text, "".join(time.text.split())),
                            '%d %B %Y %H:%M')
        createdGame.match_date = datetime_object
        
        StatsPageUrl = "{:}{:}-vs-{:}/stats/{:}".format( StatsPageBaseUrl,
                                            "-".join(teams[0].text.split()),
                                            "-".join(teams[1].text.split()),
                                            gameId)
        StatsPage = requests.get(StatsPageUrl)
        ParsedStatsPage = BeautifulSoup(StatsPage.content, "html.parser")
        
        matchStats = ParsedStatsPage.find_all("div", class_= "sdc-site-match-stats__stats")
        
        # # #7- write csv for that specific stat and the data
        for matchStat in matchStats:
            handleMatchStatDiv( createdGame, matchStat )
        
        season, created = Season.objects.get_or_create(name="{:}-{:}".format( Year, Year+1 ))
        createdGame.season= season

        createdGame.save()
        
        
        
    print("Finished scraping")


#-------------------------------
#psudo code (Might help give an idea for functions to make it readable)
#1- scan season page
#2- get list of div elements for fixres__item, should contain every match
#3- for each of these divs, store the gameId, homeTeam, awayTeam, Date (Whether month + day, or another format)
#4- write to gameCsvXX-XX file
#5- call function to get parse page based off gameId and teams
#6- for each div sdc-site-match-stats__stats, use the previous sibling to get the specific stat, and the value for home and away team
#7- write csv for that specific stat and the data

#-------------------------------
#Things to consider:
#1- When mucking about with csv's, will it overwrite things by opening constantly?- A: Can use append rather than write! 'a' not 'w'
#2- Would it be better to make the csv files at startup, and if the names can't be found then don't fill in?
#This would cover any extra dvi's appearing at any point


#-------------------------------
#Lets do the code then


#declarations
#-------------------------------

# gameInfoCsvHeader = ['gameId', 'homeTeam', 'awayTeam', 'homeScore', 'awayScore', 'date', 'time', 'season']
# possessionCsvHeader = ['gameId', 'homePossession', 'awayPossession']
# totalShotsCsvHeader = ['gameId', 'homeTotalShots', 'awayTotalShots']
# onTargetCsvHeader = ['gameId', 'homeOnTarget', 'awayOnTarget']
# offTargetCsvHeader = ['gameId', 'homeOffTarget', 'awayOffTarget']
# blockedCsvHeader = ['gameId', 'homeBlocked', 'awayBlocked']
# passingCsvHeader = ['gameId', 'homePassing', 'awayPassing']
# clearCutChancesCsvHeader = ['gameId', 'homeClearCutChances', 'awayClearCutChances']
# cornersCsvHeader = ['gameId', 'homeCorners', 'awayCorners']
# offsidesCsvHeader = ['gameId', 'homeOffsides', 'awayOffsides']
# tacklesCsvHeader = ['gameId', 'homeTackles', 'awayTackles']
# aerialDuelsCsvHeader = ['gameId', 'homeAerialDuels', 'awayAerialDuels']
# savesCsvHeader = ['gameId', 'homeSaves', 'awaySaves']
# foulsCommittedCsvHeader = ['gameId', 'homeFoulsCommitted', 'awayFoulsCommitted']
# foulsWonCsvHeader = ['gameId', 'homeFoulsWon', 'awayFoulsWon']
# yellowCardsCsvHeader = ['gameId', 'homeYellowCards', 'awayYellowCards']
# redCardsCsvHeader = ['gameId', 'homeRedCards', 'awayRedCards']


# #functions
# #-------------------------------

# #Match div functions
# def getGameIdFromMatchDiv( match ):
#     return match.a['data-item-id']

# def getTeamsFromMatchDiv( match ):
#     return match.find_all('span', class_="swap-text__target")

# def getScoresFromMatchDiv( match ):
#     return match.find_all( 'span', class_="matches__teamscores-side")

# def getDateFromMatchDiv( match ):
#     return match.find_previous('h4')

# def getTimeFromMatchDiv( match ):
#     return match.find( 'span', class_="matches__date")

# def getYearFromMatchDiv( match ):
#     return match.find_previous('h3')

# #Csv writing functions
# def setupAllCsvFiles():
#     setupGameInfoCsv()
#     setupPossessionCsv()
#     setupTotalShotsCsv()
#     setupOnTargetCsv()
#     setupOffTargetCsv()
#     setupBlockedCsv()
#     setupPassingCsv()
#     setupClearCutChancesCsv()
#     setupCornersCsv()
#     setupOffsidesCsv()
#     setupTacklesCsv()
#     setupAerialDuelsCsv()
#     setupSavesCsv()
#     setupFoulsCommittedCsv()
#     setupFoulsWonCsv()
#     setupYellowCardsCsv()
#     setupRedCardsCsv()
    
# def setupGameInfoCsv():
#     with open('{:}-{:}/{:}-{:}_gameInfo.csv'.format(Year, Year+1, Year, Year+1), 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(gameInfoCsvHeader)

# def addToGameInfoCsv( gameId, homeTeam, awayTeam, homeScore, awayScore, date, time, season ):
#     with open('{:}-{:}/{:}-{:}_gameInfo.csv'.format(Year, Year+1, Year, Year+1), 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([gameId, homeTeam, awayTeam, homeScore, awayScore, date, time, season])
        
# def setupPossessionCsv():
#     with open('{:}-{:}/{:}-{:}_possession.csv'.format(Year, Year+1, Year, Year+1), 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(possessionCsvHeader)

# def addToPossessionCsv( gameId, homePossession, awayPossession ):
#     with open('{:}-{:}/{:}-{:}_possession.csv'.format(Year, Year+1, Year, Year+1), 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([gameId, homePossession, awayPossession])
        
# def setupTotalShotsCsv():
#     with open('{:}-{:}/{:}-{:}_totalShots.csv'.format(Year, Year+1, Year, Year+1), 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(totalShotsCsvHeader)

# def addToTotalShotsCsv( gameId, homeTotalShots, awayTotalShots ):
#     with open('{:}-{:}/{:}-{:}_totalShots.csv'.format(Year, Year+1, Year, Year+1), 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([gameId, homeTotalShots, awayTotalShots])
        
# def setupOnTargetCsv():
#     with open('{:}-{:}/{:}-{:}_onTarget.csv'.format(Year, Year+1, Year, Year+1), 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(onTargetCsvHeader)

# def addToOnTargetCsv( gameId, homeOnTarget, awayOnTarget ):
#     with open('{:}-{:}/{:}-{:}_onTarget.csv'.format(Year, Year+1, Year, Year+1), 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([gameId, homeOnTarget, awayOnTarget])
        
# def setupOffTargetCsv():
#     with open('{:}-{:}/{:}-{:}_offTarget.csv'.format(Year, Year+1, Year, Year+1), 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(offTargetCsvHeader)

# def addToOffTargetCsv( gameId, homeOffTarget, awayOffTarget ):
#     with open('{:}-{:}/{:}-{:}_offTarget.csv'.format(Year, Year+1, Year, Year+1), 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([gameId, homeOffTarget, awayOffTarget])
        
# def setupBlockedCsv():
#     with open('{:}-{:}/{:}-{:}_blocked.csv'.format(Year, Year+1, Year, Year+1), 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(blockedCsvHeader)

# def addToBlockedCsv( gameId, homeBlocked, awayBlocked ):
#     with open('{:}-{:}/{:}-{:}_blocked.csv'.format(Year, Year+1, Year, Year+1), 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([gameId, homeBlocked, awayBlocked])
        
# def setupPassingCsv():
#     with open('{:}-{:}/{:}-{:}_passing.csv'.format(Year, Year+1, Year, Year+1), 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(passingCsvHeader)

# def addToPassingCsv( gameId, homePassing, awayPassing ):
#     with open('{:}-{:}/{:}-{:}_passing.csv'.format(Year, Year+1, Year, Year+1), 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([gameId, homePassing, awayPassing])
        
# def setupClearCutChancesCsv():
#     with open('{:}-{:}/{:}-{:}_clearCutChances.csv'.format(Year, Year+1, Year, Year+1), 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(clearCutChancesCsvHeader)

# def addToClearCutChancesCsv( gameId, homeClearCutChances, awayClearCutChances ):
#     with open('{:}-{:}/{:}-{:}_clearCutChances.csv'.format(Year, Year+1, Year, Year+1), 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([gameId, homeClearCutChances, awayClearCutChances])
        
# def setupCornersCsv():
#     with open('{:}-{:}/{:}-{:}_corners.csv'.format(Year, Year+1, Year, Year+1), 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(cornersCsvHeader)

# def addToCornersCsv( gameId, homeCorners, awayCorners ):
#     with open('{:}-{:}/{:}-{:}_corners.csv'.format(Year, Year+1, Year, Year+1), 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([gameId, homeCorners, awayCorners])
        
# def setupOffsidesCsv():
#     with open('{:}-{:}/{:}-{:}_offsides.csv'.format(Year, Year+1, Year, Year+1), 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(offsidesCsvHeader)

# def addToOffsidesCsv( gameId, homeOffsides, awayOffsides ):
#     with open('{:}-{:}/{:}-{:}_offsides.csv'.format(Year, Year+1, Year, Year+1), 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([gameId, homeOffsides, awayOffsides])
        
# def setupTacklesCsv():
#     with open('{:}-{:}/{:}-{:}_tackles.csv'.format(Year, Year+1, Year, Year+1), 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(tacklesCsvHeader)

# def addToTacklesCsv( gameId, homeTackles, awayTackles ):
#     with open('{:}-{:}/{:}-{:}_tackles.csv'.format(Year, Year+1, Year, Year+1), 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([gameId, homeTackles, awayTackles])
        
# def setupAerialDuelsCsv():
#     with open('{:}-{:}/{:}-{:}_aerialDuels.csv'.format(Year, Year+1, Year, Year+1), 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(aerialDuelsCsvHeader)

# def addToAerialDuelsCsv( gameId, homeAerialDuels, awayAerialDuels ):
#     with open('{:}-{:}/{:}-{:}_aerialDuels.csv'.format(Year, Year+1, Year, Year+1), 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([gameId, homeAerialDuels, awayAerialDuels])
        
# def setupSavesCsv():
#     with open('{:}-{:}/{:}-{:}_saves.csv'.format(Year, Year+1, Year, Year+1), 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(savesCsvHeader)

# def addToSavesCsv( gameId, homeSaves, awaySaves ):
#     with open('{:}-{:}/{:}-{:}_saves.csv'.format(Year, Year+1, Year, Year+1), 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([gameId, homeSaves, awaySaves])
        
# def setupFoulsCommittedCsv():
#     with open('{:}-{:}/{:}-{:}_foulsCommitted.csv'.format(Year, Year+1, Year, Year+1), 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(foulsCommittedCsvHeader)

# def addToFoulsCommittedCsv( gameId, homeFoulsCommitted, awayFoulsCommitted ):
#     with open('{:}-{:}/{:}-{:}_foulsCommitted.csv'.format(Year, Year+1, Year, Year+1), 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([gameId, homeFoulsCommitted, awayFoulsCommitted])
        
# def setupFoulsWonCsv():
#     with open('{:}-{:}/{:}-{:}_foulsWon.csv'.format(Year, Year+1, Year, Year+1), 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(foulsWonCsvHeader)

# def addToFoulsWonCsv( gameId, homeFoulsWon, awayFoulsWon ):
#     with open('{:}-{:}/{:}-{:}_foulsWon.csv'.format(Year, Year+1, Year, Year+1), 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([gameId, homeFoulsWon, awayFoulsWon])
        
# def setupYellowCardsCsv():
#     with open('{:}-{:}/{:}-{:}_yellowCards.csv'.format(Year, Year+1, Year, Year+1), 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(yellowCardsCsvHeader)

# def addToYellowCardsCsv( gameId, homeYellowCards, awayYellowCards ):
#     with open('{:}-{:}/{:}-{:}_yellowCards.csv'.format(Year, Year+1, Year, Year+1), 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([gameId, homeYellowCards, awayYellowCards])
        
# def setupRedCardsCsv():
#     with open('{:}-{:}/{:}-{:}_redCards.csv'.format(Year, Year+1, Year, Year+1), 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(redCardsCsvHeader)

# def addToRedCardsCsv( gameId, homeRedCards, awayRedCards ):
#     with open('{:}-{:}/{:}-{:}_redCards.csv'.format(Year, Year+1, Year, Year+1), 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([gameId, homeRedCards, awayRedCards])
    
#Handling match statistics
def handleMatchStatDiv( createdGame, matchStatDiv ):
    statisticString = matchStatDiv.find_previous('h5').text
    if( statisticString == "Possession %"):
        handlePossessionStatistic( createdGame, matchStatDiv )
    elif( statisticString == "Total Shots"):
        handleTotalShotsStatistic( createdGame, matchStatDiv )
    elif( statisticString == "On Target"):
        handleOnTargetStatistic( createdGame, matchStatDiv )
    elif( statisticString == "Off Target"):
        handleOffTargetStatistic( createdGame, matchStatDiv )
    elif( statisticString == "Blocked"):
        handleBlockedStatistic( createdGame, matchStatDiv )
    elif( statisticString == "Passing %"):
        handlePassingStatistic( createdGame, matchStatDiv )
    elif( statisticString == "Clear-Cut Chances"):
        handleClearCutChancesStatistic( createdGame, matchStatDiv )
    elif( statisticString == "Corners"):
        handleCornersStatistic( createdGame, matchStatDiv )
    elif( statisticString == "Offsides"):
        handleOffsidesStatistic( createdGame, matchStatDiv )
    elif( statisticString == "Tackles %"):
        handleTacklesStatistic( createdGame, matchStatDiv )
    elif( statisticString == "Aerial Duels %"):
        handleAerialDuelsStatistic( createdGame, matchStatDiv )
    elif( statisticString == "Saves"):
        handleSavesStatistic( createdGame, matchStatDiv )
    elif( statisticString == "Fouls Committed"):
        handleFoulsCommittedStatistic( createdGame, matchStatDiv )
    elif( statisticString == "Fouls Won"):
        handleFoulsWonStatistic( createdGame, matchStatDiv )
    elif( statisticString == "Yellow Cards"):
        handleYellowCardsStatistic( createdGame, matchStatDiv )
    elif( statisticString == "Red Cards"):
        handleRedCardsStatistic( createdGame, matchStatDiv )
    else:
        print("No CSV file for for stastistic: {:}".format(statisticString))
        
def handlePossessionStatistic( createdGame, matchStatDiv ):
    statisticValues = matchStatDiv.find_all("span", class_="sdc-site-match-stats__val")
    createdGame.home_possession = float(statisticValues[0].text)
    createdGame.away_possession = float(statisticValues[1].text)
    return
            
def handleTotalShotsStatistic( createdGame, matchStatDiv ):
    statisticValues = matchStatDiv.find_all("span", class_="sdc-site-match-stats__val")
    createdGame.home_total_shots = int(statisticValues[0].text)
    createdGame.away_total_shots = int(statisticValues[1].text)
    
def handleOnTargetStatistic( createdGame, matchStatDiv ):
    statisticValues = matchStatDiv.find_all("span", class_="sdc-site-match-stats__val")
    createdGame.home_on_target = int(statisticValues[0].text)
    createdGame.away_on_target = int(statisticValues[1].text)
    
def handleOffTargetStatistic( createdGame, matchStatDiv ):
    statisticValues = matchStatDiv.find_all("span", class_="sdc-site-match-stats__val")
    createdGame.home_off_target = int(statisticValues[0].text)
    createdGame.away_off_target = int(statisticValues[1].text)
    
def handleBlockedStatistic( createdGame, matchStatDiv ):
    statisticValues = matchStatDiv.find_all("span", class_="sdc-site-match-stats__val")
    createdGame.home_blocked = int(statisticValues[0].text)
    createdGame.away_blocked = int(statisticValues[1].text)
    
def handlePassingStatistic( createdGame, matchStatDiv ):
    statisticValues = matchStatDiv.find_all("span", class_="sdc-site-match-stats__val")
    createdGame.home_passing_percent = float(statisticValues[0].text)
    createdGame.away_passing_percent = float(statisticValues[1].text)
    
def handleClearCutChancesStatistic( createdGame, matchStatDiv ):
    statisticValues = matchStatDiv.find_all("span", class_="sdc-site-match-stats__val")
    createdGame.home_clear_cut_chances = int(statisticValues[0].text)
    createdGame.away_clear_cut_chances = int(statisticValues[1].text)
    
def handleCornersStatistic( createdGame, matchStatDiv ):
    statisticValues = matchStatDiv.find_all("span", class_="sdc-site-match-stats__val")
    createdGame.home_corners = int(statisticValues[0].text)
    createdGame.away_corners = int(statisticValues[1].text)
    
def handleOffsidesStatistic( createdGame, matchStatDiv ):
    statisticValues = matchStatDiv.find_all("span", class_="sdc-site-match-stats__val")
    createdGame.home_offsides = int(statisticValues[0].text)
    createdGame.away_offsides = int(statisticValues[1].text)
    
def handleTacklesStatistic( createdGame, matchStatDiv ):
    statisticValues = matchStatDiv.find_all("span", class_="sdc-site-match-stats__val")
    createdGame.home_tackles = float(statisticValues[0].text)
    createdGame.away_tackles = float(statisticValues[1].text)
    
def handleAerialDuelsStatistic( createdGame, matchStatDiv ):
    statisticValues = matchStatDiv.find_all("span", class_="sdc-site-match-stats__val")
    createdGame.home_aerial_duels = float(statisticValues[0].text)
    createdGame.away_aerial_duels = float(statisticValues[1].text)
    
def handleSavesStatistic( createdGame, matchStatDiv ):
    statisticValues = matchStatDiv.find_all("span", class_="sdc-site-match-stats__val")
    createdGame.home_saves = int(statisticValues[0].text)
    createdGame.away_saves = int(statisticValues[1].text)
    
def handleFoulsCommittedStatistic( createdGame, matchStatDiv ):
    statisticValues = matchStatDiv.find_all("span", class_="sdc-site-match-stats__val")
    createdGame.home_fouls_committed = int(statisticValues[0].text)
    createdGame.away_fouls_committed = int(statisticValues[1].text)
    
def handleFoulsWonStatistic( createdGame, matchStatDiv ):
    statisticValues = matchStatDiv.find_all("span", class_="sdc-site-match-stats__val")
    createdGame.home_fouls_won = int(statisticValues[0].text)
    createdGame.away_fouls_won = int(statisticValues[1].text)
    
def handleYellowCardsStatistic( createdGame, matchStatDiv ):
    statisticValues = matchStatDiv.find_all("span", class_="sdc-site-match-stats__val")
    createdGame.home_yellow_cards = int(statisticValues[0].text)
    createdGame.away_yellow_cards = int(statisticValues[1].text)
    
def handleRedCardsStatistic( createdGame, matchStatDiv ):
    statisticValues = matchStatDiv.find_all("span", class_="sdc-site-match-stats__val")
    createdGame.home_red_cards = int(statisticValues[0].text)
    createdGame.away_red_cards = int(statisticValues[1].text)
# #-------------------------------
# #1- scan season page

# #The 2016-17 year would be Year = 16
# Year = 24


# SeasonResultsUrl = "https://www.skysports.com/premier-league-results/20{:}-{:}".format(Year, Year+1)
# print("URL is {:}".format(SeasonResultsUrl))
# # SeasonResultsPage = requests.get(SeasonResultsUrl)
# # ParsedSeasonResults = BeautifulSoup(SeasonResultsPage.content, "html.parser")

# # Show more button has appeared, unsure on how to get around it just yet but seen something on stack overflow
# ParsedSeasonResults = BeautifulSoup(requests.get(SeasonResultsUrl).content, "html.parser")

# script = ParsedSeasonResults.select_one('[type="text/show-more"]')
# script.replace_with(BeautifulSoup(script.contents[0], "html.parser"))


# #2- get list of div elements for fixres__item, should contain every match
# div_containing_matches = ParsedSeasonResults.find_all("div", class_="fixres__item")

# #2.5- create csv files, and make headers for them
# setupAllCsvFiles()

# #3- for each of these divs, store the gameId, homeTeam, awayTeam, Date (Whether month + day, or another format)
# for match in div_containing_matches:
#     #note, it could be good to subroutine how to find all of these from the div, as then if it does change in future you can pinpoint where to change stuff
#     gameId = getGameIdFromMatchDiv(match)
#     teams = getTeamsFromMatchDiv(match)
#     scores = getScoresFromMatchDiv(match)
#     date = getDateFromMatchDiv(match)
#     time = getTimeFromMatchDiv(match)
#     year = getYearFromMatchDiv(match)
    
#     #4- write to gameCsvXX-XX file
#     #upon review, I think ideally we want the variables to just hold the text. Let the functions do the fucking about
#     addToGameInfoCsv(gameId,
#                      "-".join(teams[0].text.split()),
#                      "-".join(teams[1].text.split()),
#                      "".join(scores[0].text.split()), 
#                      "".join(scores[1].text.split()), 
#                      "{:} {:}".format("".join(x for x in date.text if x.isdigit()), 
#                            year.text),
#                      "".join(time.text.split()),
#                      "{:}-{:}".format( Year, Year+1 ) )

#     #5- call function to get parse page based off gameId and teams
#     StatsPageBaseUrl = "https://www.skysports.com/football/"
#     StatsPageUrl = "{:}{:}-vs-{:}/stats/{:}".format( StatsPageBaseUrl,
#                                         "-".join(teams[0].text.split()),
#                                         "-".join(teams[1].text.split()),
#                                         gameId)
#     StatsPage = requests.get(StatsPageUrl)
#     ParsedStatsPage = BeautifulSoup(StatsPage.content, "html.parser")
    
#     #6- for each div sdc-site-match-stats__stats, use the previous sibling to get the specific stat, and the value for home and away team
#     matchStats = ParsedStatsPage.find_all("div", class_= "sdc-site-match-stats__stats")
    
#     #7- write csv for that specific stat and the data
#     for matchStat in matchStats:
#         handleMatchStatDiv( gameId, matchStat )
# print("Finished scraping")