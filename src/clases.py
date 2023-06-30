from abc import ABC, abstractmethod
# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH и SJ
import requests

# Пакет для удобной работы с данными в формате json
import json

# Модуль для работы со значением времени
import time

# Модуль для работы с операционной системой. Будем использовать для работы с файлами
import os

from src.exceptions import ParsingError


class APIVacancies(ABC):
    """Класс для работы с API вакансиями с сайта"""

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunter(APIVacancies):
    """Класс для работы с API сайта hh.ru"""
    hh_url = 'https://api.hh.ru/vacancies'
    sleep_time = 0.5

    def __init__(self, vacancy):
        self.headers = {
            "User-Agent": "MyApp / 1.0(my - app - feedback @ example.com)"
        }

        self.params = {
            'text': vacancy,  # Текст фильтра
            'area': 113,  # Поиск осуществляется по вакансиям России - 113 (город фильтруется ключевым словом)
            'page': None,
            'per_page': 100,  # Кол-во вакансий на 1 странице
            'archived': False  # Не включать архивные вакансии
        }

        self.vacancies = []

    def get_request(self):
        """ Создание запроса на сайт HH.ru """

        response = requests.get(self.hh_url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения данных {response.status_code}")
        data = response.json()
        return data

    def get_vacancies(self, pages_amount=20):
        """ Получение списка вакансий с сайта HH.ru """

        self.vacancies.clear()

        for page in range(0, pages_amount):
            self.params['page'] = page
            try:
                page_vacancies = self.get_request()["items"]
                print(f"({self.__class__.__name__}) Загружаю {page + 1} страницу с вакансиями")
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
            if (self.get_request()['pages'] - page) <= 1:  # Проверка на последнюю страницу, если вакансий меньше 2000
                break
            time.sleep(self.sleep_time)

    def get_serialized_vacancies(self):
        """ Приведение вакансий к общему виду """

        general_vacancies = []
        for vacancy in self.vacancies:
            general_vacancy = {
                "title": vacancy['name'],
                "employer": vacancy["employer"]["name"],
                "url": vacancy["alternate_url"],
                "description": vacancy["snippet"]["responsibility"]
            }
            salary = vacancy["salary"]
            if salary:
                general_vacancy["salary_from"] = salary["from"]
                general_vacancy["salary_to"] = salary["to"]
                general_vacancy["currency"] = salary["currency"]
            else:
                general_vacancy["salary_from"] = None
                general_vacancy["salary_to"] = None
                general_vacancy["currency"] = None

            general_vacancies.append(general_vacancy)

        return general_vacancies


class SuperJob(APIVacancies):
    """Класс для работы с API сайта sj.ru"""
    sj_url = 'https://api.superjob.ru/2.0/vacancies/'
    sleep_time = 0.5

    def __init__(self, vacancy):
        self.headers = {
            "Host": "api.superjob.ru",
            "X-Api-App-Id": "v3.r.137604708.4625e11082f169e37b34e82326c54d5f8246fda6.1d5ab90621c5c13d3650f5b8eb40e2cca239d3e0",
            "Authorization": "Bearer r.000000010000001.example.access_token",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        self.params = {
            'keyword': vacancy,  # Ключевое слово для поиска вакансий
            'town': 0,  # Поиск осуществляется по вакансиям России - 113 (город фильтруется ключевым словом)
            'count': 100,  # Количество результатов
            'page': None,
            'archived': False
        }
        self.vacancies = []

    def get_request(self):
        """ Создание запроса на сайт SuperJob.ru """

        response = requests.get(self.sj_url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения данных {response.status_code}")
        data = response.json()
        return data

    def get_vacancies(self, pages_amount=20):
        """ Получение списка вакансий с сайта SuperJob.ru """

        self.vacancies.clear()

        for page in range(0, pages_amount):
            self.params['page'] = page
            try:
                page_vacancies = self.get_request()["objects"]
                print(f"({self.__class__.__name__}) Загружаю {page + 1} страницу с вакансиями")
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
            if not self.get_request()['more']:  # Проверка на "есть ли ещё результаты", если вакансий меньше 2000
                break
            time.sleep(self.sleep_time)

    def get_serialized_vacancies(self):
        """ Приведение вакансий к общему виду """

        general_vacancies = []
        for vacancy in self.vacancies:
            general_vacancy = {
                "title": vacancy["profession"],
                "employer": vacancy["firm_name"],
                "url": vacancy["link"],
                "description": vacancy["candidat"],
                "salary_from": vacancy["payment_from"],
                "salary_to": vacancy["payment_to"],
                "currency": vacancy["currency"]
            }

            general_vacancies.append(general_vacancy)

        return general_vacancies


#

class Vacancy:
    """Класс для работы с вакансиями"""

    def __init__(self, vacancy):
        self.title = vacancy["title"]
        self.employer = vacancy["employer"]
        self.url = vacancy["url"]
        self.description = vacancy["description"]
        self.salary_from = vacancy["salary_from"]
        self.salary_to = vacancy["salary_to"]
        self.currency = vacancy["currency"]

    def __str__(self):
        return f"Название вакансии: {self.title}\n" \
               f"Работодатель: {self.employer}\n" \
               f"Ссылка: {self.url}\n" \
               f"Описание: {self.description}\n" \
               f"Валюта: {self.currency}\n" \
               f"Зарплата от: {self.salary_from}\n" \
               f"Зарплата до: {self.salary_to}\n" \
               f"{'-' * 30}\n"
