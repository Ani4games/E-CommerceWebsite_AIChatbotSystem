// pages/ProductPage.js
import React, { useState } from "react";
import ProductCard from "./ProductPage";
import "./ProductPage.css";

const productsData = [
  { id: 1, name: "Wireless Headphones", price: 1499, category: "Electronics", image: "/images/headphone.png" },
  { id: 2, name: "Smart Watch", price: 1999, category: "Electronics", image: "/images/watch.png" },
  { id: 3, name: "Running Shoes", price: 899, category: "Sports", image: "/images/shoes.png" },
  { id: 4, name: "Backpack", price: 599, category: "Fashion", image: "/images/bag.png" },
  { id: 5, name: "Men's Jacket", price: 1299, category: "Fashion", image: "/images/jacket.png" },
];

function ProductPage() {
  const [categoryFilter, setCategoryFilter] = useState("All");
  const [priceFilter, setPriceFilter] = useState(2000);

  const filtered = productsData.filter(item => {
    const categoryMatch = categoryFilter === "All" || item.category === categoryFilter;

    const priceMatch = item.price <= priceFilter;

    return categoryMatch && priceMatch;
  });

  return (
    <div className="product-page-container">
      {/* ---------------- Filters ---------------- */}
      <aside className="filters">
        <h3>Filters</h3>

        <label>Category</label>
        <select
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
        >
          <option>All</option>
          <option>Electronics</option>
          <option>Fashion</option>
          <option>Sports</option>
        </select>

        <label>Max Price: ₹{priceFilter}</label>
        <input
          type="range"
          min="100"
          max="3000"
          value={priceFilter}
          onChange={(e) => setPriceFilter(Number(e.target.value))} />
      </aside>

      {/* ---------------- Product Grid ---------------- */}
      <section className="product-grid">
        {filtered.map((p) => (
          <ProductCard key={p.id} product={p} />
        ))}

        {filtered.length === 0 && (
          <p className="no-results">No products match your filters.</p>
        )}
      </section>
    </div>
  );
}

export default ProductPage;
