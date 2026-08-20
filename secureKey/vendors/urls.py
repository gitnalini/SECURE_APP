from django.urls import path 
from .serializer import VendorSerializer
from .views import VendorAPIView, VendorLoginView, VendorProfileView
from .views_license import VendorLicense, ValidLicense, RevokeLicense
from .views_product import ProductView, ProductDeletView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns =[
    path('register/', VendorAPIView.as_view(), name='vendor-register'),
    path('login/', VendorLoginView.as_view(), name='vendor-login'),
    path('login-status/', VendorProfileView.as_view(), name='vendor-login-status'),
    path('vendor-license/',VendorLicense.as_view(), name='vendor-license'),
    path('valid-license/', ValidLicense.as_view(), name='valid-license'),
    # path('license/<int:license_id>/revoke',RevokeLicense.as_view(),name='revoke-lic'),
    path('license/revoke/', RevokeLicense.as_view()),    
    path('products/', ProductView.as_view(), name='products'),
    path('products/<int:product_id>/delete/', ProductDeletView.as_view(), name='product-delete'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    

]