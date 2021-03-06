from django.urls import path, include

from rest_framework.routers import DefaultRouter
from profiles_api import views


# creater router for viewset
router = DefaultRouter()
# register viewset on router
router.register('hello-viewset', views.HelloViewSet, basename="hello-viewset")
# router will generate all urls automatically

# register user profile viewset
router.register('profile', views.UserProfileViewSet)

# feed viewset
router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),  # apiview
    path('', include(router.urls)),                    # viewset
    # login endpoint
    path('login/', views.UserLoginApiView.as_view()),
]
