import logging

import cachetools.func
import requests
import time
from app.ext_apis.util import build_kd_tree


@cachetools.func.ttl_cache(ttl=3600*6)
def ey_clarify_api():
    """
    行政院即時新聞澄清
    https://data.gov.tw/dataset/92127
    [
        {
            "標題": "關於網路謠傳我國人入境泰國需隔離14日事，外交部澄清說明如下",
            "網址": "https://www.mofa.gov.tw//News_Content.aspx?n=D6D997396B647A7C&s=6849DB948E764F68",
            "發布日期": "2020/2/29 上午 10:40:46",
            "資料來源": "外交部"
        }, ...
    ]
    """
    start = int(time.time())
    pid = 'eac3996e-f699-4a5a-a17a-6beab4eabee1'
    url = f'https://www.ey.gov.tw/OpenDataForm.aspx?PID={pid}'
    r = requests.get(url)
    end = int(time.time())
    logging.getLogger(__name__).info(f'{__name__} took {end - start} seconds')
    json_data = r.json()
    return json_data


@cachetools.func.ttl_cache(ttl=60*10)
def epa_aqi_api():
    """
    空氣品質指標(AQI)
    https://data.gov.tw/dataset/40448
    每小時提供各測站之空氣品質指標（AQI），原始資料版本公告於空氣品質監測網https://taqm.epa.gov.tw
    [
        {
            "SiteName": "桃園(觀音工業區)",
            "County": "桃園市",
            "AQI": "83",
            "Pollutant": "細懸浮微粒",
            "Status": "普通",
            "SO2": "0.5",
            "CO": "",
            "CO_8hr": "",
            "O3": "15",
            "O3_8hr": "31",
            "PM10": "46",
            "PM2.5": "31",
            "NO2": "13",
            "NOx": "13",
            "NO": "0.4",
            "WindSpeed": "0.3",
            "WindDirec": "116",
            "PublishTime": "2020-02-29 23:00",
            "PM2.5_AVG": "28",
            "PM10_AVG": "46",
            "SO2_AVG": "1",
            "Longitude": "121.128044",
            "Latitude": "25.063039",
            "SiteId": "312"
        }, ...
    ]
    """
    start = int(time.time())
    url = 'https://opendata.epa.gov.tw/ws/Data/AQI/?$format=json'
    r = requests.get(url)
    end = int(time.time())
    logging.getLogger(__name__).info(f'{__name__} took {end - start} seconds')
    json_data = r.json()

    # build K-D tree for all positions
    site_coords = []
    for site in json_data:
        lat = float(site['Latitude'])
        lon = float(site['Longitude'])
        site_coords.append([lat, lon])
    tree = build_kd_tree(site_coords)
    return json_data, tree


def gps_dms_to_dd(dms):
    """
    :param dms: list of degrees, minutes, seconds
    :return:
    """
    degrees, minutes, seconds = dms[0], dms[1], dms[2]
    decimal_degrees = degrees + (minutes/60.0) + (seconds/3600.0)
    return decimal_degrees


@cachetools.func.ttl_cache(ttl=60 * 10)
def uv_api():
    """
    紫外線即時監測資料
    https://data.gov.tw/dataset/6076
    環保署和中央氣象局設於全國紫外線測站每小時發布之紫外線監測資料（環保署及中央氣象局資料已整合成1個檔）
    主要欄位說明:
    County(縣市)、PublishAgency(發布機關)、PublishTime(發布時間)、SiteName(測站名稱)、UVI(紫外線指數)、WGS84Lat(緯度（WGS84）)、WGS84Lon(經度（WGS84）)
    :return:
    [
        {
            "County": "花蓮縣",
            "PublishAgency": "中央氣象局",
            "PublishTime": "2020-03-02 09:00",
            "SiteName": "花蓮",
            "UVI": "0.88",
            "WGS84Lat": "23,58,30",
            "WGS84Lon": "121,36,48"
        },
    ]
    """
    start = int(time.time())
    url = 'https://opendata.epa.gov.tw/ws/Data/UV/?$format=json'
    r = requests.get(url)
    end = int(time.time())
    logging.getLogger(__name__).info(f'{__name__} took {end - start} seconds')
    json_data = r.json()
    # transform dms unit to dd
    for j in json_data:
        lat_dms = [int(d) for d in j['WGS84Lat'].split(',')]
        j['lat'] = gps_dms_to_dd(lat_dms)
        lon_dms = [int(d) for d in j['WGS84Lon'].split(',')]
        j['lon'] = gps_dms_to_dd(lon_dms)

    # build K-D tree for all positions
    site_coords = []
    for site in json_data:
        lat = float(site['lat'])
        lon = float(site['lon'])
        site_coords.append([lat, lon])
    tree = build_kd_tree(site_coords)
    return json_data, tree
