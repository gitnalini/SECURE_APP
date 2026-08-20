

import {createContext,useState} from 'react';

const AuthContext=createContext();

const AuthProvider =({children}) =>{
    const [isLoggedIn,setIsLoggedIn]=useState(!!localStorage.getItem('access'));
    const login=(access,refresh) =>{
        setIsLoggedIn(true);
        localStorage.setItem('access',access);
        localStorage.setItem('refresh',refresh);
    }
    const logout=()=>{
        setIsLoggedIn(false);
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
    }
    return(
        <AuthContext.Provider value={{isLoggedIn, login, logout}}>
            {children}
        </AuthContext.Provider>
    )
}
   export { AuthContext };
   export default AuthProvider;
