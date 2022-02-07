## ImportError

### set PYTHONPATH env variable
https://towardsdatascience.com/how-to-fix-modulenotfounderror-and-importerror-248ce5b69b1c

```shell
set PYTHONPATH=%PYTHONPATH%;C:\Users\hwal\Documents\python_projects\fastAPIHello\ChristopherGS\
```

Put this inside your package’s __init__.py file:

### For relative imports to work in Python 3.6
```python3
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
```
https://itsmycode.com/importerror-attempted-relative-import-with-no-known-parent-package/


## alembic init

```shell
set PYTHONPATH=%PYTHONPATH%;C:\Users\hwal\Documents\python_projects\fastAPIHello\ChristopherGS\

# Let the DB start
python ./app/backend_pre_start.py

# Run migrations
alembic revision --autogenerate -m "update1" 
alembic upgrade head


# Create initial data in DB
python ./app/initial_data.py
```