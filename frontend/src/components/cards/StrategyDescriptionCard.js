import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const StrategyDescriptionCard = ({description}) => {

  return (
    <div className="card">
      <div className="card-body">
        {/* <p>{description.description}</p> */}
        <SyntaxHighlighter language="python" style={vscDarkPlus}>
          {description}
        </SyntaxHighlighter>
      </div>
    </div>
  );
};

export default StrategyDescriptionCard;
