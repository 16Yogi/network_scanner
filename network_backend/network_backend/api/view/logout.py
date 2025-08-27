from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LogoutView(APIView):
    def post(self, request):
        request.session.flush()  
        return Response({
            'message': 'Logout successful',
            'redirect': '/login'
        }, status=status.HTTP_200_OK)
