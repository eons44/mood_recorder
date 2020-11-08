# Mood Recorder

## Initial Setup

### Notes

* OS is assumed to be Ubuntu 20.04 or a suitable alternative
* To make it easy to copy code, permissions have been left out. If you have questions about permissions, ask eons.

### Setup Postgresql

If you don't have postgresql installed, you can install it with:
`apt install postgresql postgresql-contrib`

make sure postgress is running on localhost with the following:
`ss -tulnp | grep 5432`
This should output something like:
`tcp     LISTEN   0        244            127.0.0.1:5432           0.0.0.0:* `

Postgress can be controlled via systemd. i.e.
```
systemctl enable postgresql
systemctl disable postgresql
systemctl start postgresql
systemctl stop postgresql
systemctl restart postgresql
```

To setup pg, just run the following:
```
source ./mr.env
cat << EOF > ./pg-setup.sql
CREATE DATABASE $MR_PG_DB;
CREATE USER $MR_PG_USER WITH ENCRYPTED PASSWORD '$MR_PG_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE $MR_PG_DB TO $MR_PG_USER;
ALTER ROLE $MR_PG_USER SET client_encoding TO 'utf8';
ALTER ROLE $MR_PG_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $MR_PG_USER SET timezone TO 'UTC';
EOF
chown postgres:postgres ./pg-setup.sql
sudo -u postgres psql -f ./pg-setup.sql
```

### Libpq

If libpq is not installed, run:
`apt install libpq-dev`

### Check Python Version

`python3 --version`

If this is anything less than 3.7, upgrade python
You can install python with something like:
`apt install python-3.8`

NOTE: if you still get 3.6..., etc. when running `python3 --version`, you may need to run something like the following (adapt for your system if necessary):
```
rm /usr/bin/python3
ln -s /usr/bin/python3.8 /usr/bin/python3
```

### Install Virtual Environment

If python3-venv is not installed, install it through apt:
`apt install python3-venv`

If python3-pip is not installed, install it through apt:
`apt install python3-pip`

```
python3 -m venv .
source ./bin/activate
pip3 install -r requirements.txt
chmod +x ./mr_project/manage.py
```

## Run Django

```
source ./bin/activate
source ./mr.env
cd ./mr_project
./manage.py makemigrations
./manage.py migrate
./manage.py runserver
```

