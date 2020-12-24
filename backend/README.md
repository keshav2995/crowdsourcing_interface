# Requirements
Install all the requirements:

```
$ pip install -r requirements.txt
```


# Running the App
Before running the app export the FLASK_APP environment variable:

```
$ export FLASK_APP=api.py
```

## Running for the first time

First, you need to create the database for saving the warrants. Follow the following scripts to create the database. This only needs to be done once
First, create a migration repository with the following command:

```
$ flask db init
```
This will add a migrations folder to the application. The contents of this folder need to be added to version control along with your other source files.

You can then generate an initial migration:
```
$ flask db migrate -m "Initial migration."
```

The migration script also needs to be added to version control.

Then you can apply the migration to the database:
```
$ flask db upgrade
```
