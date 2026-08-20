from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from .models import Vendor

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .utils.crypto import generate_keys, sign_license, verify_license

class VendorAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        company_name = request.data.get('company_name')

        if not email or not password or not company_name:
            return Response(
                {'error': 'all fields are required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Vendor.objects.filter(user__email=email).exists():
            return Response(
                {'error': 'Vendor with this email already exists'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(username=email, email=email, password=password)
        vendor = Vendor.objects.create(company_name=company_name, user=user)
        private_key,public_key=generate_keys()
        vendor.private_key=private_key
        vendor.public_key=public_key
        vendor.save()


        return Response(
            {
                'message': 'Vendor registered successfully',
                'vendor': {
                    'id': vendor.id,
                    'email': user.email,
                    'company_name': vendor.company_name,
                    'created_at': vendor.created_at,
                },
            },
            status=status.HTTP_201_CREATED,
        )
    

class VendorLoginView(APIView):

    

    def post(self,request):
        email=request.data.get('email')
        password=request.data.get('password')

        try:
            user = User.objects.get(email=email)
         
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.check_password(password):
            return Response(
                {'error': 'Invalid credentials'},
                  status=status.HTTP_401_UNAUTHORIZED
            )
         

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status=status.HTTP_200_OK
        )

      #   user = User.objects.get(email=email)
      #   if not user.check_password(password):
      #       return Response(
      #           {'error':'Invalid credentials'},
      #           status=status.HTTP_401_UNAUTHORIZED
      #       )
class VendorProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        vendor= request.user.vendor
        return Response(
            {'message':'Authenticated',
             'email': request.user.email,
             'username': request.user.username,
             'id': request.user.id,
             'company_name': vendor.company_name},
             status=status.HTTP_200_OK
   )
