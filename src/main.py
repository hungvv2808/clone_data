import src.process as process
import json

URL = None
EMAIL = None
PASSWORD = None


def write_file(data, file_name='data.json'):
    with open(file_name, 'w') as export_file:
        data_json = json.loads(data)
        json.dump(data_json, export_file)


if __name__ == '__main__':
    cookies_dump = process.get_cookies(url=URL, email=EMAIL, password=PASSWORD)
    list_product = process.get_data(url=URL, entity='products', cookies=cookies_dump, api_version='2021-01')
    write_file(data=list_product)
    print('Jump to file complete. Check the data.json file !!!')
