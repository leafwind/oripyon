import unittest

from app.ext_apis import tw_open_data, dxy_open_data


class MyTestCase(unittest.TestCase):
    def test_ey_clarify_api(self):
        json_data = tw_open_data.ey_clarify_api()
        self.assertIsNotNone(json_data)
        self.assertIsNotNone(json_data[0])

    def test_eqa_aqi_api(self):
        json_data = tw_open_data.epa_aqi_api()
        self.assertIsNotNone(json_data)
        self.assertIsNotNone(json_data[0])

    def test_dxy_open_data(self):
        country_image_url = dxy_open_data.load_ncov_data()
        self.assertIsNotNone(country_image_url)


if __name__ == '__main__':
    unittest.main()
