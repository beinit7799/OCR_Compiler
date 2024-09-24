import React from "react";
import "./ErrorModal.css";

function errorModal({ modal, modalText }) {
  return <div>{modal && <div className="modal">{modalText}</div>}</div>;
}

export default errorModal;
