### Стек технологий
[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)

# Проект парсинга pep
Парсер для сайта https://docs.python.org/3/ и https://peps.python.org/

## Установка:
Клонируйте репозиторий:
```
git clone git@github.com:D4rkLght/bs4_parser_pep.git
```
Создать виртуальное окружение:
```
python -m venv venv
```
Установить зависимости:
```
pip install -r requirements.txt
```
## Парсеры:
- whats_new: Парсер который выводит список изменений python.
```
python main.py whats-new [args]
```
- latest_versions: Парсер который выводит список версий python и ссылки на их документацию.
```
python main.py latest-versions [args]
```
- download: Парсер который скачивает zip архив с документацией python.
```
python main.py download [args]
```
- pep: Парсер который выводит список количества статусов pep.
```
python main.py pep [args]
```

## Над проектом работал:
Разработчик [Ярослав Андреев ](https://github.com/D4rkLght).