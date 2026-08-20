 

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from .models import Vendor,Product, License

from rest_framework.permissions import IsAuthenticated

class ProductView(APIView):
    permission_classes =[IsAuthenticated]
    def get(self,request):
        vendor=request.user.vendor
        product=Product.objects.filter(vendor=vendor)
        data=[{'id':p.id, 'name':p.name,'created_at':p.created_at} for p in product ]
        return Response(
            { 
                'product': data 
            },
            status=status.HTTP_200_OK
        )      

    def post(self,request):
        name=request.data.get('name')
        vendor=request.user.vendor
        product=Product.objects.create(name=name, vendor=vendor)
        return Response({
            'message': 'Product created',
            'product': {
                'id': product.id,
                'name': product.name,
                'created_at': product.created_at
            }
        }, status=status.HTTP_201_CREATED)
    
class ProductDeletView(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,product_id):
        try:
            product=Product.objects.get(id=product_id,vendor=request.user.vendor)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        product.delete()

        return Response({'message': 'Product deleted'}, status=status.HTTP_200_OK)



 
