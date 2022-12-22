# My Childhood Soccer Card Project

## Description

In this project, I tried to create soccer cards which I played in my past.<br />

You can see a picture about these cards at below.

![Alt text](/old-cards.png)

I played these cards with my friends almost 20 years ago. <br />

So, I decided to generate these cards with using transfermarkt datas.

I prepared some base photos as useful source for me. You can see them at below.

![Alt text](/base-photos.png)

I created them using Gimp and MS Power Point.

I used a technique to get data from transfermarkt which is known as web scraping.
Also, I manipulated the pictures and datas which is downloaded.

You can see the final result as below.

![Alt text](/new-cards.png)

## Tools

* PyCharm Community Edition 2022.2.3 (To write codes and generate cards)
* Gimp & Power Point (To create base photos)
* Font files (To make almost same font in cards)

## Installation

* Be sure that Python 3 version is installed in your PC.
* Clone the project using this command: ``` https://github.com/erengaygusuz/soccer-card-project.git ```
* Install required packages with using this command in terminal: ``` pip install -r requirements.txt ```
* Run the project.
* Generated files will be under the ProjectRootDirectory/output-photos/final-results folder.

## How to Use

* If you run the code directly without changing anything, you will get player cards of Sportoto Super League Teams from Turkey.
* To generate cards from other leagues, please change the value of variable named leagueLinkAddress with a transfermarkt league link address
* For Example to generate England Premier League use this link: ``` https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1 ```
* Also some values are calculated with some random values if it does not exist or can not get from transfermarkt.
* For example weight, height, market value, player number etc.

## License

The MIT License (MIT)
