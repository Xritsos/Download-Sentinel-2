# Download-Sentinel-2
Download Sentinel-2 products using eodag

## How to run it
1. Open Copernicus Browser (https://browser.dataspace.copernicus.eu/)
2. Open main.py
3. Set parameters (Satellite options inside the `satellite-list.yml`)
4. Copy the created polygon from Copernicus Browser (as is) (image below)

> Polygon does not have to cover the whole Sentinel tile. If it falls inside it the whole SAFE file is downloaded.

All data are downloaded inside the `sentinel-2` directory. It can be changed inside `the main.py`.

![alt text](https://github.com/Xritsos/Download-Sentinel-2/blob/main/images/image.png?raw=true)

> Recommendation: Export your username and password to system variables and avoid hardcoding them (as is now)

## Python version
Python 3.9 was used but newer versions should work as well. Also `requirements.txt` should be updated.

## Multiple date download
Simply create a loop over `main.py` passing dates from a list of dates.