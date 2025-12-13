A cli to interface with the freesound API
# How to use it?
I recommend making a virtual environment in python. If you do that you dont have to install python packages system wide and only install them within the confines of your virtual environment.
To recreate a python virtual environment do this:
```
python -m venv myenv
```
After this you should go into the created folder and activate the the virtual environment in order to use it.
To activate a virtual environment do this inside the created folder:
```
source bin/activate
```
Your terminal session should now use the virtual environment.
Keep in mind that there are also other activation scripts inside the bin folder that you should be using if you use a non POSIX compliant terminal such as fish,
in which case you should be executing this:

```
source bin/activate.fish
```
Now that we have activated the virtual environment we can clone the git repo.
```
git clone https://github.com/MalekDeKalem/freesound-scraper.git
```
We can now move into the repo and also install all the dependencies of our python cli.
```
cd freesound-scraper && pip install -r requirements.txt 
```
