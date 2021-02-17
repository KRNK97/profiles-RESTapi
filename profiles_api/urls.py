from django.urls import path, include

from rest_framework.routers import DefaultRouter
from profiles_api import views


# creater router for viewset
router = DefaultRouter()
# register viewset on router
router.register('hello-viewset', views.HelloViewSet, basename="hello-viewset")
# router will generate all urls automatically

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('', include(router.urls)),
]
