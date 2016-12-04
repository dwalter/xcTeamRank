#python file extracting data from xc.tfrrs
# Author: David Walter
# Date: 12-03-2016

from lxml import html
import requests

from bs4 import BeautifulSoup


'''

- Need to go through all of the late season results
- Need to know which teams are in which region
- Need to 

'''

class ResultsExtract:
    """ Class that handles most of the web crawling of results on xc.tfrrs.org
        attributes: 
        - results_url: https://xc.tfrrs.org/results_search.html
        - d3_regional_dates: list of the date(s) of Div.3 Regional meets,
            must be at least length 1, in format (month)/(day)/year in 
            format mm/dd/yyyy, ex: 01/31/1999
        - visited results: list of urls of results that the program has already
            visited, as to not recount results multiple times. 
    """
    def __init__(self):
        self.results_url = 'https://xc.tfrrs.org/results_search.html'
        self.d3_regionals_dates = ['11/12/2016']
        self.visited_results = []

    def crawl_results(self):
        results_page = requests.get(self.results_url)
        print results_page
        return
        results_tree = html.fromstring(results_page.content)
        # get all 8 regional results urls
        table_tree = results_tree.xpath('//*[@id="results_search"]/div[3]/div/div[2]/table')

        #//*[@id="results_search"]/div[3]/div/div[2]/table/tbody/tr[9]/td[4]/div/a

        print type(table_tree)
        print len(table_tree)







class Team: 
    """
    TODO: docs here
    """
    def __init__(self, team_name, region):
        self.team_name = team_name
        self.region = region




def main():
    crawler = ResultsExtract()
    crawler.crawl_results()


main()

