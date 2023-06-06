# Примеры реализации различных схем взаимодействия с базой данных в Flask

Данный репозиторий содержит несколько иллюстративных примеров различных схем взаимодействия с базой данных.

Все примеры основаны на проекте Flaskr, входящем в состав авторских примеров для [библиотеки Flask](https://github.com/pallets/flask/tree/main/examples/tutorial).

Адаптация выполнена Анатолием Полетаевым aka Shtepser.


## Содержимое
1. `flaskr-original` — изначальный Flaskr. Обращение к базе данных выполняется с помощью SQL-запросов, выполняемых в обработчиках HTTP-запросов.
2. `flaskr-separated-db` — выполнение запросов выделено в отдельные функции в модуле `db`.
3. `flaskr-active-record` — используется объектно-реляционное отображение по шаблону «активная запись» (Active Record).
4. `flaskr-flask-sqlalchemy` — используется объектно-реляцоное отображение по шаблону Data Mapper с помощью библиотеки [SQLAlchemy](https://www.sqlalchemy.org); её интеграция с Flask выполняется с помощью [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com).
