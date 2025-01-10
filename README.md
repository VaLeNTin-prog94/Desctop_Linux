# System Monitor Application
## Описание
Приложение для мониторинга системных ресурсов, таких как загрузка процессора, использование оперативной памяти и загрузка диска. Программа позволяет записывать данные о загрузке и сохранять их в базе данных SQLite, а также просматривать историю записей.
## Краткие характеристики
- Отображает текущее использование ЦП, ОЗУ и ПЗУ.
- Позволяет записывать данные в базу данных.
- Интуитивно понятный интерфейс на основе библиотеки Tkinter.
- Возможность просматривать историю записей.
## Технологии
- Python 3.x
- Библиотека psutil для получения данных о системных ресурсах.
- Библиотека tkinter для создания графического интерфейса.
- SQLite для хранения данных.
## Установка и настройка
### 1. Установите необходимые зависимости:
```
pip install psutil
```
### 2. Скачайте код:
- Скачайте или клонируйте репозиторий с кодом приложения.
## Использование
- Запустите приложение:
```
  python main.py
 ```
- В основном окне приложения будут отображаться текущие значения загрузки ЦП, ОЗУ и ПЗУ.
- Чтобы начать запись данных, нажмите кнопку "Начать запись". Время записи будет отображаться в нижней части окна. 
- Чтобы остановить запись, нажмите кнопку "Остановить".
- Для просмотра истории записей нажмите кнопку "Просмотреть историю". Откроется новое окно с таблицей, в которой отображаются все сохраненные записи.