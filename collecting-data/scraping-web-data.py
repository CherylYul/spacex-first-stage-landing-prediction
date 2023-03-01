import requests
import pandas as pd
import re
import unicodedata
from bs4 import BeautifulSoup

url_1 = "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches_(2010%E2%80%932019)"
url_2 = "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches"


r = requests.get(url_1)
html_soup = BeautifulSoup(r.text, "html.parser")
tables = html_soup.select("table.wikitable>tbody")

columns = []
for column in tables[0].find_all("th", scope="col"):
    if column.sup:
        column.sup.extract()
    if column.br:
        column.br.extract()
    column_name = column.get_text(strip=True).replace(",", "").replace(" ", "")
    print(column_name)
    columns.append(column_name)

launch_dict = dict.fromkeys(columns)
for name in launch_dict:
    launch_dict[name] = []
print(launch_dict)


def get_date(cell):
    datetime = cell.get_text(strip=True)
    datetime = re.search("[^,]+", datetime)
    return datetime.group()


def get_rid_of_sup(cell):
    if cell.sup:
        cell.sup.extract()
    return cell.get_text(strip=True)


def get_payload(cell):
    if cell.find("a", title=True):
        return cell.a.get("title")


def get_mass(cell):
    mass = unicodedata.normalize("NFKD", cell.text).strip()
    if mass:
        mass.find("kg")
        new_mass = mass[0 : mass.find("kg") + 2]
    else:
        new_mass = 0
    return new_mass


def get_landing(cell):
    if cell.sup:
        cell.sup.extract()
    if cell.small:
        cell.small.extract()
    return cell.get_text(strip=True)


for url in [url_1, url_2]:
    r = requests.get(url)
    html_soup = BeautifulSoup(r.text, "html.parser")
    rows = html_soup.select("table.wikitable tr[id]")
    for row in rows:
        if row.find("th", scope="row"):
            print("scrape:")
            launch_dict["FlightNo."].append(
                row.find("th", scope="row").get_text(strip=True)
            )

            cells = row.find_all("td")
            launch_dict["Dateandtime(UTC)"].append(get_date(cells[0]))
            launch_dict["VersionBooster"].append(get_rid_of_sup(cells[1]))
            launch_dict["Launchsite"].append(cells[2].get_text(strip=True))
            launch_dict["Payload"].append(get_payload(cells[3]))
            launch_dict["Payloadmass"].append(get_mass(cells[4]))
            launch_dict["Orbit"].append(cells[5].get_text(strip=True))
            launch_dict["Customer"].append(get_rid_of_sup(cells[6]))
            launch_dict["Launchoutcome"].append(get_rid_of_sup(cells[7]))
            launch_dict["Boosterlanding"].append(get_landing(cells[8]))

df = pd.DataFrame(launch_dict)
df.to_csv("collecting-data/wiki-data.csv")
