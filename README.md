# AMIV Beerlog

A tool to track free beverage consumption offered to members written in Python 3. It allows to see the the statistics of consumed beer and coffee. This tool is connected with the user database of the [AMIV API](https://github.com/amiv-eth/amivapi) to check for permissions to access the statistics and to check for free beer/coffee.

If you want to write your application for reporting product consumptions, see the API documentation at [README_API.md](README_API.md).

## Deployment

is done via GitLab CI pipeline. The procedure has to be worked out.

## Development

To start the app locally for development, do the following:

1. clone this repo
2. create a python3 virtual environment: `virtualenv venv`
3. and activate it: `source venv/bin/activate`
4. install the requirements inside the virtualenv: `pip install -r requirements.txt`
5. set the following environment variables: `export FLASK_APP="run.py"`, `export FLASK_CONFIG="development"`, and `export FLASK_DEBUG=1`
6. create the local settings file with all the juicy secrets inside in `instance/config.py`. The two following options must be set: `SQLALCHEMY_DATABASE_URI` and `SECRET_KEY`. See next section.
7. run the flask app: `flask run`

### Creating a local DB for development

You can spin up a local database server very easily with docker.

Use the following command (make sure to replace `%USERNAME%`, `%PASSWORD%` and `%DB_NAME%` in advance!):

```bash
sudo docker run -d --name beerlog-mariadb \
     -e MYSQL_DATABASE="%DB_NAME%" \
     -e MYSQL_USER="%USERNAME%" \
     -e MYSQL_PASSWORD="%PASSWORD%" \
     -e MYSQL_RANDOM_ROOT_PASSWORD="yes" \
     -p 3306:3306 \
     mariadb:10.4
```

In the next step, edit your `config.py`:

* Set `SECRET_KEY` to some random string.
* Set `SQLALCHEMY_DATABASE_URI` to `mysql://%USER%:%PASSWORD%@localhost/%DB_NAME%`.

Last but not least, upgrade the database to the correct state with `flask db upgrade`.

### Upgrade dependencies

1. Make sure that you have activated the virtual environment with `source venv/bin/activate`.
2. Install pip-tools with `pip install pip-tools`.
3. Run `pip-compile --output-file requirements.txt requirements.in`

### How to handle database changes

Do the following if your code changes require any changes of the database schema:

1. Make sure that your local database schema is equal to the last committed migration file (found in the directory `migrations/`)
2. Generate a new migration file with `flask db migrate`.
3. Apply your changes to the local development database with `flask db upgrade`.
4. Verify that everything is ok with the database schema.
5. Commit the created migrations file. DO NOT CHANGE any migration file which is already committed!
