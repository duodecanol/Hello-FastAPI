set PYTHONPATH=%PYTHONPATH%;C:\Users\hwal\Documents\python_projects\fastAPIHello\ChristopherGS\

# Let the DB start
python ./app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python ./app/initial_data.py