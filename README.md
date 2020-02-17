# UDACasting

pg_ctl -D /usr/local/var/postgres start

FLASK_APP=app.py FLASK_DEBUG=true FLASK_ENV=development flask run

## Testing

To run the tests, run
```
dropdb UDACasting
createdb UDACasting
psql UDACasting < casting.psql
python3 test.py
```