 
// import { BrowserRouter,Routes,Route,Navigate} from 'react-router-dom'
// import Register from './pages/Register'
// import Login from './pages/Login'
// import Dashboard from './pages/Dashboard'
// import ProtectedRoute from './components/ProtectedRoute'
// import Products from './pages/Products'
// import Licenses from './pages/Licenses'
// import Navbar from './components/Navbar'
// import ValidateLicense from './pages/ValidateLicense'
// function App() { 
//   return (
//     <BrowserRouter>
//     <Navbar/>
// <Routes>
//   <Route path="/" element={<Navigate to="/login" replace />} />
//   <Route path="/register" element={<Register/>}/>
//   <Route path='/login' element={<Login/>}/>
  
//   <Route path='/dashboard' element={ 
//       <ProtectedRoute><Dashboard/></ProtectedRoute>
//       }/>
//   <Route path="/products" element={
//       <ProtectedRoute><Products/></ProtectedRoute>
//       }/>

//   <Route path="/licenses" element={
//   <ProtectedRoute><Licenses /></ProtectedRoute>} />


//   <Route path="/validate-license" element={<ValidateLicense />} />
// </Routes>

// </BrowserRouter>



//   )
// } 

// export default App



import { Routes, Route, Navigate } from 'react-router-dom';
import Register from './pages/Register';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import ProtectedRoute from './components/ProtectedRoute';
import Products from './pages/Products';
import Licenses from './pages/Licenses';
import Navbar from './components/Navbar';
import ValidateLicense from './pages/ValidateLicense';

function App() { 
  return (
    <>
      <Navbar />
      <Routes>
        {/* Redirect root URL / to /login */}
        <Route path="/" element={<Navigate to="/login" replace />} />

        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        
        <Route path="/dashboard" element={ 
          <ProtectedRoute><Dashboard /></ProtectedRoute>
        } />
        <Route path="/products" element={
          <ProtectedRoute><Products /></ProtectedRoute>
        } />
        <Route path="/licenses" element={
          <ProtectedRoute><Licenses /></ProtectedRoute>
        } />

        <Route path="/validate-license" element={<ValidateLicense />} />
      </Routes>
    </>
  );
} 

export default App;