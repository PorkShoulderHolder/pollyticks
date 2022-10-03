import pandas as pd
import json
import requests
def get_data():
    data = requests.get("https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/national-map-page/national/president.json")
    json_data = json.loads(data.text)["data"]["races"]
    new_data = []
    for s in json_data:
        print(s["state_name"])
        counties = s["counties"]
        biden_total = 0
        trump_total = 0
        try:
            for c in counties:
                trump_ratio = float(c['results']['trumpd']) / float(c['votes'])
                biden_ratio =  float(c['results']['bidenj']) / float(c['votes'])
                trump = float(c['results']['trumpd']) + trump_ratio * (float(c[
                        'tot_exp_vote']) - int(c['votes']))
                biden = float(c['results']['bidenj']) + biden_ratio * (
                        float(c['tot_exp_vote']) - int(c['votes']))
                trump_total += trump
                biden_total += biden
                new_data.append({"trump_support": trump_ratio,
                                  "biden_support": biden_ratio,
                                  "fips": c['fips'],
                                  "state": s["state_name"],
                                  "turnout": float(c['votes'])
                                  })
            print("----------")
            print(f'{s["state_name"]}: biden: {biden_total}, trump: {trump_total} --- {"BIDEN WINS!" if biden_total > trump_total else "trump WINS!"}')
        except (TypeError, ZeroDivisionError) as e:
            pass

    print(len(new_data))
    json.dump(new_data, open('data/election_results.json', 'w+'))

get_data()
