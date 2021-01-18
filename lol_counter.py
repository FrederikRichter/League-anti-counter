#!/usr/bin/env python
import requests
import json
from rich.console import Console
from rich.prompt import Prompt
from rich import print
from bs4 import BeautifulSoup
import sys
def counters():
    userChamp = getUserChamp()
    userRole = getUserRole()
    html = getHTML(userChamp,userRole)
    worstPicks = getCounters(html)
    return getPick(worstPicks, userRole)
def getUserChamp():
    return(Prompt.ask("Champion"))
def getUserRole():
    choices=["top", "mid", "adc", "jungle", "support"]
    return(Prompt.ask("Role", choices=choices))
def getHTML(Champ, Role):
    return requests.get(f"https://u.gg/lol/champions/{Champ}/counter?role={Role}").text
def getCounters(html):
    soup = BeautifulSoup(html, 'html.parser').find_all("a", class_="counter-list-card best-win-rate")
    counters = {}
    for i in soup:
        counters[i.contents[1].contents[0].string]=float(i.contents[2].contents[0].string.replace("% WR", ""))
    return counters
def getPick(Picks, Role):
    candidates = {}
    with console.status("[bold green]Calculating anti counter", spinner="material") as status:
        for x in Picks:
            counters = getCounters(getHTML(x,Role))
            for j in counters:
                if j in candidates:
                    candidates[j]+=counters[j]
                else:
                    candidates[j]=counters[j]
    return {k: v for k, v in sorted(candidates.items(), key=lambda item: item[1], reverse=True)}
def beautify(picks):
    mid = 0
    for x in picks:
        mid += picks[x]
    if len(picks) != 0:
        mid=mid/len(picks)
    else:
        print("Champion not found in u.gg database")
        sys.exit(0)
    for j in picks:
        absolute = picks[j]
        picks[j]=absolute/mid
    return picks
console = Console()
picks = counters()
beautified = beautify(picks)
for x in beautified:
    console.print(x+((14-len(x))*" "), style=f"black on rgb({min(int(70/beautified[x]), 255)},{min(int(50*beautified[x]),255)},0)")
