# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework import status
# # from api.serializers.registration import UserRegistrationSerializer
# # from api.models.registration import UserRegistration

# # class RegisterUser(APIView):
# #     def post(self, request):
# #         print("Request data:", request.data)
# #         serializer = UserRegistrationSerializer(data=request.data)
# #         if serializer.is_valid():
# #             print("Validated data:", serializer.validated_data)
# #             if UserRegistration.objects.filter(email=serializer.validated_data['email']).exists():
# #                 return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)
# #             serializer.save()
# #             return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# from django.middleware.csrf import get_token
# from django.shortcuts import redirect
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from api.serializers.registration import UserRegistrationSerializer
# from api.models.registration import UserRegistration


# # class RegisterUser(APIView):
# #     def post(self, request):
# #         serializer = UserRegistrationSerializer(data=request.data)
# #         if serializer.is_valid():
# #             if UserRegistration.objects.filter(email=serializer.validated_data['email']).exists():
# #                 return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)
            
# #             serializer.save()

# #             # Generate a CSRF token
# #             csrf_token = get_token(request)

# #             # Optional: Set session data (e.g., mark user as logged in)
# #             request.session['user_email'] = serializer.validated_data['email']

# #             # Return session cookie and CSRF token
# #             return Response({
# #                 "message": "User registered successfully",
# #                 "csrfToken": csrf_token,
# #                 "redirect": "/"
# #             }, status=status.HTTP_201_CREATED)
        
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class RegisterUser(APIView):
#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             if UserRegistration.objects.filter(email=serializer.validated_data['email']).exists():
#                 return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

#             serializer.save()

#             csrf_token = get_token(request)
#             request.session['user_email'] = serializer.validated_data['email']

#             return Response({
#                 "message": "User registered successfully",
#                 "csrfToken": csrf_token,
#                 'fullname': user.fullname,
#                 "redirect": "http://localhost:3000/"
#             }, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers.registration import UserRegistrationSerializer
from api.models.registration import UserRegistration


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            if UserRegistration.objects.filter(email=serializer.validated_data['email']).exists():
                return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            csrf_token = get_token(request)

            request.session['user_email'] = serializer.validated_data['email']
            request.session.set_expiry(3600)  # session expires in 1 hour

            return Response({
                "message": "User registered successfully",
                "csrfToken": csrf_token,
                "redirect": "http://localhost:3000/"  # full redirect URL
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
