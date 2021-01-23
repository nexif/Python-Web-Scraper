from bs4 import BeautifulSoup
import requests
import re


class CurrencyScraper:

    @staticmethod
    def is_a_number(value):
        try:
            float(value.replace(',', '.'))  # konieczna jest zamina ',' w wartościach na '.'
            return True
        except:
            return False

    @staticmethod
    def is_a_percentage(value):
        percent_pattern = '(\d+\.\d+%)'  # wzorzec, który akceptuje procenty
        if re.search(percent_pattern, value):
            return True
        else:
            return False



    def is_successful_HTTP_response(self, resp):
        try:
            assert resp.status_code == 200
            print("Response status code: ", resp.status_code)
        except AssertionError as err:
            raise Exception(f'Assertion Error: {err}')

    def is_HTML_check(self, source_code):
        is_html_check = 'DOCTYPE html'
        if is_html_check not in source_code[:50]:
            raise Exception("Read contnt in not HTML document")

    def is_end_correct_check(self, source_code):
        end_of_html_check = 'Global site tag (gtag.js) - Google Analytics'
        if end_of_html_check not in source_code:
            raise Exception("The page was not loaded fully")
        else:
            print("Page loaded successfully")
            print()

    def find_and_print_all_currencies(self, soup):
        for currency in soup.find_all('div', class_='box_mini'):

            currency_code = currency.find('b', class_='b1').text
            currency_value = currency.find('b', class_='b2').text
            currency_percent_change = currency.find('b', class_='b3')

            if not len(currency_code) == 3:
                raise Exception('Currency code is not 3 characters long')

            if not self.is_a_number(currency_value):
                raise Exception('Parsed currency value is not a number')

            if not self.is_a_percentage(currency_percent_change.text):
                raise Exception('Parsed percentage change is not correct')

            print(currency_code, ':', currency_value)
            if 'b3 ziel' in str(currency_percent_change):
                print('Zmiana kursu: ', '+', currency_percent_change.text)
            elif 'b3 czer' in str(currency_percent_change):
                print('Zmiana kursu: ', '-', currency_percent_change.text)
            print()

    def print_todays_date(self, soup):
        date = soup.find('div', class_='prawe-menu right')
        date = date.find('th', class_='head')
        date_str = date.text.split(' ')[6]  # wartość wyłuskana ze zdania "Kursy walut - Notowanie z dnia 2000-01-01"

        date_pattern = '^(19[0-9][0-9]|20[0-9][0-9])(\-)(0[1-9]|1[0-2])(\-)([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])$'  # akceptuje lata 1900-2099
        if re.search(date_pattern, date_str):
            print('Notowanie NBP z dnia: ', date_str)
        print()

    def show_links(self):
        print('Jeśli chcesz poznać kurs innych walut, kliknij tutaj:')
        print('https://kursy-walut.mybank.pl/')
        print()
        print('Jeśli chcesz zobaczyć wykresy poszczególnych walut, kliknij tutaj:')
        print('https://kursy-walut-wykresy.mybank.pl/')

    def start(self):
        resp = requests.get('https://kursy-walut.mybank.pl')
        source_code = resp.text
        soup = BeautifulSoup(source_code, 'lxml')
        self.is_successful_HTTP_response(resp)
        self.is_HTML_check(source_code)
        self.is_end_correct_check(source_code)
        self.print_todays_date(soup)
        self.find_and_print_all_currencies(soup)
        self.show_links()


if __name__ == "__main__":
    obj = CurrencyScraper()
    CurrencyScraper.start(obj)
