# JI-Coursesel CLI

[![asciicast](https://asciinema.org/a/548667.svg)](https://asciinema.org/a/548667)

## Pre-requirements

Python >=3.7

```bash
pip install ji-coursesel
```

## Getting started

Show the help manual:

```bash
ji-coursesel
```

Initialize:

```bash
ji-coursesel auth
```

Refresh JSESSIONID:

```bash
ji-coursesel refresh
```

Elect:

```bash
ji-coursesel elect
```

Specify the threads number for each course (recommended to use 1 when testing):

```bash
ji-coursesel elect -x 1
```

