#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" AutoDD: Automatically does the so called Due Diligence for you. """

#AutoDD - Automatically does the "due diligence" for you.
#Copyright (C) 2020  Fufu Fang

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

__author__ = "Fufu Fang"
__copyright__ = "The GNU General Public License v3.0"

from bs4 import BeautifulSoup
import requests
from psaw import PushshiftAPI
from datetime import datetime, timedelta
import re

days_to_scrape = 2

def get_submission(n):
    """Returns a generator for the submission in past n days"""
    api = PushshiftAPI()
    s_date = datetime.today() - timedelta(days=n)
    s_timestamp = int(s_date.timestamp())
    gen = api.search_submissions(after=s_timestamp,
                                 subreddit='pennystocks',
                                 filter=['title', 'selftext'])
    return gen


def get_freq_list(gen):
    """
    Return the frequency list for the past n days

    :param int gen: The generator for subreddit submission
    :returns:
        - all_tbl - frequency table for all stock mentions
        - title_tbl - frequency table for stock mentions in titles
        - selftext_tbl - frequency table for all stock metninos in selftext
    """

    # Python regex pattern for stocks codes
    pattern = "[A-Z]{3,4}"
    # Dictionary containing the summaries
    title_dict = {}
    selftext_dict = {}
    all_dict = {}

    for i in gen:
        if hasattr(i, 'title'):
            title = ' ' + i.title + ' '
            title_extracted = re.findall(pattern, title)
            for j in title_extracted:
                if j in title_dict:
                    title_dict[j] += 1
                else:
                    title_dict[j] = 1

                if j in all_dict:
                    all_dict[j] += 1
                else:
                    all_dict[j] = 1

        if hasattr(i, 'selftext'):
            selftext = ' ' + i.selftext + ' '
            selftext_extracted = re.findall(pattern, selftext)
            for j in selftext_extracted:
                if j in selftext_dict:
                    selftext_dict[j] += 1
                else:
                    selftext_dict[j] = 1

                if j in all_dict:
                    all_dict[j] += 1
                else:
                    all_dict[j] = 1

    title_tbl = sorted(title_dict.items(), key=lambda x: x[1], reverse=True)
    selftext_tbl = sorted(selftext_dict.items(), key=lambda x: x[1],
                          reverse=True)
    all_tbl = sorted(all_dict.items(), key=lambda x: x[1], reverse=True)

    return all_tbl, title_tbl, selftext_tbl


def filter_tbl(tbl, min):
    """
    Filter a frequency table

    :param list tbl: the table to be filtered
    :param int min: the number of days in the past
    :returns: the filtered table
    """
    BANNED_WORDS = [
        'THE', 'FUCK', 'ING', 'CEO', 'USD', 'WSB', 'FDA', 'NEWS', 'FOR', 'YOU',
        'BUY', 'HIGH', 'ADS', 'FOMO', 'THIS', 'OTC', 'ELI', 'IMO',
        'CBS', 'SEC', 'NOW', 'OVER', 'ROPE', 'MOON', 'III', 'COVI', 'NASD', 'API', 'KLSV', 'STO', 
    ]
    tbl = [row for row in tbl if row[1] > min]
    tbl = [row for row in tbl if row[0] not in BANNED_WORDS]
    return tbl

def getColorHtml(change):
    if change[0] == '-':
        return 'red'
    return 'green'

def getColor(change):
    if change == "N/A\t\t\t":
        return '\033[94m'
    if change.split('\t',1)[1][0] == '-':
        return '\033[91m'
    return '\033[92m'

def getPrice(ticker):
    source = requests.get('https://finance.yahoo.com/quote/' + ticker).text
    soup = BeautifulSoup(source, 'lxml')
    price = soup.find('span', attrs={"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})
    if price is None or not price.text:
        fo.write("<td>N/A</td><td></td><td><a target=\"_blank\" href=\"https://www.reddit.com/r/pennystocks/search?q=" + ticker + "&restrict_sr=1&sort=new\">Reddit</a></td>")
        return("N/A\t\t\t")
    else:
        change = price.find_next_sibling()
        fo.write("<td><a target=\"_blank\" href=\"https://finance.yahoo.com/quote/" + ticker + "\">" +price.text+"</a></td>""<td style=\"color:"+getColorHtml(change.text)+"\">"+change.text+"</td><td><a target=\"_blank\" href=\"https://www.reddit.com/r/pennystocks/search?q=" + ticker + "&restrict_sr=1&sort=new\">Reddit</a></td>")
        return(price.text+"\t"+change.text)

def print_tbl(tbl, fo):
    # print("Most Frequent Tickers\n-----------------------------------\nCode\tFreq\tPrice\tChange")
    fo.write("<html><head><link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css\"><title>Auto DD</title></head><body>")
    fo.write("<table class=\"table\"><thead class=\"thead-dark\"><th scope=\"col\">Code</th><th scope=\"col\">Frequency</th><th scope=\"col\">Price</th><th scope=\"col\">Change</th><th scope=\"col\">Link</th></thead>")
    x = 0
    total=len(tbl)
    for row in tbl:
        current = "Progress: "
        for y in range(x):
            current=current+"*"
        for y in range(total-x):
            current=current+"-"
        print(current, end="\r", flush=True)
        x=x+1
        fo.write("<tr>")
        fo.write("<th scope=\"row\">"+str(row[0])+"</th>""<td>"+str(row[1])+"</td>")
        price = getPrice(str(row[0]))
        # print(getColor(price) + str(row[0]) + "\t" + str(row[1]) + "\t" + price)
        fo.write("</tr>")
    fo.write("</table></body></html>")


if __name__ == '__main__':
    print("Currently set to scrape " + str(days_to_scrape) + " days.")
    print("Scraping penny stocks...")
    gen = get_submission(days_to_scrape)  # Get 1 day worth of submission
    all_tbl, _, _ = get_freq_list(gen)
    all_tbl = filter_tbl(all_tbl, 2)
    fo = open("out.html", "w")
    print_tbl(all_tbl, fo)
    fo.close()
    print("Finished scraping. Output saved to out.html.")
