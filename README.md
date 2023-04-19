<h1 align="center"> API поиска файлов </h1>

<p align="center">
  <a href="https://badgen.net/badge/python/3.10 | 3.11/blue">
      <img src="https://badgen.net/badge/python/3.10 | 3.11/blue" alt="python-version">
  </a>

[//]: # (  <a href="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">)

[//]: # (    <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">)

[//]: # (  </a>)
  <a href="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white">
    <img alt="Django" src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white">
  </a>
  <a href="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray">
    <img alt="DjangoREST" src="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray">
  </a>
  <a href="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white">
    <img alt="SQLite" src="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white">
  </a>
   <a href="https://wakatime.com/badge/user/0e21c3c1-25e0-47ee-9c0f-77ef4b6b71e2/project/d35ca18a-238f-49d8-a7ea-3126f604222c">
      <img src="https://wakatime.com/badge/user/0e21c3c1-25e0-47ee-9c0f-77ef4b6b71e2/project/d35ca18a-238f-49d8-a7ea-3126f604222c.svg" alt="wakatime">
   </a>
</p>

<p align="center">

</p>

### Описание задачи

Создайте HTTP сервер с API поиска файлов по локальной файловой системе.

#### Условия:

- API должен обрабатывать два вида запросов: создать поиск файлов, получить результаты поиска.
- Ответом на создание поиска файлов должен быть идентификатор поиска. Ответом на получение результатов поиска должен
  быть либо список путей к файлам, либо информация о том, что поиск ещё не завершился. Подробнее в "Спецификация API".
- Пользователь может указать текст, который должен содержаться в файле, чтобы файл попал в результаты поиска. Под
  текстом понимается строка в кодировке UTF-8. Вхождение строки следует искать во всех удовлетворяющих фильтрам файлах,
  даже если это не текстовые файлы.
- Пользователь может указать фильтры по свойствам файлов. Если свойства файла удовлетворяют фильтрам, то такой файл
  попадает в результаты поиска.
- Сервер должен осуществлять поиск только внутри определённой директории. Такая директория может задаваться аргументом
  при запуске сервера.
- Для сервера нужно написать набор тестов, которые будут проверять его работу.

Дополнительные условия (их выполнение необязательно, но будет плюсом)

- Сервер должен уметь искать файлы внутри архивов zip. Вложенные архивы можно не обрабатывать.

Например, в директории поиска есть архив foo.zip, а внутри архива файл bar.txt, в котором есть искомое слово. Значит
этот файл попадёт в результаты поиска — foo.zip/bar.txt .

## Спецификация API

Создать поиск файлов
`POST /search`

Пример тела запроса:

```json
{
  "text": "abs",
  "filemask": "*a*.???",
  "size": {
    "value": 42000,
    "operator": "gt"
  },
  "creation time": {
    "value": "2020-03-03T14:00:54Z",
    "operator": "eq"
  }
}
```

где:

- text — строка;
- file_mask — строка. Маска имени файла в формате glob;
- size.value — число байт;
- creation_time.value — строка в формате RFC 3339, section 5.6;
- size.operator, creation_time.operator — одно из значений: eq , gt , lt , ge , le. Значения соответствуют операторам
  сравнения "равно", "больше", "меньше", "больше или равно", "меньше или равно".

Пример ответа:

```json
{
  "search_id": "4c2a274d-462c-551a-92de-6aa86c187aa2"
}
```

Получить результаты поиска
`GET /searches/<search_id>`

Пример ответа с успешным поиском:

```json
{
  "finished": true,
  "paths": [
    "Sysinternals Suite/ADaInsight.chm",
    "Sysinternals Suite/AdaExplorer.chm",
    "git/git-2.36.1.vfs.0.0.zip/include/main.hpp",
    "git/git-2.36.1.vfs.0.0.zip/bin/gita.exe"
  ]
}
```

Пример ответа, если ничего не найдено:

```json
{
  "finished": true,
  "paths": []
}
```

Пример ответа, если поиск ещё не завершился:

```json
{
  "finished": false
}
```
