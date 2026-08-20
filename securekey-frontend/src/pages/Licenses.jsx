import {useState} from 'react';
import api from '../api/axios';

 
const Licenses=()=>{
  const [productId, setProductId] =useState('');
  const [fingerprintHash, setFingerprintHash]=useState('');
  const [expiryDate,setExpiryDate]=useState('');
  const [generateLicense, setGenerateLicense]=useState('');
  const [error,setError]=useState('');
  const [revokeId, setRevokeId] =useState('');
  const [revokeMessage, setRevokeMessage]=useState('');  
 

    const handleGenerate= async(e) =>{
    e.preventDefault();
    setError('');
    const IdempotencyKey=crypto.randomUUID();
        try{

            const response=await api.post('vendor-license/',{
                product_id: productId,
                fingerprint_hash: fingerprintHash,
                expiry_date: expiryDate
            },
        {headers:{
            'Idempotency-Key': IdempotencyKey,
        }})
            setGenerateLicense(response.data);
        }
        catch(error){
            console.log(error.response?.data);
            setError(error.response?.data?.error || 'Failed to generate license');
        }
    }

    const handleRevoke=async(e)=>{
        e.preventDefault();
        setRevokeMessage('');

        try{
            const response=await api.patch('license/revoke/',{license_key:revokeId})
            setRevokeMessage(response.data.message);
        }
        catch(error){
            console.log(error.response?.data);
            setRevokeMessage(error.response?.data?.error || 'Failed to revoke license');
        }
    }
    return(
        <>
        <h1>Licenses</h1>

        <h3>Generate License</h3>
        <form onSubmit={handleGenerate}>
            <input
                type="text"
                placeholder="Product ID"
                value={productId}
                onChange={(e) => setProductId(e.target.value)}
            />
            <input
                type="text"
                placeholder="Fingerprint Hash"
                value={fingerprintHash}
                onChange={(e) => setFingerprintHash(e.target.value)}
            />
            <input
                type="text"
                placeholder="Expiry Date (YYYY-MM-DD)"
                value={expiryDate}
                onChange={(e) => setExpiryDate(e.target.value)}
            />
            <button type="submit">Generate License</button>
            {generateLicense && <p>License Key: {generateLicense.license_key}</p>}
            {error && <p style={{color:'red'}}>{error}</p>}
        </form>

        <h3>Revoke License</h3>
        <form onSubmit={handleRevoke}>
            <input
                type="text"
                placeholder="License Key"
                value={revokeId}
                onChange={(e) => setRevokeId(e.target.value)}
            />
            <button type="submit">Revoke License</button>
            {revokeMessage && <p>{revokeMessage}</p>}
        </form>
        </>
    )
}
export default Licenses;