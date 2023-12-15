GardenHolic
===============
## Team Members
1. Siripa Maneein 6410545614
2. Jindaporn Sookying 6410546106
3. Kulisara Wiangin 6410545410
4. Nartnatta Krivichian 6410545509

We are Software and Knowledge engineering students from faculty of Engineering, Kasetsart University.

## Project Overview

Keeping plants healthy can be a challenge, which is why we're developing a tool to determine when to water them with the use of sensors and weather prediction. 

We gather our weather prediction data from Thai Meteorological Department (TMD). We also find the accucary of this prediction data with actual weather data from TMD and our kidbright sensors data.

## Data Sources
### Primary data sources:

- **Soil moisture sensor** (ZX-SOIL) (1 ea)
- **Light sensor** (Kidbright)
- **Temperature sensor** (Kidbright)
- **Humidity sensor** (Temperature and humidity sensor KY-015) (1 ea)

### Secondary data sources: 

- [TMD API Forecast Daily](https://data.tmd.go.th/nwpapi/doc/apidoc/location/forecast_daily.html)
- [Classification of amount of light intensity in lux (low, medium, high)](https://sustainablecampus.unimelb.edu.au/__data/assets/pdf_file/0005/2839190/Indoor-plant-workshop-Light-and-Moisture-Requirements.pdf)



## Features
**Current Data**: Show latest data from kidbright sensors.
- Current sensors data gauges
- Sensors data history chart for the past 24 hours
- Should I (users) water my (their) plant text box (Yes, No)
- Level of Light Intensity (Low, Medium, High)

**TMD Comparison**: Show comparison of temperature and humidity among different sources.
- Forecast API vs Actual API line chart
- Forecast API vs Sensor line chart
- Humidity Accuracy gauges
- Temperature Accuracy gauges



## Required Libraries and Tools 
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

## Instructions for Building and Running
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
    For other operating system, please visit: [Running Node-RED locally](https://nodered.org/docs/getting-started/local)

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
