from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import  pandas as pd
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
# url = "https://condo.singaporeexpats.com/"
driver = webdriver.Chrome(PATH)

df_names = pd.read_csv("./../condo_name_v2.csv")

file_obj = open('./output/out.csv', 'a')
for index, row in df_names.iterrows():
    # print('check:' + row['href'])
        driver.get(row['href'])
        mrt1 = driver.find_element(By.XPATH, '//*[@id="tabs-property-amenities"]/div[1]/p[1]/b/a').text.split(' MRT STATION')[0]
        mrt2 = driver.find_element(By.XPATH, '//*[@id="tabs-property-amenities"]/div[1]/p[2]/b/a').text.split(' MRT STATION')[0]
        mrt3 = driver.find_element(By.XPATH, '//*[@id="tabs-property-amenities"]/div[1]/p[3]/b/a').text.split(' MRT STATION')[0]

        mrtDist1 = driver.find_element(By.XPATH, '//*[@id="tabs-property-amenities"]/div[1]/p[1]').text.split('Distance: ')[1].split(' km')[0]
        mrtDist2 = driver.find_element(By.XPATH, '//*[@id="tabs-property-amenities"]/div[1]/p[2]').text.split('Distance: ')[1].split(' km')[0]
        mrtDist3 = driver.find_element(By.XPATH, '//*[@id="tabs-property-amenities"]/div[1]/p[3]').text.split('Distance: ')[1].split(' km')[0]
        
        school1 = driver.find_element(By.XPATH, '//*[@id="tabs-property-amenities"]/div[5]/p[1]/b/a').text
        school2 = driver.find_element(By.XPATH, '//*[@id="tabs-property-amenities"]/div[5]/p[2]/b/a').text
        school3 = driver.find_element(By.XPATH, '//*[@id="tabs-property-amenities"]/div[5]/p[3]/b/a').text

        schoolDist1 = driver.find_element(By.XPATH, '//*[@id="tabs-property-amenities"]/div[5]/p[1]').text.split('Distance: ')[1].split(' km')[0]
        schoolDist2 = driver.find_element(By.XPATH, '//*[@id="tabs-property-amenities"]/div[5]/p[2]').text.split('Distance: ')[1].split(' km')[0]
        schoolDist3 = driver.find_element(By.XPATH, '//*[@id="tabs-property-amenities"]/div[5]/p[3]').text.split('Distance: ')[1].split(' km')[0]

        file_obj.write('"{}","{},{},{}","{},{},{}","{},{},{}","{},{},{}"\n'.format(row['name'], mrt1,mrt2,mrt3,mrtDist1,mrtDist2, mrtDist3, school1, school2,school3,schoolDist1,schoolDist2,schoolDist3))


driver.close()
file_obj.close()