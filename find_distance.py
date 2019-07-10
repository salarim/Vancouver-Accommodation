import math
import requests
import json
import pickle

def creat_data(tlat, dlat, rlng, llng, hres, wres, chunk_size):
    dsts = [{
        "latitude": 49.278801,
        "longitude": -122.920430
    }, 
    {
        "latitude": 49.263059,
        "longitude": -123.251100
    }]
    
    data_chunks = []
    origins = []
    
    for i in range(hres):
        for j in range(wres):
            lat = dlat + i * ((tlat-dlat)/hres)
            lng = llng + j * ((rlng-llng)/wres)
            origins.append((lat, lng))
    
    for i in range(math.ceil(len(origins)/chunk_size)):
        data = {"origins": [], "destinations": dsts, "travelMode": "transit"}
        for j in range(chunk_size):
            ind = i * chunk_size + j
            if ind >= len(origins):
                break
            data["origins"].append({"latitude": origins[ind][0], "longitude": origins[ind][1]})
        data_chunks.append(data)

    return data_chunks

def create_distance_map():
    KEY = 'PUT_YOUR_KEY_HERE!'
    url = 'https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key={0}'.format(KEY)
    tlat, dlat, rlng, llng = 49.294353, 49.182451, -122.817806, -123.263958

    data = creat_data(tlat, dlat, rlng, llng, 100, 100, 300)

    result = []

    for d in data:  
        r = requests.post(url, data=json.dumps(d, ensure_ascii=False))
        json_data = json.loads(r.text)
        result.append(json_data)

    points = []
    first_dis = {}
    second_dis = {}

    for r in result:
        ps = []
        for x in r['resourceSets'][0]['resources'][0]['origins']:
            ps.append((x['latitude'], x['longitude']))

        for x in r['resourceSets'][0]['resources'][0]['results']:
            originIndex = x['originIndex']
            dstIndex = x['destinationIndex']
            travelDuration = x['travelDuration']
            ind = len(points) + originIndex
            if dstIndex == 0:
                first_dis[ind] = travelDuration
            else:
                second_dis[ind] = travelDuration
        points.extend(ps)

    compact_dict = {}

    for i in range(len(points)):
        compact_dict[i] = {'lat': points[i][0],
                        'lng': points[i][1],
                        'sfu_dis': first_dis[i],
                        'ubc_dis': second_dis[i]}
    return compact_dict

def save_obj(obj, name ):
    with open('data/obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def run():
    compact_dict = create_distance_map()
    save_obj(compact_dict, 'distance')

if __name__=='__main__':
    run()
