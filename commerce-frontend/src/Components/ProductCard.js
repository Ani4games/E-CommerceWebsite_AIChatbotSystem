import React, { useContext } from "react";
import { CartContext } from "../context/CartContext";
import "./ProductCard.css";

const ProductCard = ({ product }) => {
  const { addToCart } = useContext(CartContext);

  return (
      <div className="product-card">
      <div className="img-wrap">
        <img src={product.image} alt={product.name} />
      </div>
      <h3>{product.name}</h3>
      <p className="price">₹{product.price}</p>
      <div className="actions">
        <button className="btn" onClick={() => addToCart(product)}>Add</button>
        <button className="btn secondary">Details</button>
      </div>
    </div>

  );
};

export default ProductCard;
