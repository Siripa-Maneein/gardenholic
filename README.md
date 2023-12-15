GardenHolic
===============
## Team Members
1. Siripa Maneein 6410545614
2. Jindaporn Sookying 6410546106
3. Kulisara Wiangin 6410545410
4. Nartnatta Krivichian 6410545509

## Project overview and features

Keeping plants healthy can be a challenge, which is why we're developing a tool to determine when to water them with the use of sensors and weather prediction. 

We gather our weather prediction data from Thai Meteorological Department. We 

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
6. Create *config.py* according to *config.py.example*
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
11. Install node-red-dashboard

    Try:
    ```
    npm install node-red-dashboard
    ```
    If it is not working, for Mac, run the following command:
    ```
    sudo chown -R $(whoami) ~/.npm
    ```
    ```
    sudo npm install node-red-dashboard
    ```
12. Visit http://127.0.0.1:1880/ 
13. Select menu in the top right corner and click Manage pallete. 
14. Install node-red-dashboard
15. Select menu in the top right corner and click import. 
16. Copy everything in node-red.json
17. Then, paste everything from no.16 and click import
18. Deploy all nodes
19. Visit http://127.0.0.1:1880/ui/ to view the ui of our application
