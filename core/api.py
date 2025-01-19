import requests
from datetime import datetime
import json

base = "https://rt.data.gov.hk/v2"

def get_eta(stop_id, route, option="time"):
    url = base + f"/transport/citybus/eta/CTB/{stop_id}/{route}"
    response = requests.get(url)
    data = response.json()
    if data["data"]:
        next_eta = data["data"][0]["eta"]
        if option == "countdown":
            eta_time = datetime.fromisoformat(next_eta[:-6])
            now = datetime.now()
            countdown = (eta_time - now).total_seconds() // 60
            return "Now" if countdown <= 0 else f"{int(countdown)}"
        elif option == "time":
            eta_time = datetime.fromisoformat(next_eta[:-6])
            return eta_time.strftime("%H:%M")
    return "N/A"


#print(get_eta("002546","6","countdown"))
"""
countdowns = get_all_eta_countdowns("/Users/2115099/Desktop/CityMonitor/saved.json")
print(countdowns)
for bus, countdown in countdowns.items():
    print(f"{bus}: {countdown} minutes")
"""