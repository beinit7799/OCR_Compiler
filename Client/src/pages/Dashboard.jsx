import React, { useEffect, useState } from "react";
import "../App.css";
import "./Dashboard.css";
import axios from "axios";
import SnippetItem from "../components/SnippetItem";
import { useNavigate } from "react-router-dom";
import templateSnippetsData from "../data/templateSnippetsData.json";
import TemplateSnippetItem from "../components/TemplateSnippetItem";

const Dashboard = () => {
  const [documents, setDocuments] = useState([]);
  const [templateDocuments, setTemplateDocuments] = useState([]);
  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate("/home");
  };

  // Handle logo click
  const handleLogoClick = () => {
    {
      localStorage.getItem("access") !== null
        ? navigate("/")
        : navigate("/login");
    }
  };

  // Handle snippet item click
  const handleItemClick = (formattedCode, language) => {
    navigate("/home", { state: { code: formattedCode, language: language } });
  };

  // Delete the Snippet
  const handleSnippetDelete = async (id) => {
    // Authenticaton token
    const token = localStorage.getItem("access");

    const url = `http://localhost:8000/api/v1/code_snippet/${id}/delete/`;
    try {
      const response = await fetch(url, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`, // Include the JWT token in the Authorization header
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        console.log(`Item ${id} deleted successfully.`);
        setDocuments(documents.filter((document) => document.id !== id));
      } else {
        console.error(`Failed to delete item ${id}.`);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  // handle logout logic
  const handleLogout = async () => {
    const refreshToken = localStorage.getItem("refresh");

    if (refreshToken) {
      try {
        await axios.post("http://localhost:8000/api/v1/logout/", {
          refresh_token: refreshToken,
        });
      } catch (error) {
        console.error("Logout failed", error);
      }
    }

    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");

    navigate("/");
  };

  useEffect(() => {
    setTemplateDocuments(templateSnippetsData.snippets);
  });

  useEffect(() => {
    const token = localStorage.getItem("access"); // Retrieve JWT token from localStorage
    // console.log(token); // Check the token value
    if (token)
      fetch("http://localhost:8000/api/v1/profile/", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`, // Include the JWT token in the Authorization header
          "Content-Type": "application/json",
        },
      })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw new Error("Network response was not ok.");
      })
      .then((data) => {
        // console.log(data); // Check the response structure
        setDocuments(data.snippets);
        // setDocuments(data || []); // Adjust according to the actual structure
        // console.log(documents); // Check the updated state value
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  // Logging outside useEffect to observe state updates
  useEffect(() => {
  }, [documents]);

  return (
    <div className="App">
      {/* Navbar */}
      <div className="navbar">
        <div className="logo" onClick={handleLogoClick}>
          <span className="primary-color">OCR</span>compiler
        </div>
        <div className="save-btn btn-primary" onClick={handleButtonClick}>
          Create a new Document
        </div>
        {localStorage.getItem("access") !== null && (
          <div className="btn-secondary logout-btn" onClick={handleLogout}>
            Log out
          </div>
        )}
      </div>

      {/* Start with a Template */}
      <div className="template-wrapper">
        <div className="template-header">Start with a template</div>
        <div className="template-items">
          {templateDocuments.map((item) => (
            <TemplateSnippetItem
              key={item.id}
              thumbnail={item.language}
              handleItemClick={() =>
                handleItemClick(
                  item.formatted_code,
                  item.language
                )
              } // Pass formatted_code on item click
            />
          ))}
        </div>
      </div>

      <hr className="hr-line" />

      {/* Recent DOcuments */}
      <div className="recent-docs-wrapper">
        <div className="template-header">Recent documents</div>
        <div className="template-items">
          {documents.map((item) => (
            <SnippetItem
              key={item.id}
              thumbnail={item.language}
              title={item.id}
              date={item.created_at}
              handleItemClick={() => handleItemClick(item.formatted_code)} // Pass formatted_code on item click
              handleSnippetDelete={() => handleSnippetDelete(item.id)} //Delete the file
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
