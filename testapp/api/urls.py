from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import AuthViewset, UsersViewset

app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register('auth', AuthViewset, 'auth')
router_v1.register('users', UsersViewset, 'users')

urlpatterns = [
    path('', include(router_v1.urls))
]
