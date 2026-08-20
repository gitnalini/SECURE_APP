import { useState } from 'react';
import api from '../api/axios';

const ValidateLicense = () => {
  const [fingerprintHash, setFingerprintHash] = useState('');
  const [licenseKey, setLicenseKey] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);

    try {
      const response = await api.post('valid-license/', {
        fingerprint_hash: fingerprintHash,
        license_key: licenseKey
      });
      setResult(response.data.valid);
    } catch (error) {
      console.log(error.response?.data);
      setError(error.response?.data?.error || 'Failed to validate license');
    }
  };

  return (
    <>
      <h1>Validate License</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Fingerprint Hash"
          value={fingerprintHash}
          onChange={(e) => setFingerprintHash(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="License Key"
          value={licenseKey}
          onChange={(e) => setLicenseKey(e.target.value)}
          required
        />
        <button type="submit">Validate</button>
      </form>

      {result !== null && (
        <p style={{ color: result ? 'green' : 'red' }}>
          {result ? 'License is valid' : 'License is invalid'}
        </p>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </>
  );
};
export default ValidateLicense;