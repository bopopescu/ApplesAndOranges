## Synopsis
this is API on Django 1.8 for ApplesandOranges project

## Motivation
Web App needs functionality for registering users/spa controllers/sending commands to controllers

## Installation
(activate your virtual env first)



### Generting tokens for existing users
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

for user in User.objects.all():
    Token.objects.get_or_create(user=user)

## Contributors
* Patrick Zhang, patdujour@gmail.com
* Xueguang Lu, xueguang.lu@gmail.com
* Ran Liu,
* Yuan Xie,

## License
Patrick Zhang, Xueguang Lu, Ran Liu, Yuan Xie
