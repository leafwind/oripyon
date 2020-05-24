# Province/State,Country/Region,Lat,Long,1/22/20,1/23/20,1/24/20,1/25/20,1/26/20,1/27/20,1/28/20,1/29/20,1/30/20,1/31/20,2/1/20,2/2/20,2/3/20,2/4/20,2/5/20,2/6/20,2/7/20,2/8/20,2/9/20,2/10/20,2/11/20,2/12/20,2/13/20,2/14/20,2/15/20,2/16/20,2/17/20,2/18/20,2/19/20,2/20/20,2/21/20,2/22/20,2/23/20,2/24/20,2/25/20,2/26/20,2/27/20,2/28/20,2/29/20,3/1/20,3/2/20,3/3/20,3/4/20,3/5/20,3/6/20,3/7/20,3/8/20,3/9/20,3/10/20
# ,Japan,36,138,2,1,2,2,4,4,7,7,11,15,20,20,20,22,22,45,25,25,26,26,26,28,28,29,43,59,66,74,84,94,105,122,147,159,170,189,214,228,241,256,274,293,331,360,420,461,502,511,581

import csv
from datetime import datetime


def load_ncov_data(filepath='cache_ext_data/time_series_19-covid-Confirmed.csv'):
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        country_state_result = {}
        country_result = {}
        for row in reader:
            province_state = row[0]
            country_region = row[1]
            if country_region not in country_result:
                country_result[country_region] = []
            data_per_state = []
            for i, v in enumerate(row[4:]):
                date = datetime.strptime(headers[i+4], '%m/%d/%y')
                data_per_state.append((date, int(v)))
                if len(country_result[country_region]) >= i + 1:
                    country_result[country_region][i][1] += int(v)
                else:
                    country_result[country_region].append([date, int(v)])
            country_state_result[(country_region, province_state)] = data_per_state
        return country_state_result, country_result


if __name__ == '__main__':
    country_state_result, country_result = load_ncov_data()
    for country in country_result:
        print(country)
    print(country_result['Mainland China'])
