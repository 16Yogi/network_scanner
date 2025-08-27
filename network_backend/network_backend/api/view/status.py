from rest_framework.views import APIView
from rest_framework.response import Response

class SessionStatus(APIView):
    def get(self, request):
        if request.session.get('user_email'):
            return Response({"loggedIn": True})
        return Response({"loggedIn": False})