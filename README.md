# sec-project1-API

The project can be setup by doing the following:
``` shell
pip install -e .
cp settings.ini.dist development.ini
vim development.ini
# Fill in the empty values
pserve --reload development.ini
```

The dependencies of the project can of course be found in the `setup.py`. It's recommended to install this project in a Python 3 virtual environment.
