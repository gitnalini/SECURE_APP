from rest_framework.throttling import ScopedRateThrottle
from rest_framework.throttling import SimpleRateThrottle

class FingerprintRateThrottle(ScopedRateThrottle):
    def get_cache_key(self, request, view):
        fingerprint=request.data.get('fingerprint_hash')
 
        if fingerprint: 
            ident=fingerprint
        else:
            ident=self.get_ident(request)

        return self.cache_format % {
            'scope':self.scope,
            'ident':ident
        }
   
          
    
