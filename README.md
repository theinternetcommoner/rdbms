# rdbms
flask rdbms
### commands used for this project:
pip install virtualenv  
virtualenv venv to create virtual environment  
activate vitual environment  
 - ./venv/Scripts/Activate(Windows)  
 - source venv/bin/activate(Linux)  
pip install flask  
python -m pip install gunicorn

### Example command to run with Waitress:
waitress-serve --host=0.0.0.0 --port=5555 --workers=4 app:app

### for creating requirements.txt (includes everything)
pip freeze > requirements.txt

### for creating requirements.txt (includes only those that are in use)
pip install pipreqs  
pipreqs or pipreqs --force to override existing file

### to install using requirements.txt
pip install -r requirements.txt

*** *note:* ***   
if pip install (package) is not working, please use python -m pip install (package)  

*this is not a full feature app, but I hope you find it helpful, thank you!*
