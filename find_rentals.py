import pandas as pd
import pickle
import subprocess

def crawl():
    rc = subprocess.call("./crawl.sh")
    return rc == 0

def sort_rentals(distance):
    craigslist = pd.read_csv('craigslist.csv')
    kijiji = pd.read_csv('kijiji.csv')
    df = craigslist.append(kijiji, ignore_index=True)

    lng_num, lat_num = 100, 100
    min_lng, min_lat = distance[0]['lng'], distance[0]['lat']
    max_lng, max_lat = distance[len(distance)-1]['lng'], distance[len(distance)-1]['lat']
    eps_lng, eps_lat = (max_lng-min_lng)/(lng_num-1), (max_lat-min_lat)/(lat_num-1)

    def sum_distance(lat, lng):
        if lat < min_lat:
            lat = min_lat
        if lat > max_lat:
            lat = max_lat
        if lng < min_lng:
            lng = min_lng
        if lng > max_lng:
            lng = max_lng
        lng_ind = int((lng - min_lng)/eps_lng)
        lat_ind = int((lat - min_lat)/eps_lat)
        total_ind = lat_ind * lng_num + lng_ind
        return max(distance[total_ind]['sfu_dis'], distance[total_ind]['ubc_dis'])
    
    df2 = df[df['lat'].notnull()]
    df2 = df2[df2['long'].notnull()]
    df2['dis'] = df2.apply(lambda x: sum_distance(x['lat'], x['long']), axis=1)
    df2 = df2.sort_values('dis')
    df2 = df2[df2['dis'] > 0]
    df2 = df2[(df2['price'] > 900) & (df2['price'] < 1600)]

    df2.to_csv('result.csv')
    print("Results have been written in result.csv!")

def load_obj(name):
    with open('data/obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def run():
    if not crawl():
        print("Crawling was unsuccessful!")
        return
    sort_rentals(load_obj('distance'))

if __name__=='__main__':
    run()
