from bs4 import BeautifulSoup
import requests
import pandas as pd
# nlp = spacy.load('en_core_web_sm')
from spacy.matcher import Matcher
# m_tool = Matcher(nlp.vocab)
from urllib.request import urlopen as uReq


# desktop user-agent


def simpleGoogleSearch(query, start):
    results = []

    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}&start={start}"
    URL = "https://patents.google.com/patent/EP2536453B1/en"
    # https://www.google.com/search?q=covid&start=0

    # desktop user-agent
    # ###################################
    #IMPORTANT                              go to chrome, search my user agent, copy the User agent into the User_agent down below.
    # ###################################
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"

    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")

        for g in soup.find_all('div', class_='yuRUbf'):
            anchors = g.find_all('a')

            if anchors:
                link = anchors[0]['href']
                title = g.find('h3').text
                item = {"title": title, "link": link}
                results.append(item)

    return results


def googleToPandas(googleQuery):
    resultsCounter = 0
    resultsList = []

    while True:
        pageResults = simpleGoogleSearch(googleQuery, resultsCounter)

        if not pageResults:
            break
        else:
            resultsList.extend(pageResults)
            resultsCounter = resultsCounter + 10

    return pd.DataFrame(resultsList)

googleSearchQuery   = "hello"
results = googleToPandas(googleSearchQuery)

results.to_csv('GoogleResults.csv', index=False)
results.to_excel('GoogleResults.xlsx', index=False)
results.to_json('GoogleResults.jsonl', orient='records', lines=True)