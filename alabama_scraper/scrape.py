from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse

aldh_covid_url = 'http://www.alabamapublichealth.gov/infectiousdiseases/2019-coronavirus.html'

class AlabamaCovidTableParser:


  def __init__(self):
    table = self.fetch_table_data()
    self.parse_table(table)
    

  def fetch_table_data(self):
    response = urllib.request.urlopen(aldh_covid_url)
    aldh_covid_page = response.read()
    soup = BeautifulSoup(aldh_covid_page, 'html.parser')
    return soup.find_all('table')[0]

  def parse_table(self, table):
    pass


app = AlabamaCovidTableParser()

