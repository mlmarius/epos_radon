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

Now run the app
```
python radon.py
```

You should now be able to access the app on port 8888 or your configured service port
