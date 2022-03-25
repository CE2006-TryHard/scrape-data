from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import  pandas as pd
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
url = "https://www.onemap.gov.sg/main/v2/"
driver = webdriver.Chrome(PATH)
driver.get(url)

df_names = pd.read_csv("./raw.csv")

inputAddr = driver.find_element(By.XPATH, '//*[@id="search-text"]')
hasResult = driver.find_element(By.XPATH, '//*[@id="road_name"]')

file_obj = open('./out.csv', 'a')

for index, row in df_names.iterrows():
        # if (index < 5):
        if (row['address'] != 't'):
            file_obj.write('"{}",{},{},{}\n'.format(row['name'],row['address'], row['lat'], row['lng']))
        else:
            inputAddr.send_keys(Keys.CONTROL + "a")
            inputAddr.send_keys(Keys.DELETE)
            inputAddr.send_keys(row['name'])
            time.sleep(1)
            inputAddr.click()
            inputAddr.send_keys(Keys.RETURN)
            time.sleep(1)
            if (hasResult.text.strip() == ''):
                print(str(index) + " | " + row['name'] + ' does not exist')
                file_obj.write('"{}",,,\n'.format(row['name']))
            else:
                print(str(index) + " | " + row['name'] + ' found')
                addressFull = driver.find_element(By.XPATH, '//*[@id="start_marker"]/div[1]').text.split('\n')
                length = len(addressFull)
                address = addressFull[length-2]
                lat,lng = addressFull[length-1].split(', ')
                
                print('address: ', address)
                print('lat lng', lat, lng)
                file_obj.write('"{}","{}",{},{}\n'.format(row['name'],address,lat,lng))


# driver.close()
file_obj.close()