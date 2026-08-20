from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email = models.EmailField(unique=True)
    company_name= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    public_key=models.TextField(blank=True,null=True)
    private_key=models.TextField(blank=True, null=True)
    # password = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name
    
class Product(models.Model):
    # vendor ,name, created at 
    vendor =models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name= models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class License(models.Model):
 
  product =models.ForeignKey(Product, on_delete=models.CASCADE)
  fingerprint_hash= models.CharField(max_length=255)
  license_key=models.TextField()
  STATUS_CHOICES =[
      ('active', 'Active'),
      ('revoked', 'Revoked'),
      ('expired', 'Expired'),
  ]
  status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
  expiry_date=models.DateField()
  created_at =models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return f"{self.product.name} - {self.status}"


class ValidationLog(models.Model):
    EVENT_TYPE_CHOICES=[
        ('LICENSE_GENERATED','License Generated'),
        ('LICENSE_REVOKED','License Revoked'),
        ('LICENSE_VALIDATION','License Validation'),
    ]

    STATUS_CHOICES=[
        ('VALID','Valid'),
        ('REVOKED','Revoked'),
        ('EXPIRED','Expired'),
        ('INVALID','Invalid'),
        ('NOT_FOUND','Not Found'),
        ('SUCCESS','Success')
    ]

    event_type=models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES)
    vendor=models.ForeignKey(Vendor, on_delete=models.CASCADE)
    license_key=models.CharField(max_length=1024)
    fingerprint=models.CharField(max_length=255, blank=True, null=True)
    expiry=models.DateField(blank=True, null=True)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES)
    timestamp=models.DateTimeField()


  

    
