# create-flask-app
a cli tool that scaffolds a flask application

## examples
the following command generate a blog web app:
```bash
$ python main.py -o blog -d . -b post auth account dashboard
```
```
./blog/
├── core
│   ├── account
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates
│   │       └── account
│   │           └── index.html
│   ├── auth
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates
│   │       └── auth
│   │           └── index.html
│   ├── config.py
│   ├── dashboard
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates
│   │       └── dashboard
│   │           └── index.html
│   ├── exts.py
│   ├── __init__.py
│   ├── models.py
│   ├── post
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates
│   │       └── post
│   │           └── index.html
│   ├── static
│   │   ├── css
│   │   │   └── main.css
│   │   └── js
│   │       └── main.js
│   ├── templates
│   │   ├── about.html
│   │   └── base.html
│   └── utils.py
├── requirements.txt
└── run.py

17 directories, 27 files
```