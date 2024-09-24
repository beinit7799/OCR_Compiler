import React, { useEffect, useState } from "react";
import "./Loginpage.css";
import { useNavigate } from "react-router-dom";

const Registerpage = () => {
  const [name, setName] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const navigate = useNavigate();

  // Route if there are tokens set
  useEffect(() => {
    const token = localStorage.getItem("access");
    if (token) {
      navigate("/dashboard");
    }
  }, [navigate]);

  function handleClick() {
    navigate("/login");
  }

  // handle icon click
  const handleLogoClick = () => {
    navigate("/");
  };

  // handle form submit
  async function handleSubmit(event) {
    event.preventDefault();
    try {
      const formData = new FormData();
      formData.append("email", email);
      formData.append("password", password);
      formData.append("name", name);
      formData.append("username", username);

      const response = await fetch("http://localhost:8000/api/v1/signup/", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data);
        localStorage.setItem("accessToken", data.tokens.access);
        localStorage.setItem("refreshToken", data.tokens.refresh);
        // Route to dashboard
        navigate("/login");
      } else {
        // Handle error responses
        console.error("Register failed");
        const errorData = await response.json();
        setError(errorData.message || "Register failed");
      }
    } catch (error) {
      console.error("Error:", error);
      setError("An error occurred. Please try again.");
    }
  }
  return (
    <div className="login-container">
      <div className="left-panel"></div>
      <div className="right-panel">
        <div className="right-panel-wrapper">
          <div className="logo login-logo" onClick={handleLogoClick}>
            <span className="primary-color">OCR</span>compiler
          </div>
          <div className="welcome-text">Create a new account !</div>
          <div className="welcome-subtext">
            To start compiling your code snippets
          </div>
          <form className="input-form" onSubmit={handleSubmit}>
            <input
              type="text"
              id="Name"
              placeholder="Enter name"
              className="input-field"
              onChange={(e) => {
                setName(e.target.value);
              }}
            ></input>
            <input
              type="text"
              id="username"
              placeholder="Enter username"
              className="input-field"
              onChange={(e) => {
                setUsername(e.target.value);
              }}
            ></input>
            <input
              type="text"
              id="email"
              placeholder="Enter email"
              className="input-field"
              onChange={(e) => {
                setEmail(e.target.value);
              }}
            ></input>
            <input
              type="password"
              id="password"
              placeholder="Enter password"
              className="input-field"
              onChange={(e) => {
                setPassword(e.target.value);
              }}
            ></input>
            {/* Register Error Messages */}
            {error && <div className="error-message">{error}</div>}
            <button className="login-btn btn-primary">Sign In</button>
          </form>
          <div className="register-text">
            Already have an account?
            <span className="primary-color register-cta" onClick={handleClick}>
              Login
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Registerpage;
