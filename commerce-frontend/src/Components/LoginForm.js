// Components/LoginForm.js
import React, { useState } from "react";
import "./Login.css";
import api from "../axiosconfig";   // Correct import

const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await api.post("/auth/login", { email, password });

      alert("Login Successful!");
      localStorage.setItem("token", res.data.access_token);
    } catch (err) {
      alert("Invalid credentials");
    }
  };

  return (
    <div className="login-wrapper">
      <form className="login-card" onSubmit={handleSubmit}>
        <h2>Login</h2>

        <div className="form-row">
          <label>Email</label>
          <input
            type="email"
            placeholder="Enter email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="form-row">
          <label>Password</label>
          <input
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <div className="login-actions">
          <button type="submit" className="login-btn">Login</button>
        </div>
      </form>
    </div>
  );
};

export default LoginForm;
