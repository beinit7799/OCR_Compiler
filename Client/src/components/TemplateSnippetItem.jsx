import React from "react";
import "../pages/Dashboard.css";

const TemplateSnippetItem = ({ thumbnail, handleItemClick }) => {
  return (
    <div>
      <div className="template-item" onClick={handleItemClick}>
        <div className="template-rect">
          <div className="template-rect-text">{thumbnail}</div>
        </div>
        <div className="template-info">
          <div className="template-info-title">{thumbnail} document</div>
        </div>
      </div>
    </div>
  );
};

export default TemplateSnippetItem;
