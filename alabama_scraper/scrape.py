from datetime import datetime
from prometheus_client import Gauge, start_http_server
import requests
import threading

poll_time = 3600
arcgis_url = 'https://services7.arcgis.com/4RQmZZ0yaZkGR1zy/arcgis/rest/services/COV19_Public_Dashboard_ReadOnly/FeatureServer/0/query'
query_params = {
    "f": "json",
    "where": "CONFIRMED>0",
    "returnGeometry": "false",
    "outFields": "CNTYNAME,CONFIRMED,DIED",
    "orderFields": "CNTYNAME"
}

CASE_COUNT = Gauge(
    'case_count', 'Number of confirmed COVID-19 cases',
    ['county_name']
)

DEATH_COUNT = Gauge(
    'death_count', 'Number of confirmed COVID-19 deaths',
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


  def fetch_data(self):
    return requests.get(arcgis_url, params=query_params)

  def parse_data(self, data, stat) -> dict:
    def parse_row(row: dict) -> (str, int):
        return row['attributes']['CNTYNAME'].upper(), row['attributes'][stat]

    county_data: dict = data['features']
    return {county: count for county, count in map(parse_row, county_data)}

  def update_counters(self):
    data = self.fetch_data().json()
    print(data)
    county_case_dict: dict = {county: 0 for county in self.county_names}
    county_case_dict.update(self.parse_data(data, "CONFIRMED"))
    county_death_dict: dict = {county: 0 for county in self.county_names}
    county_death_dict.update(self.parse_data(data, "DIED"))
    print(county_case_dict)
    for county in county_case_dict:
        CASE_COUNT.labels(county).set(county_case_dict[county])
    for county in county_death_dict:
        DEATH_COUNT.labels(county).set(county_death_dict[county])


if __name__ == '__main__':
    app = AlabamaCovidTableParser()
    def poll():
        threading.Timer(poll_time, poll).start()
        app.update_counters()
    poll()
    # Start up the server to expose the metrics.
    start_http_server(8000)



