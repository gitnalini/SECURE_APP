import {Link} from "react-router-dom";
import {useContext} from "react";
import {AuthContext} from "../context/AuthContext";

const Navbar =() =>{
const {isLoggedIn, logout}=useContext(AuthContext);
return(
<nav style ={{ display: "flex", gap:"15px", padding:"10px", background:"#f4f4f4"}}>
    {isLoggedIn?(
        <>
        <Link to ="/dashboard">Dashboard</Link>
        <Link to="/products">Products</Link>
        <Link to="/licenses">Licenses</Link>
        {/* <Link to="/validate-license">Validate License</Link> */}
        <button onClick={logout}>Logout</button>
        </>
    ):(
        <>
        <Link to="/login"> Login</Link>
        <Link to="/register">Register</Link> 
        </>
    )}
    <Link to="/validate-license">Validate License</Link>
</nav>
);
};
export default Navbar;