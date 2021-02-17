from rest_framework.views import APIView
from rest_framework.response import Response


class HelloApiView(APIView):
    """test API view"""

    def get(self, request, format=None):
        "returns a list of APIView features"
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django view',
            'Gives you the most control over app logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'hello', 'an_apiview': an_apiview})
