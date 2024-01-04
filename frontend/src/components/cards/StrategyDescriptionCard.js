import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const StrategyDescriptionCard = ({description}) => {

  return (
    <div className="card">
      <div className="card-body">
        {/* <h5 className="card-title">Coefficient of Variance</h5> */}
        {/* <p className="card-text">The coefficient of variance ranks stocks by their standard deviation to price. See code snippet below:</p> */}
        <SyntaxHighlighter language="python" style={vscDarkPlus}>
          {description}
        </SyntaxHighlighter>
      </div>
    </div>
  );
};

export default StrategyDescriptionCard;
