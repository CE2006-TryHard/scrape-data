from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import  pandas as pd
import time

constituencyDict = {
    'ALJUNIED':	1,
    'ANG MO KIO':	2,
    'BISHAN-TOA PAYOH':	3,
    'BUKIT BATOK':	4,
    'BUKIT PANJANG':	5,
    'CHUA CHU KANG':	6,
    'EAST COAST':	7,
    'HOLLAND-BUKIT TIMAH':	8,
    'HONG KAH NORTH':	9,
    'HOUGANG':	10,
    'JALAN BESAR':	11,
    'JURONG':	12,
    'KEBUN BARU':	13,
    'MACPHERSON':	14,
    'MARINE PARADE':	15,
    'MARSILING-YEW TEE':	16,
    'MARYMOUNT':	17,
    'MOUNTBATTEN':	18,
    'NEE SOON':	19,
    'PASIR RIS-PUNGGOL':	20,
    'PIONEER':	21,
    'POTONG PASIR':	22,
    'PUNGGOL WEST':	23,
    'RADIN MAS':	24,
    'SEMBAWANG':	25,
    'SENGKANG':	26,
    'TAMPINES':	27,
    'TANJONG PAGAR':	28,
    'WEST COAST':	29,
    'YIO CHU KANG':	30,
    'YUHUA':	31
}
PATH = "C:\Program Files (x86)\chromedriver.exe"
url = "https://www.straitstimes.com/multimedia/graphics/2020/03/singapore-general-election-ward/index.html"
driver = webdriver.Chrome(PATH)
driver.get(url)

inputAddr = driver.find_element(By.XPATH, '//*[@id="st-content-graphic"]/main/article/section[1]/div/div/div/span/div/div/input')

df_names = pd.read_csv("./raw.csv")

file_obj = open('./out.csv', 'a')
for index, row in df_names.iterrows():
        if (index >= 1229):
            address = str(row['address']).split(' ')
            postal = address[len(address) - 1]
            inputAddr.send_keys(Keys.CONTROL + "a")
            inputAddr.send_keys(Keys.DELETE)
            inputAddr.send_keys(postal) 
            time.sleep(1)
            hasResult = driver.find_element(By.CLASS_NAME, 'v-dropdown-container')

            if (hasResult.text.strip() == ''):
                print('{} | {} postal not found'.format(index, row['name']))
                file_obj.write('"{}",nan\n'.format(row['name']))
            else:
                inputAddr.click()
                inputAddr.send_keys(Keys.RETURN)
                time.sleep(1)
                constituency =  driver.find_element(By.CSS_SELECTOR, '.mapboxgl-popup-content .popover-content .title').text
                print('{} | {}: {} ({})'.format(index, row['name'], constituency, constituencyDict[constituency.upper()]))
                file_obj.write('"{}","{}"\n'.format(row['name'], constituencyDict[constituency.upper()]))

                # file_obj.write('"{}",{}\n'.format(row['name'],postal))


# driver.close()
file_obj.close()