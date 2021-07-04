**NAME**          
___ENDGAME Python___

**DESCRIPTION**                     
___API client program with command-line and graphical interfaces___


**PREREQUISITES**  
_HOW TO INSTALL:_

Clone repository and launch virtual environment
* python3 -m venv venv/
* source venv/bin/activate
* pip install -r requirements.txt

_IF USING PYTHON 3.9:_

__brew install python-tk@3.9__

_ADD YOUR CONFIGURATION OF MYSQL TO_  
__cfg.yaml__

_**EXAMPLE**_  
host:    localhost  
user:  root  
password: somepsw   
database: endgameDatabase

**USAGE**    
_HOW TO LAUNCH (CLI FLAG INSTRUCTION):_

* __$python3 endgame.py [-h] [--gui] [--history {show,clear}]
                  [--method {GET,POST,PUT,PATCH,DELETE}] [--endpoint ENDPOINT]
                  [--params [PARAMS ...]] [--header [HEADER ...]]
                  [--body [BODY ...]] [--auth AUTH AUTH] [--yaml]__
  
_FOR HELP:_

__-h__

_FOR STARTING WITH GRAPHICAL INTERFACE USE FLAG:_  
__--gui__

_FOR HISTORY USE FLAG:_    
__--history__ show/clean

_FOR REQUEST:_

__--method__ 
* GET
  
* POST

* PUT

* PATCH

* DELETE  


_ADDING PARAMS AND HEADERS:_     
__--params__ [PARAMS ...]      
__--headers__ [HEADERS ...]


**AUTHORS**  
nkrutoholo  
kpaputsia  
mmasniy
