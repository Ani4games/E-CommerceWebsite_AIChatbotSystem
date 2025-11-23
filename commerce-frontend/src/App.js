// App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Chatbot from "./Components/Chatbot/Chatbot";
import Footer from "./Components/Footer";
import Navbar from "./Components/Navbar";
import Cart from "./pages/Cart";
import ProductPage from "./pages/ProductPage";
import Home from "./pages/Home";
import Login from "./pages/Login";

import { CartProvider } from "./context/CartContext";

import "./App.css";

function App() {
  return (
    <Router>
      <CartProvider>
        <Navbar />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/products" element={<ProductPage />} />   {/* FIXED */}
          <Route path="/cart" element={<Cart />} />
          <Route path="/login" element={<Login />} />
        </Routes>

        <Chatbot />
        <Footer />
      </CartProvider>
    </Router>
  );
}

export default App;
