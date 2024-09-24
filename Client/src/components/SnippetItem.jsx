import React from "react";
import "../pages/Dashboard.css";
import { MdDeleteOutline } from "react-icons/md";

const SnippetItem = ({
  thumbnail,
  title,
  date,
  handleItemClick,
  handleSnippetDelete,
}) => {
  return (
    <div>
      <div className="template-item">
        <div className="template-rect" onClick={handleItemClick}>
          <div className="template-rect-text">{thumbnail}</div>
        </div>
        <div className="template-info">
          <div className="">
            <div className="template-info-title">Document no: {title}</div>
            <div className="template-info-date"> Created On : {date}</div>
          </div>
          <div className="delete-btn" onClick={handleSnippetDelete}>
            <MdDeleteOutline />
          </div>
        </div>
      </div>
    </div>
  );
};

export default SnippetItem;
