import React from "react";
import { MdOutlineOutput } from "react-icons/md";

function OutputSection({ output, ref, input ,handleInputChange}) {
  return (
    <div className="output-section" ref={ref}>
      <div className="section-title">
        <div className="section-title-text">
          <MdOutlineOutput className="section-title-icon" />
          OUTPUT
        </div>
      </div>
      {/* <textarea rows={20} cols={100} value={output}></textarea> */}
      <div className="output-code">{output}</div>
      <input type="text" className="input-section" value={input} onChange={(e)=>{handleInputChange(e)}}/>
    </div>
  );
}

export default OutputSection;
