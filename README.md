# Telecom Customer Intelligence Platform

End-to-end аналитический проект: предсказание оттока клиентов
телеком-компании, оценка потерь выручки и проверка стратегии
удержания через симуляцию A/B-теста.

## Stack
PostgreSQL · Python (pandas, scikit-learn, scipy) · Power BI · Git

## Business question
Кто из клиентов уйдёт, почему, сколько денег мы теряем
и какая стратегия удержания окупится?

## Структура
- `etl/` — загрузка данных в PostgreSQL
- `sql/` — схема и аналитические запросы
- `notebooks/` — EDA, ML-модель, A/B-симуляция
- `dashboard/` — Power BI

## Данные
[Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
(не включён в репозиторий; скачать в `data/raw/`)

## Статус
🚧 In progress