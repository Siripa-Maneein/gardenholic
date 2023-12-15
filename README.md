GardenHolic
===============
## Team Members
1. Siripa Maneein 6410545614
2. Jindaporn Sookying 6410546106
3. Kulisara Wiangin 6410545410
4. Nartnatta Krivichian 6410545509

## Project overview and features

Keeping plants healthy can be a challenge, which is why we're developing a tool to determine when to water them with the use of sensors and weather prediction. 


## Required libraries and tools 
```
Python 3.10.6
DBUtils
PyMySQL
connexion
connexion[swagger-ui]
python_dateutil
setuptools
swagger-ui-bundle
flask_testing
coverage
nose
pluggy
py
randomize
tox
node-red
```

## Instructions for building and running
1. Open gardenholic folder in vscode
2. Start new terminal
3. Creare virtual environment
```
python3 -m venv env
```
4. Activate the virtual environment
```
. env/bin/activate
```
5. Install dependencies
```
pip install -r requirements.txt
```
6. Create config.py according to config.py.example
7. Run the server
```
python app.py
```
8. Add new terminal
9. For Mac, install node red on your terminal (if not yet installed) 
```
sudo npm install -g --unsafe-perm node-red
```
For other operating system, please visit https://nodered.org/docs/getting-started/local
10. Run node-red server
```
node-red
```
11. Copy everything in node-red.json
12. Visit http://127.0.0.1:1880/
13. Select menu in the top right corner and click import. 
14. Then, paste everything in No.11 and click import
15. Deploy all nodes
11. Visit http://127.0.0.1:1880/ui/ to view the ui of our application
