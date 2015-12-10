How to test the project by running local server
INSTRUCTIONS FOR UBUNTU

  $ sudo apt-get update
  $ sudo apt-get install python3-pip httpie
  
  $ pip3 install django djangorestframework
  $ cd django-project // Note: this is the root directory of the project you cloned
  $ python3 manage.py runserver 0.0.0.0:8000
  
  // Example
  $ http http://0.0.0.0:8000/users/ username='a_user' password='testing123' email='a@gmail.com' address='mux' city='mux' phone_number='911'
  
  // To view the admin panel you need to create a superuser.
  $ python3 manage.py createsuperuser
  
  // then in your webbrowser.
  $ http://0.0.0.0:8000/admin

