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

def get_team_names_and_ids():

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

                age = soupPlayerInfo.find('span',attrs={'class':'data-header__content', 'itemprop':'birthDate'})
                randomAge = random.randint(15, 39)
                strAge = age.text.replace(" ", "").split('(')[1][:2] if age is not None else str(randomAge)
                playerAge = strAge

                number = soupPlayerInfo.find('span',attrs={'class':'data-header__shirt-number'})
                randomNumber = random.randint(0, 99)

                while randomNumber in playerNos:
                    randomNumber = random.randint(0, 99)

                playerNos.append(randomNumber)
                strNumber = number.text.replace(" ", "")[2:] if number is not None else str(randomNumber)
                playerNumber = strNumber

                value = soupPlayerInfo.find('a',attrs={'class':'data-header__market-value-wrapper'})

                thousandOrMillion = random.randint(0, 1)

                if thousandOrMillion == 1:
                    randomValue = random.randint(50, 999)
                    strValue = value.text.split('€')[0] if value is not None else str(randomValue) + " Bin "
                else:
                    randomValue = random.randint(1, 15)
                    strValue = value.text.split('€')[0] if value is not None else str(randomValue) + ".00 mil. "

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

            absolute_path = os.path.dirname(__file__)
            relative_path = "output-photos\\player-photos\\" + teamNames[i] + "\\"
            full_path = os.path.join(absolute_path, relative_path)

            if not os.path.isdir(full_path):
                pathlib.Path(full_path).mkdir(parents=True, exist_ok=True)

            urllib.request.urlretrieve(playerImageLinks[j], full_path + playerNames[j] + '.png')

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

def create_team_card_templates(teamColors):

    for i in range(len(teamNames)):

        absolute_path = os.path.dirname(__file__)

        flag_inside1 = Image.open(absolute_path + "\\base-photos\\flag-inside-1.png")
        flag_inside2 = Image.open(absolute_path + "\\base-photos\\flag-inside-2.png")
        inline_border = Image.open(absolute_path + "\\base-photos\\inline-border.png")

        new_image1 = []
        new_image2 = []
        new_image3 = []

        flag_inside1 = flag_inside1.convert("RGBA")
        flag_inside2 = flag_inside2.convert("RGBA")
        inline_border = inline_border.convert("RGBA")

        d1 = flag_inside1.getdata()
        d2 = flag_inside2.getdata()
        d3 = inline_border.getdata()

        color1 = teamColors[i][0]
        color2 = teamColors[i][1]

        for item in d1:

            if item[0] in list(range(200, 256)):
                new_image1.append(color1)
            else:
                new_image1.append(item)

        for item in d2:

            if item[0] in list(range(200, 256)):
                new_image2.append(color2)
            else:
                new_image2.append(item)

        for item in d3:

            if item[0] in list(range(200, 256)):
                new_image3.append(color1)
            else:
                new_image3.append(item)

        flag_inside1.putdata(new_image1)
        flag_inside2.putdata(new_image2)
        inline_border.putdata(new_image3)

        relative_path = "output-photos\\team-templates\\" + teamNames[i] + "\\"
        full_path = os.path.join(absolute_path, relative_path)

        if not os.path.isdir(full_path):
            pathlib.Path(full_path).mkdir(parents=True, exist_ok=True)

        flag_inside1.save(full_path + "flag-inside1.png")

        flag_inside2.save(full_path + "flag-inside2.png")

        inline_border.save(full_path + "inline-border.png")

def generate_team_cards(playerInfos):

    for i in range(len(playerInfos)):

        for j in range(len(playerInfos[i][1])):

            absolute_path = os.path.dirname(__file__)

            background = Image.open(absolute_path + "\\base-photos\\background.png")
            base_info = Image.open(absolute_path + "\\base-photos\\base-info.png")
            flag_border = Image.open(absolute_path + "\\base-photos\\flag-border.png")

            flag_inside1 = Image.open(absolute_path + "\\output-photos\\team-templates\\" + playerInfos[i][0] + "\\" + "flag-inside1.png")
            flag_inside2 = Image.open(absolute_path + "\\output-photos\\team-templates\\" + playerInfos[i][0] + "\\" + "flag-inside2.png")
            inline_border = Image.open(absolute_path + "\\output-photos\\team-templates\\" + playerInfos[i][0] + "\\" + "inline-border.png")

            photo = Image.open(absolute_path + "\\output-photos\\player-photos\\" + playerInfos[i][0] + "\\" + playerInfos[i][1][j].replace(" ", "-").lower() + ".png")

            photo = photo.resize((550, 700))

            im = Image.new(mode="RGBA", size=(background.width, background.height))

            im.paste(photo, (150, 110))

            relative_path = "output-photos\\resized-player-photos\\" + playerInfos[i][0] + "\\"

            full_path = os.path.join(absolute_path, relative_path)

            if not os.path.isdir(full_path):
                pathlib.Path(full_path).mkdir(parents=True, exist_ok=True)

            im.save(full_path + playerInfos[i][1][j].replace(" ", "-").lower() + ".png")

            photo = Image.open(full_path + playerInfos[i][1][j].replace(" ", "-").lower() + ".png")

            img1 = Image.alpha_composite(background, photo)
            img2 = Image.alpha_composite(img1, base_info)
            img3 = Image.alpha_composite(img2, inline_border)
            img4 = Image.alpha_composite(img3, flag_inside1)
            img5 = Image.alpha_composite(img4, flag_inside2)
            img6 = Image.alpha_composite(img5, flag_border)

            i1 = ImageDraw.Draw(img6)

            nameFont = ImageFont.truetype(absolute_path + '\\fonts\\arial-narrow.ttf', 60)
            infoFont = ImageFont.truetype(absolute_path + '\\fonts\\UniversalisADFStd-CondItalic.otf', 53)
            numberFont = ImageFont.truetype(absolute_path + '\\fonts\\arial.ttf', 60)

            name = playerInfos[i][1][j]

            age = playerInfos[i][2][j]
            weight = playerInfos[i][6][j]
            height = playerInfos[i][5][j]
            value = playerInfos[i][4][j]
            number = playerInfos[i][3][j]

            i1.text((img6.width/2, 902), name, font=nameFont, fill=(0, 0, 0), anchor="mm")

            i1.text((img6.width/4, 1028), age, font=infoFont, fill=(0, 0, 0), anchor="mm")
            i1.text((img6.width*(3/4), 1028), weight, font=infoFont, fill=(0, 0, 0), anchor="mm")
            i1.text((img6.width/4 + 40, 1120), height, font=infoFont, fill=(0, 0, 0), anchor="mm")
            i1.text((img6.width*(3/4) + 50, 1120), value, font=infoFont, fill=(0, 0, 0), anchor="mm")
            i1.text((img6.width*(3/4) + 92, 125), number, font=numberFont, fill=(0, 0, 0), anchor="mm")

            relative_path = "output-photos\\final-results\\" + playerInfos[i][0] + "\\"

            full_path = os.path.join(absolute_path, relative_path)

            if not os.path.isdir(full_path):
                pathlib.Path(full_path).mkdir(parents=True, exist_ok=True)

            img6.save(full_path + playerInfos[i][1][j].replace(" ", "-").lower() + ".png")

def main():
    get_team_names_and_ids()

    teamColors = [[0 for i in range(2)] for j in range(len(teamNames))]
    playerInfos = [[str(), list(), list(), list(), list(), list(), list()] for j in range(len(teamNames))]

    get_team_colors(teamColors)
    get_player_datas(playerInfos)
    create_team_card_templates(teamColors)
    generate_team_cards(playerInfos)

if __name__ == "__main__":
    main()