# Eanmble_Ts

NB: the foolowing documentation assummes that you are working an avtivated virtualenv. if new to the subject click here for a quickstart 
## Configuration 

KEY			|	VALUE
SECRET_KEY	| <You choose>
CONFIG		| default, testing, production, development

LAUNCH CONFIGURATION
    TESTING
        NB: configuration done on a windows machine
        export CONFIGURATION=testing / default
        Runthe deploy command this should create the databse tables as well as create a suoer user account
            python manage.py deploy
        now you just have to start the server vua the below command
            python manage.py runserver
        
        Ps: 
        
    PRODUCTION
        for a production case setup there are some crucial environment variables that you need to set. a comprehensive variables list is provided in the table below:

