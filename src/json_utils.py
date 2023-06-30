import json
import os
from abc import ABC, abstractmethod
from src.utils import currency_coefficient
from src.clases import Vacancy

DATA_JSON = os.path.join("data", "job.json")


class Saver(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def read_vacancy(self):
        pass

    @abstractmethod
    def delete_vacancy(self, exception):
        pass


class JSONWorker(Saver):
    """ Работа с вакансиями через JSON """

    def __init__(self, data_json):
        self.add_vacancy(data_json)

    def add_vacancy(self, data_json):
        """ Создание JSON-файла с вакансиями """

        with open(DATA_JSON, 'w', encoding='utf-8') as json_file:
            json.dump(data_json, json_file, indent=4, ensure_ascii=False)

    def read_vacancy(self):
        """ Чтение вакансий из файла"""

        with open(DATA_JSON, 'r', encoding='utf-8') as json_file:
            data_vacancies = json.load(json_file)

        return [Vacancy(i) for i in data_vacancies]

    def delete_vacancy(self, vacancy_title):
        """Удаление вакансий по названию """

        with open(DATA_JSON, 'r', encoding='utf-8') as json_file:
            data_vacancies = json.load(json_file)

        indices_to_delete = []
        for index, data in enumerate(data_vacancies):
            if data['title'] == vacancy_title:
                indices_to_delete.append(index)

        if indices_to_delete:
            updated_vacancies = [data_vacancies[i] for i in range(len(data_vacancies)) if i not in indices_to_delete]

            with open(DATA_JSON, 'w', encoding='utf-8') as json_file:
                json.dump(updated_vacancies, json_file, indent=4, ensure_ascii=False)

            return [Vacancy(i) for i in updated_vacancies]

    def get_vacancies_by_salary(self, salary):
        """ Поиск вакансий по зарплате """

        with open(DATA_JSON, 'r', encoding='utf-8') as json_file:
            data_vacancies = json.load(json_file)
            vacancies_by_salary = []
            for vacancy in data_vacancies:
                if vacancy["salary_to"]:
                    if (vacancy["currency"] == "RUR" or vacancy["currency"] == "rub") and vacancy["salary_to"] > salary:
                        vacancies_by_salary.append(vacancy)
                    if vacancy["currency"] == "EUR" and vacancy["salary_to"] > (salary / currency_coefficient('EUR')):
                        vacancies_by_salary.append(vacancy)
                    if vacancy["currency"] == "USD" and vacancy["salary_to"] > (salary / currency_coefficient('USD')):
                        vacancies_by_salary.append(vacancy)

        with open(DATA_JSON, 'w', encoding='utf-8') as json_file:
            json.dump(vacancies_by_salary, json_file, indent=4, ensure_ascii=False)

        return [Vacancy(i) for i in vacancies_by_salary]

    def exception_vacancies(self, exception):
        """ Удаление вакансий по слову-исключению """

        with open(DATA_JSON, 'r', encoding='utf-8') as json_file:
            data_vacancies = json.load(json_file)

            new_vacancies = []
            for vacancy in data_vacancies:
                if exception.lower() not in vacancy["title"].lower():
                    new_vacancies.append(vacancy)

        with open(DATA_JSON, 'w', encoding='utf-8') as json_file:
            json.dump(new_vacancies, json_file, indent=4, ensure_ascii=False)

        return [Vacancy(i) for i in new_vacancies]
