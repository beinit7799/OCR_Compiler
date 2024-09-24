import { useState, useRef, useEffect } from "react";
import "../App.css";
import ImageSection from "../section/ImageSection.jsx";
import OcrSection from "../section/OcrSection";
import OutputSection from "../section/OutputSection";
import ErrorModal from "../section/ErrorModal";
import axios from "axios";
import Tesseract from "tesseract.js";
import { HiDownload } from "react-icons/hi";
import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [data, setData] = useState({});
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");
  const [input, setInput] = useState("");
  const ref = useRef(null);
  const [modal, setModal] = useState(false);
  const [modalText, setModalText] = useState("");
  const [windowSize, setWindowSize] = useState();
  const [progressBar, setProgressBar] = useState(0);
  const [extension, setExtension] = useState("code.txt");
  const [language, setLanguage] = useState("");
  const navigate = useNavigate();

  //handle logo click
  const handleLogoClick = () => {
    navigate("/dashboard");
  };

  // Get code from SnippetItem
  const location = useLocation();
  useEffect(() => {
    if (location.state && location.state.code) {
      setCode(location.state.code);
    }
    if (location.state && location.state.language) {
      setLanguage(location.state.language);
    }
  }, [location.state]);

  //Downloads the code as a txt file
  const downloadTxtFile = () => {
    if (code) {
      const element = document.createElement("a");
      const file = new Blob([code], { type: "text/plain" });
      element.href = URL.createObjectURL(file);
      // element.download = "code.txt";
      element.download = `code.${extension}`;
      document.body.appendChild(element);
      element.click();
    } else {
      setModal(true);
      setModalText("There's no code to download.");
      setTimeout(() => {
        setModal(false);
        setModalText("");
      }, 2000);
    }
  };

  //Updates the extension variable
  const updateExtension = (e) => {
    setExtension(e);
  };

  //For updating windowSize on resize
  window.addEventListener("resize", () => {
    setWindowSize(window.innerWidth);
  });

  //Sets the input image on the state variable
  const onimgchangeHandler = (e) => {
    setSelectedImage(e.target.files[0]);
  };

  //Handles Image Upload
  const handleImageUpload = async () => {
    if (!selectedImage) return;

    // Perform OCR on the image using Tesseract
    const textData = await Tesseract.recognize(selectedImage, "eng", {
      logger: (m) => {
        setProgressBar(m.progress);
      },
    });

    // Check if the OCR output contains a substantial amount of text
    const minTextLength = 5;

    if (textData.data.text.length >= minTextLength) {
      const formData = new FormData();
      formData.append("image", selectedImage);

      try {
        const accessToken = localStorage.getItem("access"); // Retrieve JWT token from localStorage
        const headers = {
          "Content-Type": "multipart/form-data",
        };
        if (accessToken) {
          headers.Authorization = `Bearer ${accessToken}`;
        }
        const response = await axios.post(
          "http://localhost:8000/api/v1/upload/",
          formData,
          { headers }
        );
        console.log(response);
        console.log(response.data.snippet);
        setData(response.data.snippet.formatted_code);
        setCode(response.data.snippet.formatted_code);
        if (response.data.snippet.language) {
          setLanguage(response.data.snippet.language);
          console.log("Language", response.data.snippet.language);
        } else {
          setLanguage("");
        }
        
      } catch (error) {
        console.error("Error uploading image:", error);
      }
    } else {
      setModal(true);
      setModalText("Insert a valid document");
      setTimeout(() => {
        setModal(false);
        setModalText("");
      }, 2000);
    }
  };

  //handles image reupload
  const handleReupload = () => {
    setSelectedImage(null);
    setCode("");
    setOutput("");
  };

  //Sets Code as the editor updates
  const oninputChangeHandler = (e) => {
    setCode(e);
  };

  //Handles compile btn click
  const handleRunClick = async () => {
    let lowercaseLanguage;
    switch (language) {
      case "C":
        lowercaseLanguage = "c";
        break;
      case "c":
        lowercaseLanguage = "c";
        break;
      case "Js":
        lowercaseLanguage = "javascript";
        break;
      case "JS":
        lowercaseLanguage = "javascript";
        break;
      case "JAVASCRIPT":
        lowercaseLanguage = "javascript";
        break;
      case "js":
        lowercaseLanguage = "javascript";
        break;
      case "Python":
        lowercaseLanguage = "python";
        break;
      case "py":
        lowercaseLanguage = "python";
        break;
      case "Py":
        lowercaseLanguage = "python";
        break;
      case "C++":
        lowercaseLanguage = "cpp";
        break;
      case "Cpp":
        lowercaseLanguage = "cpp";
        break;
      case "java":
        lowercaseLanguage = "java";
        break;
      case "Java":
        lowercaseLanguage = "java";
      case "unknown":
        lowercaseLanguage = "c";
        break;
      default:
        language.toLowerCase();
    }

    if (!code) {
      setModal(true);
      setModalText("There's no code to compile.");
      setTimeout(() => {
        setModal(false);
        setModalText("");
      }, 2000);
    } else {
      console.log(code);
      const payload = {
        code,
        input,
        language: lowercaseLanguage,
      };
      const outputData = await axios.post(
        "http://localhost:8000/api/v1/compile/",
        payload
      );
      console.log("OUTPUTDATA:", outputData.data);
      if (outputData.data.error) {
        setOutput(outputData.data.error);
      } else {
        setOutput(outputData.data.output);
      }
      // ref.current?.scrollIntoView({ behavior: "smooth" });
    }
  };

  //Handles Input Change
  const handleInputChange = (e) => {
    // setInput("");
    setInput(e.target.value);
  };

  return (
    <div>
      <div className="App">
        <ErrorModal modal={modal} modalText={modalText} />
        {/* <div className="input-section">
        <input type="file" accept="image/*" onChange={onchangeHandler}></input>
      </div> */}

        {/* <div className="image-view">
        {selectedImage && (
          <img src={URL.createObjectURL(selectedImage)} id="inputImg"></img>
        )}
      </div> */}

        {/* {data.ocr} */}
        <div className="navbar">
          <div className="logo">
            <div className="" onClick={handleLogoClick}>
              <span className="primary-color">OCR</span>compiler
            </div>
          </div>
          <div className="save-btn btn-primary" onClick={downloadTxtFile}>
            {windowSize <= 580 ? (
              <div>
                <HiDownload className="download-icon" />
              </div>
            ) : (
              "Download Code"
            )}
          </div>
          {/* <div className="user-img">.</div> */}
        </div>
        <div className="sections">
          <ImageSection
            onchangeHandler={onimgchangeHandler}
            selectedImage={selectedImage}
            handleImageUpload={handleImageUpload} // Pass the image upload handler
            progressBar={progressBar}
            handleReupload={handleReupload}
          />
          <OcrSection
            code={code}
            onchangeHandler={oninputChangeHandler}
            handleRunClick={handleRunClick}
            updateExtension={updateExtension}
            language={language}
          />
          <OutputSection
            output={output}
            ref={ref}
            input={input}
            handleInputChange={handleInputChange}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
