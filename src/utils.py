import requests
from src.exceptions import   ParsingError


def currency_coefficient(currency):

    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    try:
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения данных {response.status_code}")
        data = response.json()
        return data['Valute'][currency]['Value']
    except ParsingError as error:
        print(error)


def print_vacancies(result):
    for r in result:
        print(r, end='\n')