# baumanki.net tools

Скачивает и распаковывает файлы с сайта baumanki.net.

## Как установить

```sh
pip3 install -r requirements.txt
```

## Как пользоваться

Скачать категорию:
```sh
./download_category.py http://baumanki.net/filearray/high-school/category-***.html ~/Desktop/baumankinet
```

Скачать один файл:
```sh
./download_file.py http://baumanki.net/filearray/file-info-***.html ~/Desktop/baumankinet
```