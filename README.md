# links-dataset
Дамп данных с проекта [https://pythondigest.ru/](https://pythondigest.ru/)

Свежий дамп всегда доступе по ссылке [https://pythondigest.ru/dataset.zip](https://pythondigest.ru/dataset.zip)


# Структура датасета

Датасет это набор `.json файлов`
Каждый `.json` файл содержит структуру:

```
[
    "links":[
        {
            "link": "ссылка на страницу",
            "data": {
                "title": "Заголовок новости",
                "description": "Описание новости",
                "type": "строка article или library",
                "label": "True/False - хорошая/плохая ссылка",
                "article": "Строка html - текст ссылки",
                "language": "Язык новости - ru или en",
            }
        },
        
        ....
        ....
        ....
        
        {
            "link": "...",
            "data": {
                "title": "...",
                "description": "...",
                "type": "...",
                "label": "...",
                "article": "...",
                "language": "...",
            }
        },
        
    ]
]
```