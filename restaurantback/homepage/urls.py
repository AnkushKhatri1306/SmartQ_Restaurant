from rest_framework import routers
from .views import *

router = routers.SimpleRouter()

router.register(r'rest', RestaurantViewset)

urlpatterns = router.urls