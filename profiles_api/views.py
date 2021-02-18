from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions


class HelloApiView(APIView):
    """test API view"""

    # this will make the api accept a char input with validations
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        "returns a list of APIView features"
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django view',
            'Gives you the most control over app logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'hello', 'an_apiview': an_apiview})

    def post(self, request):
        """Create hello message with our name"""
        # add serializer class with data passed in
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f"hello {name}"

            return Response({'message': message})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({"method": "PUT"})

    def patch(self, request, pk=None):
        """Handle partial updating of object"""
        return Response({"method": "PATCH"})

    def delete(self, request, pk=None):
        """Handle deleting an object"""
        return Response({"method": "DELETE"})


class HelloViewSet(viewsets.ViewSet):
    """Test API Viewset"""

    serializer_class = serializers.HelloSerializer
    # viewsets method correspond to actions we perfom rather than http request names

    def list(self, request):
        """return Hello message"""

        a_viewset = [
            "uses actions (list, create, retrieve, update, partial_update, destroy)",
            "Automatically maps to urls using Routers",
            "Provides more functionality with less code"
        ]

        return Response({"message": "hello", "a_viewset": a_viewset})

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f"hello {name}"
            return Response({"message": message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        return Response({"method": "Retrieve"})

    def update(self, request, pk=None):
        return Response({"method": "Update"})

    def partial_update(self, request, pk=None):
        return Response({"method": "partial_update"})

    def destroy(self, request, pk=None):
        return Response({"method": "destroy"})


# model viewsets are desgined for interfacing with models
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    # queryset is needed to tell which objects to use
    queryset = models.UserProfile.objects.all()
    # the authentication to use
    authentication_classes = (TokenAuthentication,)
    # permissions
    permission_classes = (permissions.UpdateOwnProfile,)
    # add a search by name and email filter
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user auth tokens"""
    # add a default view for browser
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    # this view will give us an auth token to add to headers as authorization


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated,)

    def perform_create(self, serializer):
        """sets user profile to logged in user"""
        # serializer is a model serializer so it has a save function to add the item
        # we can override it and use perform_create to add custom values
        serializer.save(user_profile=self.request.user)
