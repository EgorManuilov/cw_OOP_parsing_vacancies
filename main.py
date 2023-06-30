from src.json_utils import JSONWorker
from src.clases import HeadHunter, SuperJob
from src.utils import print_vacancies


def main():
    select_site = int(input("Введите на каком сайте будем искать вакансии:\n"
                            "1 - HeadHanter.ru,\n"
                            "2 - SuperJob.ru\n"))

    select_vacancy = input("Введите название вакансии: \n")
    select_city = input("Введите город: \n"
                        "или нажмите Enter для поиска по России")
    select_pages = input("Введите количество страниц поиска\n"
                         "или нажмите Enter для поиска всех вакансий на сайте\n")

    vacancies_json = []

    if select_site == 1:

        hh = HeadHunter(f"{select_vacancy} {select_city}")
        if select_pages == '':
            hh.get_vacancies()
        else:
            hh.get_vacancies(int(select_pages))
        vacancies_json.extend(hh.get_serialized_vacancies())
        json_saver = JSONWorker(vacancies_json)
        vacancies = json_saver.read_vacancy()
        print_vacancies(vacancies)

    elif select_site == 2:

        sj = SuperJob(f"{select_vacancy} {select_city}")
        if select_pages == '':
            sj.get_vacancies()
        else:
            sj.get_vacancies(int(select_pages))
        vacancies_json.extend(sj.get_serialized_vacancies())
        json_saver = JSONWorker(vacancies_json)
        vacancies = json_saver.read_vacancy()
        print_vacancies(vacancies)

    while True:
        select = input(
            "1 - Удалить вакансию из списка по названию\n"
            "2 - Найти вакансии соответствующие требуемой зарплате\n"
            "3 - Исключить вакансии по слову-исключению\n"
            "0 - Для выхода\n"
        )

        if select == "0":
            break
        elif select == "1":
            select_title = input("Введите название удаляемой вакансии:\n")
            vacancies = json_saver.delete_vacancy(select_title)
        elif select == "2":
            select_salary = int(input("Введите желаемую зп:\n"))
            vacancies = json_saver.get_vacancies_by_salary(select_salary)
        elif select == "3":
            select_word = input("Введите слово-исключение\n"
                                "Например Junior, Middle, Senior:\n")
            vacancies = json_saver.exception_vacancies(select_word)
        print_vacancies(vacancies)


if __name__ == "__main__":
    main()
