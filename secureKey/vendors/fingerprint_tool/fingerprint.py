import uuid
import hashlib
import platform

def get_machine_fingerprint():
    machine_id=str(uuid.getnode())
    cpu_info=platform.processor()
    salt="secureKeysalt"

    raw=f"{machine_id}{cpu_info}{salt}"
    fingerprint=hashlib.sha256(raw.encode()).hexdigest()

    print("="*50)
    print("YOUR FINGERPRINT:")
    print("="*50)
    print("share this to vendor to get license")
    print(fingerprint)
    return fingerprint

if __name__ == "__main__":
    get_machine_fingerprint()

    