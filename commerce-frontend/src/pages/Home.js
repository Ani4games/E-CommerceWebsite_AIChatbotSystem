import axios from 'axios';
import { useEffect, useState } from 'react';
import { useContext } from 'react';
import { CartContext } from '../context/CartContext';
import ProductCard from '../Components/ProductCard';
// import './Home.css';
const Home = () => {
  const [products, setProducts] = useState([]);
  const { addToCart } = useContext(CartContext);

  useEffect(() => {
    axios.get('https://fakestoreapi.com/products')
      .then(res => setProducts(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <><div className="products-grid">
      {products.map(product => (
        <ProductCard key={product.id} product={product} addToCart={addToCart} />
      ))}
    </div><h2 className="text-2xl font-semibold mb-4">Welcome to ShopSmart!</h2><p>Explore our amazing products below.</p></>
  );
};

export default Home;
