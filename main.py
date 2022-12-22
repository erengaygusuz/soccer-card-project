import requests
import random
import pathlib
import urllib.request
import os.path
from lxml import etree
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

playerNames = []
playerNos = []
playerImageLinks = []
teamNames = []
teamIds = []

def get_team_names():

    leagueLinkAddress = 'https://www.transfermarkt.com.tr/super-lig/startseite/wettbewerb/TR1'

    leagueTreeResponse = requests.get(leagueLinkAddress, headers=headers)
    soupLeague = BeautifulSoup(leagueTreeResponse.content, 'html.parser')

    teamNamesTree = (etree.HTML(str(soupLeague)).xpath('/html/body/div[2]/main/div[2]/div[1]/div[2]/div[2]/div/table/tbody/tr'))

    for i in range(len(teamNamesTree)):

        if teamNamesTree[i].xpath('td[2]/a')[0].text != '':
            teamNames.append(teamNamesTree[i].xpath('td[2]/a/@href')[0].split('/')[1])
            teamIds.append(teamNamesTree[i].xpath('td[2]/a/@href')[0].split('/')[4])

def get_team_colors(teamColors):

    for i in range(len(teamNames)):

        temaColorUrl = 'https://www.transfermarkt.com.tr/' + teamNames[i] + '/datenfakten/verein/' + teamIds[i]

        tree = requests.get(temaColorUrl, headers=headers)
        soup = BeautifulSoup(tree.content, 'html.parser')

        arr = soup.findAll('p', class_='vereinsfarbe')

        if len(arr) == 0:
            randomColor1 = ("#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])).lstrip('#')
            randomColor2 = ("#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])).lstrip('#')

            teamColors[i][0] = tuple(int(randomColor1[i:i + 2], 16) for i in (0, 2, 4))
            teamColors[i][1] = tuple(int(randomColor2[i:i + 2], 16) for i in (0, 2, 4))

        else:
            h1 = arr[0].findAll('span')[0]["style"].split(':')[1].rstrip(";").lstrip('#')
            h2 = arr[0].findAll('span')[1]["style"].split(':')[1].rstrip(";").lstrip('#')

            teamColors[i][0] = tuple(int(h1[i:i + 2], 16) for i in (0, 2, 4))
            teamColors[i][1] = tuple(int(h2[i:i + 2], 16) for i in (0, 2, 4))

def get_player_datas(playerInfos):

    for i in range(len(teamNames)):

        playerNames.clear()
        playerImageLinks.clear()
        playerNos.clear()

        page = 'https://www.transfermarkt.com.tr/' + teamNames[i] + '/startseite/verein/' + teamIds[i]

        tree = requests.get(page, headers=headers)
        soup = BeautifulSoup(tree.content, 'html.parser')

        playerInfos[i][0] = teamNames[i]

        players = soup.findAll('img', class_='bilderrahmen-fixed')

        for j in range(len(players)):
            if players[j]['title'] != '':
                playerNames.append(players[j]['title'].replace(" ", "-").lower())

                playerLink = soup.find('a', attrs={'title':players[j]['title']})

                pagePlayerInfo = 'https://www.transfermarkt.com.tr' + playerLink.findNext('a')['href']
                treePlayerInfo = requests.get(pagePlayerInfo, headers=headers)
                soupPlayerInfo = BeautifulSoup(treePlayerInfo.content, 'html.parser')

                playerName = players[j]['title']

                playerAge = soupPlayerInfo.find('span',attrs={'class':'data-header__content', 'itemprop':'birthDate'}).text.replace(" ", "").split('(')[1][:2]

                number = soupPlayerInfo.find('span',attrs={'class':'data-header__shirt-number'})
                randomNumber = random.randint(0, 99)

                while randomNumber in playerNos:
                    randomNumber = random.randint(0, 99)

                playerNos.append(randomNumber)
                strNumber = number.text.replace(" ", "")[2:] if number is not None else str(randomNumber)
                playerNumber = strNumber

                value = soupPlayerInfo.find('a',attrs={'class':'data-header__market-value-wrapper'})
                randomValue = random.randint(50000, 15000000)
                strValue = value.text.split('€')[0] if value is not None else str(randomValue)
                playerValue = strValue + "€"

                height = soupPlayerInfo.find('span',attrs={'class':'data-header__content', 'itemprop':'height'})
                playerHeight = height.text if height is not None else str(round(random.uniform(1.6, 2.0), 2)) + " m"
                strHeight = playerHeight.replace(" ", "").replace("m", "").replace(",", "").replace(".", "")

                playerWeight = str(round(calculate_age_constant(int(playerAge)) * (int(strHeight) - 105))) + " kg"

                playerInfos[i][1].append(playerName)
                playerInfos[i][2].append(playerAge)
                playerInfos[i][3].append(playerNumber)
                playerInfos[i][4].append(playerValue)
                playerInfos[i][5].append(playerHeight)
                playerInfos[i][6].append(playerWeight)

        for playerImageLink in soup.findAll('img', class_='bilderrahmen-fixed'):

            playerImageLinks.append(playerImageLink['data-src'].replace("small", "header"))

        for j in range(len(playerNames)):

            path = "E:\\ProjectFiles\\PythonProjects\\CardProject\\output-photos\\player-photos\\" + teamNames[i] + "\\"

            if not os.path.isdir(path):
                pathlib.Path(path).mkdir(parents=True, exist_ok=True)

            urllib.request.urlretrieve(playerImageLinks[j], path + playerNames[j] + '.png')

def calculate_age_constant(ageValue):
    if ageValue < 15:
        return 0.9
    elif ageValue >= 15 and ageValue < 20:
        return 0.95
    elif ageValue >= 20 and ageValue < 25:
        return 1.00
    elif ageValue >= 25 and ageValue < 30:
        return 1.00
    elif ageValue >= 30 and ageValue < 35:
        return 1.00
    elif ageValue >= 35 and ageValue < 40:
        return 1.05
    else:
        return 1.1



def main():
    get_team_names()

    teamColors = [[0 for i in range(2)] for j in range(len(teamNames))]
    playerInfos = [[str(), list(), list(), list(), list(), list(), list()] for j in range(len(teamNames))]

    get_team_colors(teamColors)
    get_player_datas(playerInfos)
    
if __name__ == "__main__":
    main()