import api from "../api/axios";
import {useEffect, useState} from 'react';
const Products=() => {
const [products, setProducts]=useState([]);
const [error,setError]=useState('');
const [name,setName]=useState('');
const [description,setDescription]=useState('');

// Your task
// Write a function handleDelete that takes a productId parameter, calls await api.delete(products/${productId}/delete/) inside a try/catch, and calls loadProducts() on success
// Add a delete <button> next to each product in your .map(), with onClick={() => handleDelete(product.id)}

const handleDelete=async(productId) =>{
    try{
        await api.delete(`products/${productId}/delete`)
        loadProducts();
    }
    catch(error){
        console.log(error.response?.data);
        setError(error.response?.data?.error || 'Failed to delete product');
    }
}
const loadProducts=async () =>{
    try{
        const response=await api.get('products/')
        setProducts(response.data.product);
        // console.log('products response:', response.data);
    }
    catch(error){
        console.log(error.response?.data);
        setError(error.response?.data?.error || 'Failed to fetch products');
    }
}

useEffect(() =>{
    loadProducts();
},[])
const handleSubmit=  async(e)=>{
    e.preventDefault();
    setError('');
try{
    await api.post('products/',{name,description})
    setName('');
    setDescription('');
    loadProducts();

}
catch(error){
    console.log(error.response.data);
    setError(error.response.data.error || 'Failed to create product');
}
}

// useEffect(()=>{
//     const loadProducts=async()=>{
//         try{
//             const response=await api.get('products/')
//             setProducts(response.data);
//         }
//         catch(error){
//             console.log(error.response.data);
//             setError(error.response.data.error || 'Failed to fetch products');

//         }
//     }
//     loadProducts();
// },[]) 

return (
    <>
    <h1>Products</h1> 
    <form onSubmit={handleSubmit}>
        <div>
            <input type="text" placeholder="Product Name" value={name} onChange={(e)=>setName(e.target.value)}
            required
            />

        </div>
        <div>
            <input type="text" placeholder="Product Description" value={description} onChange={(e)=>setDescription(e.target.value)}
            required
            />
        </div>
        <button type="submit">Create Product</button>
    </form>

 {error && <p style={{ color: 'red' }}>{error}</p>}

      {/* Product List */}
      <h3>Product List</h3>
      {products.map((product) => (
<p key={product.id}>
  ID: {product.id} — {product.name}
  <button onClick={() => handleDelete(product.id)} style={{ marginLeft: '8px' }}>
    Delete
  </button>
</p>
      ))}
    </>
)
}
export default Products;
