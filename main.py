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


def main():
    get_team_names()

    teamColors = [[0 for i in range(2)] for j in range(len(teamNames))]
    playerInfos = [[str(), list(), list(), list(), list(), list(), list()] for j in range(len(teamNames))]

    get_team_colors(teamColors)

if __name__ == "__main__":
    main()