from cryptography.hazmat.primitives.asymmetric import rsa 
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

def generate_keys():
    private_key=rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key=private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem= public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem.decode('utf-8'), public_pem.decode('utf-8')


def sign_license(private_key_pem, fingerprint_hash):
    private_key=serialization.load_pem_private_key(
        private_key_pem.encode('utf-8'),
        password=None,
        backend=default_backend()
    )

    signature=private_key.sign(
        fingerprint_hash.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return base64.b64encode(signature).decode('utf-8')


def verify_license(public_key_pem, fingerprint_hash, license_key):
    # load the public key 

    public_key=serialization.load_pem_public_key(

    public_key_pem.encode('utf-8'),
    backend=default_backend()
    )
    # decode licensekey
    signature=base64.b64decode(license_key) 
    # verify public key
    try:
        public_key.verify(
            signature,
            fingerprint_hash.encode('utf-8'),
            padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    


    