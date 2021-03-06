#
python file extracting data from xc.tfrrs
# Author: David Walter
# Date: 12-03-2016

# from lxml import html
# import requests


import urllib2
from bs4 import BeautifulSoup

import numpy as np


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
        self.d3_regionals_dates = ['11/12/16']
        self.late_season_start_date = '09/24/16'
        self.visited_results = []
        self.pager_links = self.get_main_results_pager_links()

    def fix_url(self, url):
        ''' Returns a url string without a substring  '/' in the first position.
        '''
        if url[0] == '/':
            url = 'https:' + url
        return url

    def get_html(self, url):
        ''' Returns the html text from the url.
        '''
        hdr = {'User-Agent':'Mozilla/5.0'} 
        req = urllib2.Request(url, headers=hdr)
        results_page = urllib2.urlopen(req)
        results_html = results_page.read()
        return results_html

    def crawl_main_results(self, url = '', page_number=-1):
        '''
        Returns: an n by 3 python list, where every list within the list has
            [meet_date, meet_name, meet_url] for the Div. 3 regional meets. 

        '''
        if url == '':
            url = self.results_url # the default url
        if url[0] == '/':
            url = 'https:' + url
        results_html = self.get_html(url)

        soup = BeautifulSoup(results_html)
        tables = soup.findAll('table')
        table = tables[2] #this is NOT very robust 
        all_rows = table.findAll('tr')
        table_data = []

        for row in all_rows:
            columns = row.findAll('td', {'class': 'tableText'})
            if len(columns) == 0:
                continue
            date = columns[0].get_text()[:8]
            if not date in self.d3_regionals_dates:
                continue
            meet_name = columns[1].get_text()
            meet_url = 'https:'+ columns[1].findAll(href=True)[0]['href']
            table_data.append([date, meet_name, meet_url])

        if len(table_data) == 0: # try the next page link
            new_page_num = page_number + 1
            new_url = self.pager_links[new_page_num]
            table_data = self.crawl_main_results(new_url, new_page_num)

        for data_row in table_data:
            assert len(data_row) == 3

        return table_data


    def get_main_results_pager_links(self, url=''):
        ''' Returns the list of url links needed for all regional results. 
        '''
        if url == '':
            url = self.results_url
        results_html = self.get_html(url)
        soup = BeautifulSoup(results_html)
        pagers = soup.findAll('div', {'class':'pager'})
        pager = pagers[0].findAll('a')
        links = []
        for link in pager:
            url = link['href']
            links.append(url)
        return links


    def crawl_regional_results(self, main_table_data):
        ''' Crawls over each Regional results page.
            Returns a tuple. The first element in the tuple is the Men's
                Regional results data from the table on TFRRS. This Table is a
                list of lists, in each row containing:
                    - team name: a string
                    - team url: a string
                The second element is the Women's Reginal Results data.
                Formatted identically to the Men's Regional Results. 
        '''
        regional_results_men = []
        regional_results_women = []
        for region in main_table_data:
            # get the team places
            date, meet_name, meet_url = region
            if 'III' not in meet_name:
                continue
            region_html = self.get_html(meet_url)
            soup = BeautifulSoup(region_html)
            tables = soup.findAll('table')
            team_html_tables = [tables[2], tables[4]]
            team_data_tables = []
            avg_times_both_genders = []
            for table in team_html_tables:
                team_data_table = []
                avg_times = [] # used to distinguish mens and womens genders. 
                all_rows = table.findAll('tr')
                for row in all_rows:
                    columns = row.findAll('td', {'class': 'tableText'})
                    if len(columns) == 0:
                        continue

                    team_name = columns[1].get_text()
                    try:
                        team_url = 'https:'+ columns[1].findAll(href=True)[0]['href']
                    except IndexError: # this happens if the result is not a regional results page
                        print 'url = ',meet_url
                        print 'team name = ', team_name
                    avg_time = columns[1].get_text()

                    team_data_table.append([team_name, team_url])
                    avg_times.append(avg_time)
                team_data_tables.append(team_data_table)
                avg_times_both_genders.append(avg_times)
            if avg_times[0][0] > avg_times[1][0]:
                men_table_data = team_data_tables[0]
                women_table_data = team_data_tables[1]
            else:
                women_table_data = team_data_tables[0]
                men_table_data = team_data_tables[1]
            # print len(men_table_data)
            # print len(women_table_data)

            regional_results_men.append(men_table_data)
            regional_results_women.append(women_table_data)
        # print regional_results_men
        # print regional_results_women
        return (regional_results_men, regional_results_women)


    def crawl_team_results(self, regional_results_men, regional_results_women, late_season_start_date):
        ''' Goes over the results from each team's TFRRS website.
                regional_results_men and regional_results_women are returned in the
                tuple from crawl_regional_results. 
        '''
        for gender in [regional_results_men, regional_results_women]:
            visited_urls = []
            for region in gender:
                for team in region:
                    team_name, team_url = team[0], team[1]
                    if team_url in visited_urls:
                        continue
                    visited_urls.append(team_url)
                    team_html = self.get_html(team_url)
                    soup = BeautifulSoup(team_html)
                    tables = soup.findAll('table')
                    results_table = tables[5] # this is a hack and not very robust
                    all_rows = results_table.findAll('tr')
                    for row in all_rows:
                        columns = row.findAll('td', {'class': 'tableText'})
                        if len(columns) == 0:
                            continue

                        meet_date = columns[0].get_text()
                        month = int(meet_date[0:2])
                        day = (meet_date[3:5])
                        year = (meet_date[6:8])
                        if not self.is_valid_late_season_date(month, day, year):
                            continue 
                        try:
                            team_url = 'https:'+ columns[1].findAll(href=True)[0]['href']
                        except IndexError: # this happens if the result is not a regional results page
                            print 'url = ',meet_url
                            print 'team name = ', team_name
                        avg_time = columns[1].get_text()

                    
                    return
                    # team_html_tables = [tables[2], tables[4]]



    def is_valid_late_season_date(month, day, year):
        """
        month: integer from 1 to 12
        day: integer from 1 to 31
        year: integer from 0 t0 99 (for example, 16 represents 2016)
        """
        start_month = int(self.late_season_start_date[0:2])
        start_day = int(self.late_season_start_date[3:5])
        start_year = int(self.late_season_start_date[6:8])
        end_month = int(self.d3_regionals_dates[0][0:2])
        end_day = int(self.d3_regionals_dates[0][3:5])
        end_year = int(self.d3_regionals_dates[0][6:8])
        if not year == start_year:
            return False
        if not (start_month <= month <= end_month):
            return False
        if month == start_month:
            if not start_day <= day:
                return False
        if month == end_month:
            if not end_day > day:
                return False
        return True






class Team: 
    """
    TODO: docs here
    """
    def __init__(self, team_name, region):
        self.team_name = team_name
        self.region = region




def main():
    crawler = ResultsExtract()
    main_table_data = crawler.crawl_main_results()
    regional_results_men, regional_results_women = crawler.crawl_regional_results(main_table_data)
    crawler.crawl_team_results(regional_results_men, regional_results_women)
    


main()
