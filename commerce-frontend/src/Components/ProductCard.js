// Components/ProductCard.js
import React from "react";
import "./ProductCard.css";

const ProductCard = ({ product, addToCart }) => {
  return (
    <div className="product-card">
      <img src={product.image} alt={product.title || product.name} />

      <h3>{product.title || product.name}</h3>

      <p className="price">₹ {product.price}</p>

      {product.category && (
        <p className="category">{product.category}</p>
      )}

      {addToCart && (
        <button
          className="add-btn"
          onClick={() => addToCart(product)}
        >
          Add to Cart
        </button>
      )}
    </div>
  );
};

export default ProductCard;
