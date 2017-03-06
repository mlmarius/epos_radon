## EPOS Radon Service

microservice enabling retrieval of Radon data

## Installation

Need to install a mysql connector capable of running multiple queries at a time

```
sudo apt install python-mysql.connector
```

Clone the github repo
```
git clone https://github.com/mlmarius/epos_radon.git
```

then cd into the installation dir
```
cd epos_radon
```

make sure all requirements are installed
```
pip install -r requirements.txt
```

now copy or move the config file
```
mv config.ini.sample config.ini
```

Dont't forget to edit config.ini and replace your own config details 
so that the app has access to the database created from geochem_TABOO_DB_v2.3_withdata.sql

Now run the app
```
python radon.py
```

You should now be able to access the app on port 8888 or your configured service port

## Docker

### Building the image
```
docker build -t base_radon .
```

### Running the image

The image will use the following environment variables if available. Database configuration is mandatory.

Example docker container built from image. App will be accessible on port 8888, localhost.

```
docker run -e EP_DB_HOST='db_seismo' \
-e EP_DB_USER='root' \
-e EP_DB_PASS='db_pass' \
-e EP_DB_DB='geochem_taboo' \
--link db_seismo:db_seismo -p 8888:8888 -d --name epos_radon base_radon
```
