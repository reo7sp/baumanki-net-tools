# studizba tools

Скачивает и распаковывает файлы с сайта studizba.com (ранее baumanki.net).

## Как установить

```sh
git clone https://github.com/reo7sp/baumanki-net-tools
cd baumanki-net-tools
pip3 install -r requirements.txt
```

## Как пользоваться

Скачать категорию:
```sh
./download_category.py ссылка_на_категорию ~/Desktop/studizba
```

Скачать один файл:
```sh
./download_file.py ссылка_на_файл ~/Desktop/studizba
```
