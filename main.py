#!/usr/bin/env python3
import requests
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
from os import system, name

#Color class for displaying results on CLI
class colors:
    green  = '\033[92m'
    yellow = '\033[93m'
    red    = '\033[91m'
    end    = '\033[0m'

def color(string, color):
    return color + string + colors.end

def log_info(string):
        print(color('INFO -> ', colors.green) + string)

def clearTerminal():
    clear = system('clear')

def getGlobal(soup):
    counts = [n.text for n in soup.find_all('div', class_= 'maincounter-number')]
    return counts

def printGlobal(soup):
    counts = getGlobal(soup)
    data = {}
    data['totalCases'] = counts[0]
    data['totalDeaths'] = counts[1]
    data['totalRecovered'] = counts[2]

    print("__________________")
    print("GLOBAL STATISTICS")
    print("__________________")
    print()

    print("Total Cases: %14s" %data['totalCases'])
    print("Total Deaths: %19s" %color(data['totalDeaths'], colors.red))
    print("Total Recovered: %15s" %color(data['totalRecovered'], colors.green))
    print()
def getUs(soup):
    countries = []
    table = soup.find('table')
    tableBody = table.find('tbody')

    rows = tableBody.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        countries.append([ele for ele in cols if ele])

    for country in countries:
        if country[0] == "USA":
            unitedStates = country

    return unitedStates

def printUs(soup):
    unitedStates = getUs(soup)

    '''
    INDEX REFERENCE:
        0 = country name
        1 = total cases
        2 = new cases
        3 = total deaths
        4 = new deaths
        5 = total recovered
        6 = active cases
        7 = serious critical
        8 = I GOT NO CLUE LMFAO
        '''

    print("__________________")
    print('UNITED STATES')
    print("__________________")
    print()
    print("Total Cases: %10s" %unitedStates[1])
    print("Total Recovered: %12s" %color(unitedStates[5], colors.green))
    print("Total Deaths: %15s" %color(unitedStates[3], colors.red))
    print("New Cases: %21s" %color(unitedStates[2], colors.red))




def main():
    while True:

        html = requests.get('https://www.worldometers.info/coronavirus/#countries').text
        soup = BeautifulSoup(html, 'lxml')
        d = datetime.now().strftime("%m/%d/%Y -- %I:%M %p")


        log_info("Updated at: %s" %d)
        printGlobal(soup)
        printUs(soup)

        sleep(300)
        clearTerminal()

#main()
html = requests.get('https://www.worldometers.info/coronavirus/#countries').text
soup = BeautifulSoup(html, 'lxml')

printGlobal(soup)
