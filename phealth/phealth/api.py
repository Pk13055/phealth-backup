'''
contains the router for the api routes and the like 

'''

from rest_framework.routers import DefaultRouter
from api.views import *

router = DefaultRouter()
router.register('address', AddressViewSet)

