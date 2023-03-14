# octo-loop-super-smasher

|METHOD|request url|required params|
|---|------------------------------------|---|
|POST |`/report/trigger_report`|store_id|
|GET |`/report/get_report`|report_id|
|POST| `/poll`|store_id, status, time_utc|


### Packages
```

Flask             2.2.3
Flask-SQLAlchemy  3.0.3
pip               22.0.2
psycopg2-binary   2.9.5
pycodestyle       2.10.0
pytz              2022.7.1
redis             4.5.1
rq                1.13.0
SQLAlchemy        2.0.5

```
### Directory Tree
```
:.
|   .gitignore
|   tasks.py           (generate report)
|   extensions.py      (db, rq objects)
|   __init__.py
|   
|           
+---helpers
|   |   date_time_helpers.py
|   |   extrapolation_helpers.py
|   |   report_helpers.py
|   |   __init__.py
|           
+---model
|   |   models.py
|   |   __init__.py
|           
+---repos
|   |   extrapolation_data.py
|   |   menu_hours.py
|   |   polls.py
|   |   report.py
|   |   timezone.py
|   |   __init__.py
|   |   
+---resources
|   |   poll.py
|   |   report.py
|   |   __init__.py

```
