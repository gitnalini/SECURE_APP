from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model=Vendor
        fields=['email', 'company_name', 'password', 'created_at', ]
        read_only_fields =['created_at',] 
        # extra_kwargs ={
        #     'password': {'write_only': True},
        #     'email': {'required': True},
        #     'company_name': {'required': True}
        # }

