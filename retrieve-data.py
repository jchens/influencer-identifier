import numpy as np
import pandas as pd
import json
import copy
import datetime
import firebase_admin
import math
from firebase_admin import credentials, db
<<<<<<< HEAD
=======
import geocoder
import re
>>>>>>> e385833df2532a1cadc87aafe38692ebfdda0f81


def main():
    cred = credentials.Certificate("firebase-cred.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://hive-258ce.firebaseio.com/'
    })

    retrieveData()

def retrieveData():
    ref = db.reference('/Tweets-Folder/' + str(datetime.date.today())+ '/')
    result = ref.get()
    data = pd.DataFrame(columns=['Date', 'Tweet','Tweet latitude', 'Tweet longitude', 'User','User location', 'Retweets', 'Replies', 'Liked', 'Handle', 'Followers', 'Total Tweets by user'])
    for i,key in enumerate(result.keys()):
        data.loc[i] = (result[key]['Date'] if 'Date' in result[key] else np.NaN,
        result[key]['Tweet'] if 'Tweet' in result[key] else np.NaN,
        result[key]['Tweet latitude'] if 'Tweet latitude' in result[key] else np.NaN,
        result[key]['Tweet longitude'] if 'Tweet longitude' in result[key] else np.NaN,
        result[key]['User'] if 'User' in result[key] else np.NaN,
        result[key]['User location'] if 'User location' in result[key] else np.NaN,
        result[key]['Retweets'] if 'Retweets' in result[key] else np.NaN,
        result[key]['Replies'] if 'Replies' in result[key] else np.NaN,
        result[key]['Liked'] if 'Liked' in result[key] else np.NaN,
        result[key]['Handle'] if 'Handle' in result[key] else np.NaN,
        result[key]['Followers'] if 'Followers' in result[key] else np.NaN,
        result[key]['Total Tweets by user'] if 'Total Tweets by user' in result[key] else np.NaN)
    data.fillna(0)
<<<<<<< HEAD
    log_tweet_count = np.log(data['Total Tweets by user'].astype('float'))
    data['Influencer-Score'] = (data['Followers'] * (data['Retweets']+1) * log_tweet_count * (data['Liked']+1)) / 10**9
=======
    data['Influencer-Score'] = (data['Followers'] * (data['Retweets']+1) * (np.log(data['Total Tweets by user'].astype('float'))/np.log(1.5)) * (data['Liked']+1)) / 10**9
>>>>>>> e385833df2532a1cadc87aafe38692ebfdda0f81
    influencers = data.loc[data['Influencer-Score'] >= 1]

    influencer_ref = db.reference('Influencers/')
    city_ref = db.reference('City/')
    for index,row in influencers.iterrows():
        existingChild = influencer_ref.child(row['Handle']).get()
        existingChild_ref = influencer_ref.child(row['Handle'])
        if(existingChild):
            if(existingChild['Influencer-Score'] < row['Influencer-Score']):
                existingChild_ref.update({
                    'User': row['User'],
                    'User location': row['User location'],
                    'Handle': row['Handle'],
                    'Latitude': row['Tweet latitude'],
                    'Longitude': row['Tweet longitude'],
                    'Followers': row['Followers'],
                    'Total Tweets by user': row['Total Tweets by user'],
                    'Tweet': row['Tweet'],
                    'Influencer-Score': row['Influencer-Score'],
                })
        else:
            newInfluencer = influencer_ref.child(row['Handle'])
            newInfluencer.update({
                'User': row['User'],
                'User location': row['User location'],
                'Handle': row['Handle'],
                'Latitude': row['Tweet latitude'],
                'Longitude': row['Tweet longitude'],
                'Followers': row['Followers'],
                'Total Tweets by user': row['Total Tweets by user'],
                'Tweet': row['Tweet'],
                'Influencer-Score': row['Influencer-Score'],
            })
        try:
            g = geocoder.yandex(row['Tweet latitude'], [row['Tweet longitude']], method='reverse').json
        except:
            g = None

        if(g):
            cityName = g['raw']['metaDataProperty']['GeocoderMetaData']['text']
            cityName = re.sub('[.]', '', cityName)
            cityName = cityName.split(',')
            cityName.reverse()
            cityName = ",".join(cityName)
        else:
            cityName = 'unknown'

        existingCity = city_ref.child(cityName).get()
        existingCity_ref = city_ref.child(cityName)
        if(existingCity and not existingChild):
            newInfluencer = existingCity_ref.child(row['Handle'])
            newInfluencer.update({
                'User': row['User'],
                'User location': row['User location'],
                'Handle': row['Handle'],
                'Latitude': row['Tweet latitude'],
                'Longitude': row['Tweet longitude'],
                'Followers': row['Followers'],
                'Total Tweets by user': row['Total Tweets by user'],
                'Tweet': row['Tweet'],
                'Influencer-Score': row['Influencer-Score'],
            })
        elif(not existingCity):
            newCity = city_ref.child(cityName)
            newInfluencer = newCity.child(row['Handle'])
            newInfluencer.update({
                'User': row['User'],
                'User location': row['User location'],
                'Handle': row['Handle'],
                'Latitude': row['Tweet latitude'],
                'Longitude': row['Tweet longitude'],
                'Followers': row['Followers'],
                'Total Tweets by user': row['Total Tweets by user'],
                'Tweet': row['Tweet'],
                'Influencer-Score': row['Influencer-Score'],
            })




if __name__ == '__main__':
    main()
