from bs4 import BeautifulSoup
from datetime import datetime
from prometheus_client import Gauge, start_http_server
import urllib.request, urllib.error, urllib.parse
import threading

aldh_covid_url = 'http://www.alabamapublichealth.gov/infectiousdiseases/2019-coronavirus.html'

CASE_COUNT = Gauge(
    'case_count', 'Number of confirmed COVID-19 cases',
    ['county_name']
)

class AlabamaCovidTableParser:

  def __init__(self):
    self.county_names = ['AUTAUGA', 'BALDWIN', 'BARBOUR', 'BIBB', 'BLOUNT', 'BULLOCK', 'BUTLER', 'CALHOUN',
                 'CHAMBERS', 'CHEROKEE', 'CHILTON', 'CHOCTAW', 'CLARKE', 'CLAY', 'CLEBURNE',
                 'COFFEE', 'COLBERT', 'CONECUH', 'COOSA', 'COVINGTON', 'CRENSHAW', 'CULLMAN',
                 'DALE', 'DALLAS', 'DEKALB', 'ELMORE', 'ESCAMBIA', 'ETOWAH', 'FAYETTE', 'FRANKLIN',
                 'GENEVA', 'GREENE', 'HALE', 'HENRY', 'HOUSTON', 'JACKSON', 'JEFFERSON', 'LAMAR',
                 'LAUDERDALE', 'LAWRENCE', 'LEE', 'LIMESTONE', 'LOWNDES', 'MACON', 'MADISON',
                 'MARENGO', 'MARION', 'MARSHALL', 'MOBILE', 'MONROE', 'MONTGOMERY', 'MORGAN',
                 'PERRY', 'PICKENS', 'PIKE', 'RANDOLPH', 'RUSSELL', 'SHELBY', 'ST CLAIR', 'SUMTER',
                 'TALLADEGA', 'TALLAPOOSA', 'TUSCALOOSA', 'WALKER', 'WASHINGTON', 'WILCOX',
                 'WINSTON']


  def fetch_table_data(self):
    response = urllib.request.urlopen(aldh_covid_url)
    aldh_covid_page = response.read()
    soup = BeautifulSoup(aldh_covid_page, 'html.parser')
    return soup.find_all('table')[0]

  def parse_table(self, table) -> dict:
    def get_date(table_row) -> datetime:
      updated_string: str = table_row.find_all('h2')[1].text
      time_string: str = updated_string.strip('Updated: ').rstrip(' (CT)').replace('.', '')
      print(time_string)
      return datetime.strptime(time_string, '%B %d, %Y %I:%M %p')

    def parse_county_row(table_row) -> tuple:
      key = table_row.find_all('p')[0]
      value = table_row.find_all('p')[1]
      return key.text.upper(), value.text


    table_rows = table.find_all('tr')
    get_date(table_rows[0])
    return {county: count for county, count in map(parse_county_row, table_rows[2:-1])}

  def update_counters(self):
    table = self.fetch_table_data()
    county_dict: dict = {county: 0 for county in self.county_names}
    county_dict.update(self.parse_table(table))
    for county in county_dict:
        CASE_COUNT.labels(county).set(county_dict[county])


if __name__ == '__main__':
    app = AlabamaCovidTableParser()
    def poll():
        threading.Timer(5.0, poll).start()
        app.update_counters()
    poll()
    # Start up the server to expose the metrics.
    start_http_server(8000)



