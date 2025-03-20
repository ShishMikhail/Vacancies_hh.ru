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

![image](https://github.com/user-attachments/assets/d67b7384-39b9-48c6-a7e9-3318ca341e82)



