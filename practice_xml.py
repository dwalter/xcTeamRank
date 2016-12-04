# examples with xpaths
# tutorial on http://docs.python-guide.org/en/latest/scenarios/scrape/#lxml-and-requests

from lxml import html
import requests

page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
tree = html.fromstring(page.content)

#This will create a list of buyers:
buyers = tree.xpath('/html/body/div/div/text()')
#This will create a list of prices
prices = tree.xpath('//span[@class="item-price"]/text()')

test2 = tree.xpath('//table/tbody/tr/td[@class="tableText"]/div/text()')

print 'Buyers: ', buyers
print 'Prices: ', prices
print 'test2: ', test2

##################################

page = requests.get('https://xc.tfrrs.org/results_search.html')
tree = html.fromstring(page.content)


#This will create a list of buyers:
meets_path = '/div[@id="blackbox"]/div[@class="blackfullbox-bod"]/div[@id="results_search"]/div/div[@class="tablelist"]/div/table/tbody/tr/td[@class="tableText"]/div/text()'
meets = tree.xpath(meets_path)


print 'meets:  ', meets



# page = requests.get('https://google.com')
# tree = html.fromstring(page.content)

# #This will create a list of buyers:
# test = tree.xpath('//span[@id="fsl"]/a[@class="_Gs"]/text()')

# print 'test: ', test

