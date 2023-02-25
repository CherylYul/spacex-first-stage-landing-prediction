import requests
import json
import pandas as pd
import datetime

api = "https://api.spacexdata.com/v4/launches/past"


def get_rockets_data(x):
    url = "https://api.spacexdata.com/v4/rockets/" + str(x)
    r = requests.get(url).json()
    return r["name"], r["cost_per_launch"]


def get_launchpads_data(x):
    url = "https://api.spacexdata.com/v4/launchpads/" + str(x)
    r = requests.get(url).json()
    return r["full_name"], r["latitude"], r["longitude"]


def get_payloads_data(x):
    url = "https://api.spacexdata.com/v4/payloads/" + str(x)
    r = requests.get(url).json()
    return r["customers"], r["mass_kg"], r["orbit"], r["manufacturers"]


def get_cores_data(x):
    url = "https://api.spacexdata.com/v4/cores/" + str(x)
    r = requests.get(url).json()
    return r["block"], r["reuse_count"], r["serial"]


Date = []
FlightNumber = []
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
LandingType = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []
CostPerLaunch = []
Customers = []
Manufacturers = []

r = requests.get(api).json()
for flight in r:
    print("scraping...")
    name, cost_per_launch = get_rockets_data(flight["rocket"])
    print(name, cost_per_launch)
    launch_site, latitude, longitude = get_launchpads_data(flight["launchpad"])
    print(launch_site, latitude, longitude)
    customers, mass, orbit, manufacturers = get_payloads_data(flight["payloads"][0])
    print(customers, mass, orbit, manufacturers)
    block, reuse_count, serial = get_cores_data(flight["cores"][0]["core"])
    print(block, reuse_count, serial)

    Date.append(flight["date_utc"])
    FlightNumber.append(flight["flight_number"])
    BoosterVersion.append(name)
    PayloadMass.append(mass)
    Orbit.append(orbit)
    LaunchSite.append(launch_site)
    LandingType.append(flight["cores"][0]["landing_type"])
    Outcome.append(flight["cores"][0]["landing_success"])
    Flights.append(flight["cores"][0]["flight"])
    GridFins.append(flight["cores"][0]["gridfins"])
    Reused.append(flight["cores"][0]["reused"])
    Legs.append(flight["cores"][0]["legs"])
    LandingPad.append(flight["cores"][0]["landpad"])
    Block.append(block)
    ReusedCount.append(reuse_count)
    Serial.append(serial)
    Longitude.append(longitude)
    Latitude.append(latitude)
    CostPerLaunch.append(cost_per_launch)
    Customers.append(customers)
    Manufacturers.append(manufacturers)

df = pd.DataFrame(
    {
        "date": Date,
        "flight no": FlightNumber,
        "booster version": BoosterVersion,
        "payload mass": PayloadMass,
        "orbit": Orbit,
        "launch site": LaunchSite,
        "landing type": LandingType,
        "outcome": Outcome,
        "flights": Flights,
        "gridfins": GridFins,
        "reused": Reused,
        "legs": Legs,
        "landing pad": LandingPad,
        "block": Block,
        "reused count": ReusedCount,
        "serial": Serial,
        "longitude": Longitude,
        "latitude": Latitude,
        "cost per launch": CostPerLaunch,
        "customers": Customers,
        "manufacterers": Manufacturers,
    }
)

df.to_csv("api-data.csv")
