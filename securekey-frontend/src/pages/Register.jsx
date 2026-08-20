import { useState } from "react";
import api from '../api/axios';

const  Register =() =>{

    const [email, setEmail]=useState('')
    const [password,setPassword]=useState('')
    const[companyName,setCompanyName]=useState('')
    const [error,setError]=useState('')
    
    const handleSubmit = async(e) =>{
        e.preventDefault();
        setError('')

        try{
            const response=await api.post('register/',{
                email,
                password,
                company_name:companyName
            })
        }catch (error) {
    //  console.log(error.response.data);
        setError(error.response.data.email?.[0] || 'Something went wrong')
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
        id="comapnyname"
        type="text"
        value={companyName}
        onChange={(e) => setCompanyName(e.target.value)}
        placeholder="TATA"
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
export default Register;
