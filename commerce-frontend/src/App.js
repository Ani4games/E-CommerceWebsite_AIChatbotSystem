// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Chatbot from "./Components/Chatbot/Chatbot";
import Footer from "./Components/Footer";
import Navbar from "./Components/Navbar";
import Cart from "./pages/Cart";
import ProductPage from "./pages/ProductPage";
import { CartProvider } from "./context/CartContext";

const Home = () => {
  return (
    <div style={{ padding: 20 }}>
      <h2>Welcome to ShopSmart</h2>
      <p>This is your Home page. Context not used yet.</p>
    </div>
  );
};


const Products = () => {
  const products = [
    {
      id: 1,
      name: "Wireless Earbuds",
      price: 1999,
      image: "https://via.placeholder.com/200",
      description: "Crystal clear sound with long battery life.",
    },
    {
      id: 2,
      name: "Smart Watch",
      price: 2999,
      image: "https://via.placeholder.com/200",
      description: "Track your fitness goals and heart rate.",
    },
    {
      id: 3,
      name: "Bluetooth Speaker",
      price: 1499,
      image: "https://via.placeholder.com/200",
      description: "Portable and powerful with deep bass.",
    },
  ];

  return (
    <div style={{ padding: 20 }}>
      <h2>Products</h2>
      <div
        style={{
          display: "flex",
          gap: "20px",
          flexWrap: "wrap",
        }}
      >
        {products.map((p) => (
          <ProductCard key={p.id} product={p} />
        ))}
      </div>
    </div>
  );
};

function App() {
  return (
    <CartProvider>
      <Router>
        <div style={{ padding: 20 }}>
          <Navbar />
          <h1>ShopSmart 🛍️</h1>
          <nav style={{ marginBottom: 20 }}>
            <Link to="/" style={{ marginRight: 10 }}>Home</Link>
            <Link to="/products" style={{ marginRight: 10 }}>Products</Link>
            <Link to="/cart">Cart</Link>
          </nav>

          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/products" element={<Products />} />
            <Route path="/cart" element={<Cart />} />
          </Routes>

          <Chatbot />
          <Footer />
        </div>
      </Router>
  );
}

export default App;
