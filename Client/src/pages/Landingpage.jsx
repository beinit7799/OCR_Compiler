import React from "react";
import "../App.css";
import "./Landingpage.css";
import { useNavigate } from "react-router-dom";
import homepagess from "../images/homepagess.png";
import wigglevector from "../images/wigglevector.svg";
import { TbScan } from "react-icons/tb";
import { TbCapture } from "react-icons/tb";
import { FaCode } from "react-icons/fa6";
import { FaArrowRight } from "react-icons/fa6";

const Landingpage = () => {
  const navigate = useNavigate();

  function handleClick() {
    navigate("/login");
  }
  return (
    <>
      <div className="navbar landing-navbar">
        <div className="logo">
          <span className="primary-color">OCR</span>compiler
        </div>
        {/* onClick={downloadTxtFile} */}
        {/* <a href="/login"> */}
        <div className="save-btn btn-primary" onClick={handleClick} ddd>
          {localStorage.getItem("access") !== null
            ? "Go to your dashboard"
            : "Login"}
        </div>
        {/* </a> */}
      </div>
      <div className="container">
        <div className="hero-section">
          Scan and compile <br />{" "}
          <span className="wiggle-wrapper">
            code snippets
            <img src={wigglevector} className="wiggle-svg" width={450}></img>
          </span>{" "}
          in an instant.
        </div>
        <div className="landing-img">
          <img src={homepagess} alt="landing_img" width={1000}></img>
        </div>
        <div className="features-wrapper">
          <div className="feature">
            <div className="feature-icon">
              <TbCapture />
            </div>
            <div className="feature-description">
              Capture a code <br />
              snippet.
            </div>
          </div>
          <div className="right-arrow-icon">
            <FaArrowRight />
          </div>
          <div className="feature">
            <div className="feature-icon">
              <TbScan />
            </div>
            <div className="feature-description">
              Extract the code <br />
              into digital format.
            </div>
          </div>
          <div className="right-arrow-icon">
            <FaArrowRight />
          </div>
          <div className="feature">
            <div className="feature-icon">
              <FaCode />
            </div>
            <div className="feature-description">
              Compile the <br />
              code.
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Landingpage;
