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

df = pd.DataFrame({'name': [], 'score': []})

input1 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/div/div/div/div[1]/div[2]/div/div/input[1]')
submit_button = driver.find_element(By.XPATH, '//*[@id="showme"]')

def checkIfResultMatch(condoName):
    global df
    # driver.implicitly_wait(5)
    time.sleep(2)
    resultItem = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/div/div/div/div[1]/div[2]/div/ul/li/a')
    if resultItem.text.lower() == condoName.lower():
        resultItem.click()
        submit_button.click()
        time.sleep(1)
        percentage = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/div/div/div/div[3]/div[1]').text
        df = df.append({'name': condoName, 'score': percentage}, ignore_index=True)
        print(condoName+ ' score: '+percentage)
    else:
        df = df.append({'name': condoName, 'score': 'null'}, ignore_index=True)
        print(condoName + " not found")

def checkIfResultPanelOccurs(condoName):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[1]/div/div/div/div[1]/div[2]/div/ul'))
        )
        checkIfResultMatch(condoName)
    finally:
        pass

df_names = pd.read_csv("./condo-names.csv")

for index, row in df_names.iterrows():
    input1.send_keys(Keys.CONTROL + "a")
    input1.send_keys(Keys.DELETE)
    input1.send_keys(row['name'])
    checkIfResultPanelOccurs(row['name'])
    

df.to_csv("./output/condo_scores.csv", index=False)
# driver.close() # close current tab
# driver.quit() # close the entire browser