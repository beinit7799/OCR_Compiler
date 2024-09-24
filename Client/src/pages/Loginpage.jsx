import React, { useEffect, useState } from "react";
import "../pages/Loginpage.css";
import { useNavigate } from "react-router-dom";

const Loginpage = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  // Route if there are tokens set
  useEffect(() => {
    const token = localStorage.getItem('access');
    if (token) {
      navigate('/dashboard');
    }
  }, [navigate]);

  // Route to /register
  function handleClick() {
    navigate("/register");
  }

  // handle guest login
  function handleGuestLogin() {
    navigate("/dashboard");
  }

  // handle icon click
  const handleLogoClick = ()=>{
    navigate("/");
  }

  // Handle Login Button Click
  async function handleSubmit(event) {
    event.preventDefault();
    try {
      const formData = new FormData();
      formData.append("email", email);
      formData.append("password", password);

      const response = await fetch("http://localhost:8000/api/v1/login/", {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("access", data.tokens.access);
        localStorage.setItem("refresh", data.tokens.refresh);
        // Route to dashboard
        navigate("/dashboard");
      } else {
        // Handle error responses
        console.error("Login failed");
        const errorData = await response.json();
        setError(errorData.message || "Login failed");
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
          <div className="welcome-text">
            Hey, <br /> Welcome back !
          </div>
          <div className="welcome-subtext">Login to access your dashbaord</div>
          <form className="input-form" onSubmit={handleSubmit}>
            <input
              type="email"
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
            {/* Login Error Messages */}
            {error && <div className="error-message">{error}</div>}
            <div className="buttons">
              <button className="login-btn btn-primary">Log In</button>
              <button
                className="login-btn guest-btn btn-secondary"
                onClick={handleGuestLogin}
              >
                Login as a guest
              </button>
            </div>
          </form>

          <div className="register-text">
            Dont have an account?
            <span className="primary-color register-cta" onClick={handleClick}>
              Register
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Loginpage;
