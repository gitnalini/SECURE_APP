from django.shortcuts import render
from django.core.cache import cache
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle

from .utils.crypto import generate_keys, sign_license, verify_license
from .telemetry import publish_event
from .models import Vendor,Product, License
from .throttles import FingerprintRateThrottle

import logging 

logger=logging.getLogger(__name__)




class VendorLicense(APIView):
    permission_classes =[IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope='generate_license'
    def post(self,request):
        idempotency_key=request.headers.get('Idempotency-Key')
        if idempotency_key:
            cache_key = f"idempotency:{idempotency_key}"
            cached_response=cache.add( cache_key, {"status": "processing"}, timeout=86400)
            if not cached_response:
                existing=cache.get(cache_key)
                if existing and existing.get("status") == "processing":
                    return Response({"error": "Duplicate request in progress, retry shortly"}, status=status.HTTP_409_CONFLICT)
                return Response(existing, status=status.HTTP_201_CREATED)
            
        
        fingerprint_hash=request.data.get('fingerprint_hash')
        product_id=request.data.get('product_id')
        expiry_date=request.data.get('expiry_date')

        vendor=request.user.vendor
        product = Product.objects.get(id=product_id,vendor=vendor)
        private_key=vendor.private_key
        license_key = sign_license(private_key,fingerprint_hash)

        license=License.objects.create(
            product=product,
            fingerprint_hash=fingerprint_hash,
            license_key=license_key,
            expiry_date=expiry_date
        )
        publish_event(
            event_type="LICENSE_GENERATED",
            vendor_id=vendor.id,
            status="SUCCESS",
            data={
                "license_key":license_key,
                "fingerprint":fingerprint_hash,
                "expiry": expiry_date,
            }
        )
        response_data = {
        'message': 'License generated',
        'license_key': license_key,
        'fingerprint_hash': fingerprint_hash,
        'expiry_date': expiry_date,
    }

        if idempotency_key:
            cache.set(cache_key, response_data, timeout=86400)

        return Response(response_data, status=status.HTTP_201_CREATED)
         
        # return Response(
        #     {
        #         'message': 'License generated',
        #         'license_key': license_key,
        #         'fingerprint_hash': fingerprint_hash,
        #         'expiry_date': expiry_date,
        #     },
        #     status=status.HTTP_201_CREATED

        # )


class ValidLicense(APIView): 
    throttle_classes=[FingerprintRateThrottle]
    throttle_scope='valid_license'
    def post(self,request):
        fingerprint_hash = request.data.get('fingerprint_hash')
        license_key = request.data.get('license_key')



        if not license_key or not fingerprint_hash:
            return Response(
                {'error': 'Both license_key and fingerprint_hash are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        cache_key=f"license_valid:{license_key}:{fingerprint_hash}"
        cached_result=cache.get(cache_key)

        if cached_result is not None:
            print(f"CACHE HIT: License validation for {license_key}")
            return Response(cached_result,status=status.HTTP_200_OK)
        print(f"CACHE MISS: License validation for {license_key}")
        try:
            license = License.objects.get(license_key=license_key)  
        except License.DoesNotExist:
            return Response({'error':'LICENSE NOT FOUND'},  status=status.HTTP_404_NOT_FOUND)
        product=license.product
        vendor=product.vendor

        if not vendor.public_key:

            return Response({'error': 'Vendor has no public key '}, status=status.HTTP_400_BAD_REQUEST)

        today =timezone.now().date()
        if license.expiry_date and license.expiry_date<today:
            if(license.status!= 'expired'):
                license.status='expired'
                license.save()
            result_data={'valid':False,'error':'LICENSE EXPIRED'}
            cache.set(cache_key, result_data, timeout=300)
            publish_event(
            event_type="LICENSE_VALIDATION",
            vendor_id=license.product.vendor.id,
            status="EXPIRED",
            data={
                "license_key":license.license_key,
                "fingerprint":license.fingerprint_hash,
                "expiry": str(license.expiry_date),
            }
            )
            return Response(result_data,status=status.HTTP_401_UNAUTHORIZED)
        


        if license.status!='active':
            result_data={'valid':False,'error': f'LICENSE INVALID ({license.status.upper()})'}
            cache.set(cache_key,result_data,timeout=300)
            publish_event(
            event_type="LICENSE_VALIDATION",
            vendor_id=license.product.vendor.id,
            status="INVALID",
            data={
                "license_key":license.license_key,
                "fingerprint":license.fingerprint_hash,
                "expiry": str(license.expiry_date),
            }
            )
            return Response(result_data, status=status.HTTP_401_UNAUTHORIZED)      
        
    #    / public_key=vendor.public_key

        result=verify_license(vendor.public_key,fingerprint_hash, license_key)
        result_data={'valid':result}
        cache.set(cache_key,result_data,timeout=300)
        publish_event(
            event_type="LICENSE_VALIDATION",
            vendor_id=license.product.vendor.id,
            status="VALID" if result else "INVALID",
            data={
                "license_key":license.license_key,
                "fingerprint":license.fingerprint_hash,
                "expiry": str(license.expiry_date),
            }
            )
        return Response(result_data, status=status.HTTP_200_OK)
       
        
class RevokeLicense(APIView):
    permission_classes=[IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope='revoke_license'
    def patch(self,request):
        license_key=request.data.get('license_key') 

        if not license_key:
            return Response({'error':'license_k is required'},status=status.HTTP_400_BAD_REQUEST)

        try:
            license_k=License.objects.get(license_key=license_key) 
        except License.DoesNotExist:
            return Response({'error':'LICENSE NOT FOUND'},status=status.HTTP_404_NOT_FOUND)

        if license_k.product.vendor != request.user.vendor:
            return Response({'error': 'LICENSE NOT VALID FOR THIS VENDOR'}, status=status.HTTP_403_FORBIDDEN)

        # Update status in Database
        license_k.status = 'revoked'
        license_k.save()
        cache.delete(f"license_valid:{license_key}:{license_k.fingerprint_hash}")

        publish_event(
            event_type="LICENSE_REVOKED",
            vendor_id=license_k.product.vendor.id,
            status="SUCCESS",
            data={
                "license_key":license_k.license_key,
                "fingerprint":license_k.fingerprint_hash,
                "expiry": str(license_k.expiry_date),
            }

        )

        return Response({'message': 'License revoked'}, status=status.HTTP_200_OK)
        





#     Vendor must be logged in
# Send license_id in URL
# Change license status from active to revoked
# Only the vendor who owns the license can revoke it
