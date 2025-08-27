from rest_framework.views import APIView
from rest_framework.response import Response

class SessionCheckView(APIView):
    def get(self, request):
        email = request.session.get('user_email')
        fullname = request.session.get('user_fullname')
        if email:
            return Response({'loggedIn': True, 'email': email, 'fullname': fullname})
        return Response({'loggedIn': False})
