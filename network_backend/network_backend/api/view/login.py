# api/view/login.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from api.models.registration import UserRegistration

# class LoginView(APIView):
#     def post(self, request):
#         # Check if user is already logged in
#         if request.session.get('user_email'):
#             return Response({
#                 'message': 'User already logged in',
#                 'alreadyLoggedIn': True
#             }, status=status.HTTP_200_OK)

#         email = request.data.get('email')
#         password = request.data.get('password')

#         if not email or not password:
#             return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = UserRegistration.objects.get(email=email)
#             if check_password(password, user.password):
#                 # Set session
#                 request.session['user_email'] = user.email

#                 # Set session to expire in 1 hour (3600 seconds)
#                 request.session.set_expiry(3600)

#                 return Response({
#                     'message': 'Login successful',
#                     'csrfToken': request.META.get("CSRF_COOKIE", ""),
#                     'redirect': '/'
#                 }, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#         except UserRegistration.DoesNotExist:
#             return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserRegistration.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_email'] = user.email
                request.session['user_fullname'] = user.fullname
                request.session.set_expiry(3600)  # 1 hour

                return Response({
                    'message': 'Login successful',
                    'email': user.email,
                    'fullname': user.fullname,
                    'redirect': 'http://localhost:3000/'  
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except UserRegistration.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
