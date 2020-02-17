# UDACasting

pg_ctl -D /usr/local/var/postgres start

FLASK_APP=app.py FLASK_DEBUG=true FLASK_ENV=development flask run

start postgres: pg_ctl -D /usr/local/var/postgres start


## Testing

To run the tests, run
```
dropdb UDACasting
createdb UDACasting
psql UDACasting < casting.psql
python3 test.py
```