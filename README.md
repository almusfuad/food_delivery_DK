# Food_Delivery_API
**This project is made with Django-5.1.1 and djangorestframework 3.15.2 . An ERD is provided named as food_delivery.png**

## Getting started:
**Here will be some instruction how to download and start the project.**

### Clone project:
In your working directory, open the **CMD**. Then copy the following code to clone the **Github Repository and run the project** and Paste it
```
> git clone https://github.com/almusfuad/food_delivery_DK.git
```

### Installation:
Type the following commands to install the requirements. Assuming **[python](https://www.python.org/doc/) and [django](https://docs.djangoproject.com/en/5.1/topics/install/)** are already installed in your device.
_It is better to use **[virtual environment](https://www.freecodecamp.org/news/how-to-set-up-a-django-development-environment/)**_

**Install Packages:** 
Type the following commands
```
> cd food_delivery_DK
> pip install -r requirements.txt
```
This Commands will install a couple of packeges and dependencies. It may take some time.

## Run project:
After you successfully following all the commands and install all the packeges, move to the main part as run the project. There is a couple of steps.

_**1.  Setup Database:**_
The following commands help to setup database correctly.
```
> python manage.py makemigrations
> python manage.py migrate
```
These two commands will intregrate with database for the tables. If there is any error please search on Google.

_**2. Create Superuser:**_
To access the admin panel through Django-admin panel, create a superuser by following these commands.
```
> python manage.py createsuperuser
```
Then fillup the information those are asked in console.

_**3.  Run:**_
If all the procedure has passed successfully, now move to run the project. Follow the below command to run the project,
```
> python manage.py runserver
```

**Boom...!! You are successfully clone a repository and run the project.**


### API Documentation:
There is a file name **api_and_data.txt** which includes _> api_end_points_ and also the _> json_body_ for making a _> post request_




If there is any error feel free to [contact me](https://api.whatsapp.com/send/?phone=8801737975033&text&type=phone_number&app_absent=0) or search on the Google.