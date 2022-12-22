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

def main():
    get_team_names()

    teamColors = [[0 for i in range(2)] for j in range(len(teamNames))]
    playerInfos = [[str(), list(), list(), list(), list(), list(), list()] for j in range(len(teamNames))]

if __name__ == "__main__":
    main()