import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import {AuthContext} from '../context/AuthContext.jsx';
import {useContext} from 'react';

const Login=()=>{
    const {login} = useContext(AuthContext);
    const navigate=useNavigate();
    const [email,setEmail]=useState('');
    const [password,setPassword]=useState('');
    const [error,setError]=useState('');

    
    const handleSubmit =async(e) =>{
        e.preventDefault();
        setError('')

        try{
            const response=await api.post('login/',{
                email,
                password,
            })
            const {access, refresh}=response.data;
            login(access,refresh); 

            console.log("Login successfully")
            navigate('/dashboard')

        }
        catch(error){
            console.log(error.response.data)
            setError(error.response.data.error || 'Login failed')
            
        }
        
    };
        return(
        <form
        onSubmit={handleSubmit}>
        <input 
        id="email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="abc@gmail.com"
        />

        <input 
        id="pass"
        type="password"
        value={password}
        onChange={(e)=> setPassword(e.target.value)}
        placeholder="Enter you password"
        />

        <button>
        SUBMIT
        </button>
        {error && <p style={{color: 'red'}}>{error}</p>}
        </form>

         
    )
}
export default Login;