// CodeRenderer.jsx
import React, { useEffect, useRef, useState } from 'react';
import * as Babel from '@babel/standalone';
import '../styles/components/CodeRenderer.css';

const CodeRenderer = ({ htmlCode, cssCode, codeType }) => {
  const iframeRef = useRef(null);
  const [scale, setScale] = useState(1);

  useEffect(() => {
    const iframe = iframeRef.current;
    if (iframe) {
      const doc = iframe.contentDocument || iframe.contentWindow.document;
      doc.open();

      let content = htmlCode;
      if (codeType === 'jsx') {
        try {
          const transformedCode = Babel.transform(htmlCode, {
            presets: ['react'],
          }).code;
          content = `
            <div id="root"></div>
            <script src="https://unpkg.com/react@17/umd/react.development.js"></script>
            <script src="https://unpkg.com/react-dom@17/umd/react-dom.development.js"></script>
            <script>
              ${transformedCode}
              ReactDOM.render(React.createElement(App), document.getElementById('root'));
            </script>
          `;
        } catch (error) {
          console.error('Babel transformation error:', error);
          content = `<div>Error: ${error.message}</div>`;
        }
      }

      doc.write(`
        <!DOCTYPE html>
        <html>
          <head>
            <style>
              ${cssCode}
              body {
                margin: 0;
                padding: 0;
                width: 1920px;
                height: 1080px;
                transform-origin: top left;
                transform: scale(${scale});
              }
            </style>
            <script src="https://cdn.tailwindcss.com"></script>
          </head>
          <body>
            ${content}
          </body>
        </html>
      `);
      doc.close();

      // Make the iframe content interactive
      iframe.style.pointerEvents = 'auto';
    }
  }, [htmlCode, cssCode, codeType, scale]);

  const handleZoomIn = () => setScale(prev => Math.min(prev + 0.1, 2));
  const handleZoomOut = () => setScale(prev => Math.max(prev - 0.1, 0.5));

  return (
    <div className="code-renderer-container">
      <div className="zoom-controls">
        <button onClick={handleZoomOut}>-</button>
        <span>{Math.round(scale * 100)}%</span>
        <button onClick={handleZoomIn}>+</button>
      </div>
      <iframe
        ref={iframeRef}
        title="rendered-output"
        className="rendered-iframe"
        sandbox="allow-scripts allow-same-origin allow-forms"
      />
    </div>
  );
};

export default CodeRenderer;
