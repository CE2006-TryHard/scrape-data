from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import  pandas as pd
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
url = "https://www.edgeprop.sg/en-bloc-calculator"
driver = webdriver.Chrome(PATH)
driver.get(url)

df = pd.DataFrame({'name': [], 'score': [], 'href': ''})

input1 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/div/div/div/div[1]/div[2]/div/div/input[1]')
submit_button = driver.find_element(By.XPATH, '//*[@id="showme"]')

def checkIfResultMatch(condoName, href):
    global df
    # driver.implicitly_wait(5)
    time.sleep(2)
    resultItem = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/div/div/div/div[1]/div[2]/div/ul/li/a')
    if resultItem.text.lower() == condoName.lower():
        resultItem.click()
        submit_button.click()
        time.sleep(1)
        percentage = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/div/div/div/div[3]/div[1]').text
        df = df.append({'name': condoName, 'score': percentage, href: href}, ignore_index=True)
        print(condoName+ ' score: '+percentage)
    else:
        df = df.append({'name': condoName, 'score': 'null', href: href}, ignore_index=True)
        print(condoName + " not found")

def checkIfResultPanelOccurs(condoName, href):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[1]/div/div/div/div[1]/div[2]/div/ul'))
        )
        checkIfResultMatch(condoName, href)
    finally:
        pass

df_names = pd.read_csv("./../dist/condo_dist_page.csv")

for index, row in df_names.iterrows():
    input1.send_keys(Keys.CONTROL + "a")
    input1.send_keys(Keys.DELETE)
    input1.send_keys(row['name'])
    checkIfResultPanelOccurs(row['name'], row['href'])
    

df.to_csv("./output/condo_scores.csv", index=False)
# driver.close() # close current tab
# driver.quit() # close the entire browser