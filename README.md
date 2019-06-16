# My Zone

[Live link](https://taniacao12.github.io/myZone/)

## Project Overview
My Zone is a website that works in a similar manner as bullet journals.

### Launch Instructions
#### Install and run on localhost
1. Go to [root repository](https://github.com/taniacao12/myZone) and click "Clone or Download" button
2. Copy the ssh/https link and run `$ git clone <link>`
3. Make sure the latest version of Python (currently Python 3.7.1) is installed. If not, download it [here](https://www.python.org/downloads/).
4. Install virtualenv by running `$ pip install virtualenv`
   * Make a venv by running `$ python3 -m venv path_to_venv`
   * Activate it by running `$ . /path_to_venv/bin/activate`
   * Deactivate it by running `$ deactivate`
5. Move into the climate_crackers directory: `$ cd myZone/`
6. **With your virtual environment activated**, download all of the app's dependencies by running
```
 (venv)$ pip install -r requirements.txt
```
7. Run `$ python app.py`
8. Launch the root route (http://127.0.0.1:5000/) in your browser to go to the login page.
