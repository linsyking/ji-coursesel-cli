# JI-Coursesel CLI

[![asciicast](https://asciinema.org/a/0M3EJMGSq8Qrc4M7izJjrPfhZ.svg)](https://asciinema.org/a/0M3EJMGSq8Qrc4M7izJjrPfhZ)

## Pre-requirements

Python >=3.9

```bash
pip install -r requirements.txt
```

## Getting started

Show the help manual:

```bash
python main.py
```

Initialize:

```bash
python main.py init
```

Refresh JSESSIONID:

```bash
python main.py refresh
```

Elect:

```bash
python main.py elect
```

Specify the threads number for each course (recommend to use 1 when testing):

```bash
python main.py elect -x 1
```

