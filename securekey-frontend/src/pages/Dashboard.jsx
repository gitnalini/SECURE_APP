import api from "../api/axios";
import { useEffect, useState } from "react";
import {useNavigate} from  'react-router-dom';
import {AuthContext} from '../context/AuthContext.jsx';
import {useContext} from 'react';

const Dashboard=() =>{
    const {logout} =useContext(AuthContext);
    const [vendor,setVendor]=useState(null)
    const [error, setError] = useState('');
    const navigate =useNavigate();

    const handleLogout =() =>{ 
        logout();
        navigate('/login');
        
    }

    useEffect(() =>{
        const loadVendor=async() =>{

            try{ 
                const response = await api.get('login-status/');
                setVendor(response.data);

            }catch(error){
                console.log(error.response.data)
                setError(error.response.data.error || 'failed')
            }
        }
        loadVendor();
    },[])
return (
  <>
    <h1>Dashboard</h1>
    {vendor && <p>Welcome, {vendor.company_name}</p>}

    <button onClick={handleLogout}>Logout</button>
  </>
)

}
export default Dashboard;
 
 
 