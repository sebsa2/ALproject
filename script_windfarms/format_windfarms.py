import pandas as pd
import numpy as np
import re
from decimal import Decimal
import os


def formatlist(degrees):
    degrees = re.split('°|\' ',degrees)
    degrees[-1] = degrees[-1].replace('"',"")
    degrees = [float(x) for x in degrees]
    return degrees

def decimalDegree(degrees):
    degree, minute, second = degrees[0], degrees[1], degrees[2]
    return degree + (minute + second/60.)/60.


path = 'C:/Users/sebsa/Documents/Centrale Paris/3A/OEN/Projet Synthese/data/installed_capacity/Wind/Extraction The Wind Power'
wind_farms = os.listdir(path)


for wind_farm in wind_farms:
    test = pd.read_csv(path+'/'+wind_farm, sep = ';', encoding = "ISO-8859-1")

    test['Latitude'] = test['Latitude'].str.replace('å¡','°')
    test['Longitude'] = test['Longitude'].str.replace('å¡','°')
    test['Latitude'] = test['Latitude'].str.replace('Â°','°')
    test['Longitude'] = test['Longitude'].str.replace('Â°','°')

    test['Latitude'] = test['Latitude'].astype(str)
    test['Longitude'] = test['Longitude'].astype(str)
    test['Longitude'] = test['Longitude'].apply(lambda row: formatlist(row))
    test['Latitude'] = test['Latitude'].apply(lambda row: formatlist(row))
    test['longlat'] = test['Latitude'].apply (lambda row: len(row))
    test['longlong'] = test['Longitude'].apply (lambda row: len(row))
    test = test.loc[test['longlat'] == 3]

    test['Longitude'] = test['Longitude'].apply(lambda row: decimalDegree(row))
    test['Latitude'] = test['Latitude'].apply(lambda row: decimalDegree(row))

    test['Total nominal power'] = test['Total nominal power'].astype(str).str.extract('(\d+)').astype(float)
    test.loc[test['Total nominal power'] >= 10]
    
    test.drop(['longlat','longlong'], axis=1, inplace=True)
    test.to_csv(path+'/'+wind_farm[:-4]+'_formatted'+'.csv')

