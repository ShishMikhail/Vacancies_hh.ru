Общий обзор
Данный проект представляет собой веб-инструмент для мониторинга вакансий с сайта HeadHunter, специально разработанный для поддержки учебных заведений, таких как колледжи. Сервис позволяет отслеживать вакансии в разрезе бизнес-ролей и предоставляет студентам персонализированные рекомендации вакансий на основе их навыков.

Ключевые компоненты
Мониторинг вакансий:

Реализован сбор и обновление данных о вакансиях с HeadHunter.
Данные хранятся в реляционной базе данных PostgreSQL.
Вэб-сервис (Flask) позволяют пользователям анализировать вакансии в разрезе бизнес-ролей.
Рекомендации вакансий:

Реализован алгоритм, который анализирует навыки студентов и подбирает для них подходящие вакансии.
Вэб-сервис визуализирует список рекомендованных вакансий для каждого студента.

Технические детали
Стэк технологий: Python для написания скриптов и алгоритмов, PostgreSQL для хранения данных, Flask.
База данных: Спроектирована и реализована реляционная БД, которая эффективно поддерживает работу сервиса.

Сбор и обновление вакансий: В рамках демонстрации происходит сбор новых вакансий и хи обновление.
Добавление нового студента: Сервис позволяет добавлять студента с набором навыков, после чего система автоматически рассчитывает и визуализирует для него рекомендации по вакансиям.

пример использования 


Вывод всех вакансий 
![image](https://github.com/user-attachments/assets/d67b7384-39b9-48c6-a7e9-3318ca341e82)


Вывод выкансий по направлению (Реклама)
![image](https://github.com/user-attachments/assets/00c356f6-e4ea-4195-ab79-6ba8775c668a)


Добавление нового студента
![image](https://github.com/user-attachments/assets/bf957145-7181-4667-88dc-cd747b2c2243)


Карточка вакансии
![image](https://github.com/user-attachments/assets/a3978777-bc5b-4fb8-916e-6ecd542e7ac3)


Вывод вканасий по навыкам студента 
![image](https://github.com/user-attachments/assets/b3af1812-5f47-4ae0-802e-855052d6d8bc)


Схема базы данных
![image](https://github.com/user-attachments/assets/2bbb2e52-38d1-4610-8f1c-39015f70afd6)




