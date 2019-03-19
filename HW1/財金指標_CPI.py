from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import requests
import pandas as pd

path = '/Users/selina920063/Desktop/chromedriver'

#先呼叫chromdedriver
main_driver = webdriver.Chrome(path)

#告訴chromedriver 等下要找的element 如果沒有找到，要等10秒讓他們生完
main_driver.implicitly_wait(20)

#打開目標網頁 (資料量龐大請耐心等候)
main_driver.get('https://www.bls.gov/cpi/data.htm')

nxt_page_elems = main_driver.find_elements_by_class_name('col-b')
nxt_page_ele = nxt_page_elems[6]
nxt_page_ele.click()

download_ele = main_driver.find_element_by_link_text('cu.data.2.Summaries')
download_ele.click()

txt_ele = main_driver.find_element_by_xpath('/html/body/pre')

#把頁面的所有資料抓下來 (text, data type: string)
cpi_data = txt_ele.text

#切割cpi_data的整串string (data type: list)
cpi_lst = cpi_data.split()

#從cpi_lst取出需要的資料
def check(lst, name):
    data_lst = []
    for i in range(5, len(lst), 4):
        if lst[i] == name:
            if int(lst[i+1]) > 1946:
                if lst[i+2] != 'M13':
                    data_lst.append(lst[i+3])
    return data_lst

cpi_NSA = check(cpi_lst, 'CUUR0000SA0') # 挑出資料--CPI (not seasonally adjusted)
cpi_SA = check(cpi_lst, 'CUSR0000SA0') # 挑出資料--CPI (seasonally adjusted)
datelist = pd.date_range(start = '1947-01-31', end = '2019-02-28', freq = 'M').tolist() #create a time list

#將挑出的資料放進cpi (data type: dictionary)，並存在Pandas的DataFrame中
cpi = {'Date':datelist, 'CPI_not_SA':cpi_NSA, 'CPI_SA':cpi_SA}
cpi_df = pd.DataFrame(cpi)
print(cpi_df.head(20))

