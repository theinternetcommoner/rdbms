# rdbms
flask rdbms
#commands used for this project:
pip install virtualenv
pip install flask
python -m pip install waitress

#for creating requirements.txt (includes everything)
pip freeze > requirements.txt

#for creating requirements.txt (includes only those that are in use)
pip install pipreqs
pipreqs or pipreqs --force to override existing file

#to install using requirements.txt
pip install -r requirements.txt

*note:
if pip install (package) is not working, please use
python -m pip install (package) 
