## 1. API возвращает "нет поля likes" при отсутствующем поле "statistics"
```
Шаги:
1. Отправить невалидный payload с отсутствующим `statistics` на endpoint `/api/1/item`:
```
```json
payload = {
  "sellerID": 126612,
  "name": "test item",
  "price": 123
}
```
```
2. Проверить ответ JSON
```
```
Ожидаемый результат: в теле ответа - поле statistics обязательно
Фактический результат: в теле ответа - поле likes обязательно
```
```
Серьёзность: Major
Окружение:
Сервер: https://qa-internship.avito.com
API: /api/1/item
Python: 3.13
pytest: 9.0.2
requests: 2.33.1
```

## 2. Возможность создать объявление с невалидным SellerID
```
Шаги:
1. Отправить payload с sellerID = -1 на endpoint /api/1/item:
```
```json
payload = {
  "sellerID": -1,
  "name": "test item",
  "price": 123,
  "statistics": {
    "likes": 1,
    "viewCount": 1,
    "contacts": 1
  }
}
```
```
2. Проверить статус код
```
```
Ожидаемый результат: статус код 400
Фактический результат: статус код 200, объявление создано и его можно запросить через GET
```
```
Серьёзность: Critical
Окружение:
Сервер: https://qa-internship.avito.com
API: /api/1/item
Python: 3.13
pytest: 9.0.2
requests: 2.33.1
```

## 3. Возможность создать объявление с отрицательным price 
```
Шаги:
1. Отправить payload с price = -1 на endpoint /api/1/item:
```
```json
payload = {
  "sellerID": 126612,
  "name": "test item",
  "price": -1,
  "statistics": {
    "likes": 1,
    "viewCount": 1,
    "contacts": 1
  }
}
```
```
2. Проверить статус код
```
```
Ожидаемый результат: статус код 400
Фактический результат: статус код 200
```
```
Серьёзность: Critical
Окружение:
Сервер: https://qa-internship.avito.com
API: /api/1/item
Python: 3.13
pytest: 9.0.2
requests: 2.33.1
```
## 4. Возможность создать объявление с невалидным полем в statistics
```
Шаги:
1. Отправить payload с statistics.likes = -1 на endpoint /api/1/item:
```
```json
payload = {
  "sellerID": 126612,
  "name": "test item",
  "price": 123,
  "statistics": {
    "likes": -1,
    "viewCount": 1,
    "contacts": 1
  }
}
```
```
2. Проверить статус код
```
```
Ожидаемый результат: статус код 400
Фактический результат: статус код 200
```
```
Серьёзность: Critical
Окружение:
Сервер: https://qa-internship.avito.com
API: /api/1/item
Python: 3.13
pytest: 9.0.2
requests: 2.33.1
```
## 5. Возможность создать объявление с невалидным значением поля name
```
Шаги:
1. Отправить payload с name = " " на endpoint /api/1/item:
```
```json
payload = {
  "sellerID": 126612,
  "name": " ",
  "price": 123,
  "statistics": {
    "likes": 1,
    "viewCount": 1,
    "contacts": 1
  }
}
```
```
2. Проверить статус код
```
```
Ожидаемый результат: статус код 400
Фактический результат: статус код 200
```
```
Серьёзность: Major
Окружение:
Сервер: https://qa-internship.avito.com
API: /api/1/item
Python: 3.13
pytest: 9.0.2
requests: 2.33.1
```
## 6. Отличие поля code от HTTP status при GET /item/:id
```
Примеры {id}: '', '#', '/', '///', '?'
Шаги:
1. Отправить GET на /api/1/item/:id
2. Сравнить HTTP status и поле code в ответе
```
```
Ожидаемый результат: одинаковый статус код
Фактический результат: HTTP код 404, code в теле ответа = 400
```
```
Серьёзность: Major
Окружение:
Сервер: https://qa-internship.avito.com
API: /api/1/item/:id
Python: 3.13
pytest: 9.0.2
requests: 2.33.1
```

## 7. Отличие поля code от HTTP status при GET /statistic/:id
```
Примеры {id}: '', '#', '/', '///', '?', 'abc', '1', '-1', '0', 'None'

Шаги:
1. Отправить GET на /api/2/statistic/:id
2. Сравнить HTTP status и поле code в ответе
```
```
Ожидаемый результат: одинаковый статус код
Фактический результат: HTTP код 404, code в теле ответа = 400
```
```
Серьёзность: Major
Окружение:
Сервер: https://qa-internship.avito.com
API: /api/2/statistic/:id
Python: 3.13
pytest: 9.0.2
requests: 2.33.1
```

## 8. Невозможно создать объявление с price = 0
```
Шаги:
1. Отправить POST на /api/1/item:
```
```json
payload = {
  "sellerID": 500000,
  "name": "null",
  "price": 0,
  "statistics": {
    "likes": 555,
    "viewCount": 555,
    "contacts": 555
  }
}
```
```
2. Проверить статус код
```
```
Ожидаемый результат: статус код 200
Фактический результат: статус код 400
```
```
Серьёзность: Critical
Окружение:
Сервер: https://qa-internship.avito.com
API: /api/1/item
Python: 3.13
pytest: 9.0.2
requests: 2.33.1
```

## 9. Невозможно создать объявление со значениями 0 в statistics
```
Шаги:
1. Отправить POST на /api/1/item:
```
```json
payload = {
  "sellerID": 500000,
  "name": "null",
  "price": 555,
  "statistics": {
    "likes": 0,
    "viewCount": 555,
    "contacts": 555
  }
}
```
```
2. Проверить статус код
```
```
Ожидаемый результат: статус код 200
Фактический результат: статус код 400
```
```
Серьёзность: Blocker
Окружение:
Сервер: https://qa-internship.avito.com
API: /api/1/item
Python: 3.13
pytest: 9.0.2
requests: 2.33.1
```