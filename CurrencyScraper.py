from bs4 import BeautifulSoup
import requests
from urllib import request
import re

def is_a_number(value):
    try:
        float(value.replace(',','.')) #konieczna jest zamina , na .
        return True
    except:
        return False

def is_a_percentage(value):
    percent_pattern = '(\d+\.\d+%)' #akceptuje procenty
    if re.search(percent_pattern,value):
        return True
    else:
        return False
 

# with open('index.html') as html_file:  #test offline z zapisanego pliku index.html
#     soup = BeautifulSoup(html_file,'lxml')
# resp = requests.urlopen('https://kursy-walut.mybank.pl')

resp = requests.get('https://kursy-walut.mybank.pl')
source_code = resp.text

try:    
    assert resp.status_code == 200
    print("Status code: ", resp.status_code)
except AssertionError as err:
    raise Exception(f'Assertion Error: {err}')



isHTMLCheck = 'DOCTYPE html'
if not isHTMLCheck in source_code[:50]:
    raise Exception("Read contnt in not HTML document")

endOfHTMLCheck = '2003-2020 MyBank.pl. Wszelkie prawa zastrzeżone'
if not endOfHTMLCheck in source_code:
    raise Exception("The page was not loaded fully")
else:
    print("Page loaded successfully")
    print()
    print()


source_code = resp.text
soup = BeautifulSoup(source_code,'lxml')



date = soup.find('div',class_='prawe-menu right')
date = date.find('th',class_='head')
date_str = date.text.split(' ')[6] #wartość wyłuskana ze zdania "Kursy walut - Notowanie z dnia 2020-05-22"

date_pattern = '^(19[0-9][0-9]|20[0-9][0-9])(\-)(0[1-9]|1[0-2])(\-)([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])$' #akceptuje lata 1900-2099
if(re.search(date_pattern,date_str)):
    print('Notowanie NBP z dnia: ', date_str)
print()



for currency in soup.find_all('div',class_='box_mini'):

    currency_code = currency.find('b',class_='b1').text
    currency_value = currency.find('b',class_='b2').text
    currency_percent_change = currency.find('b',class_='b3')
    
    if not len(currency_code) == 3:
        raise Exception('Currency code is not 3 characters long')

    
    if not is_a_number(currency_value):
        raise Exception('Parsed currency value is not a number')

    if not is_a_percentage(currency_percent_change.text):
        raise Exception('Parsed percentage change is not correct')

    print(currency_code, ':', currency_value)
    if 'b3 ziel' in str(currency_percent_change):
        print('Zmiana: ', '+',currency_percent_change.text)
    elif 'b3 czer' in str(currency_percent_change):
        print('Zmiana: ', '-',currency_percent_change.text)
    print()

