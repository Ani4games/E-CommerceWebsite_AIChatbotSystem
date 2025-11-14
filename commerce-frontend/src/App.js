import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import ProductPage from './pages/ProductPage';
import Cart from './pages/Cart';
import Chatbot from './Components/Chatbot/Chatbot';
// src/App.js

const Home = () => {
  return (
    <div style={{ padding: 20 }}>
      <h2>Welcome to ShopSmart</h2>
      <p>This is your Home page. Context not used yet.</p>
    </div>
  );
};

const Products = () => {
  return (
    <div style={{ padding: 20 }}>
      <h2>Products</h2>
      <p>List of products will appear here.</p>
    </div>
  );
};

const Cart = () => {
  return (
    <div style={{ padding: 20 }}>
      <h2>Cart</h2>
      <p>Your selected items will appear here.</p>
    </div>
  );
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/product/:id" element={<ProductPage />} />
        <Route path="/cart" element={<Cart />} />
      </Routes>
      <Chatbot />
    </Router>
  );
}


export default App;
