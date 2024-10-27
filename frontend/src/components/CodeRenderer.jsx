// CodeRenderer.jsx
import React, { useEffect, useRef, useState, forwardRef, useImperativeHandle } from 'react';
import * as Babel from '@babel/standalone';
import html2canvas from 'html2canvas';
import '../styles/components/CodeRenderer.css';

const CodeRenderer = forwardRef(({ htmlCode, cssCode, codeType, cssType }, ref) => {
  const iframeRef = useRef(null);
  const [scale, setScale] = useState(1);

  useImperativeHandle(ref, () => ({
    captureImage: async () => {
      const iframe = iframeRef.current;
      if (iframe) {
        const iframeContent = iframe.contentDocument.body;
        try {
          const canvas = await html2canvas(iframeContent, {
            scale: 1,
            useCORS: true,
            allowTaint: true,
          });
          return canvas.toDataURL('image/png');
        } catch (error) {
          console.error('Error capturing image:', error);
          throw error;
        }
      }
    }
  }));

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
                width: 1280px;
                height: 720px;
                transform-origin: top left;
                transform: scale(${scale});
              }
              ::-webkit-scrollbar {
                width: 10px !important;
              }
              ::-webkit-scrollbar-track {
                background: transparent;
              }
              ::-webkit-scrollbar-thumb {
                background-color: hsl(243, 49%, 54%, 80%);
                border-radius: 5px;
              }
              * {
                scrollbar-width: thin !important;
                scrollbar-color: hsl(243, 49%, 54%, 80%) transparent;
              }
            </style>
            ${cssType === 'tailwind' ? '<script src="https://cdn.tailwindcss.com"></script>' : ''}
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
    
    <div className="render">

      <div className="render_header">
          <h4 style={{margin: 0, fontSize: '1.2rem'}}>Render</h4>
          
          <div className="zoom-controls">
            <button onClick={handleZoomOut}>-</button>
            <span>{Math.round(scale * 100)}%</span>
            <button onClick={handleZoomIn}>+</button>
          </div>
      </div>
      
      <iframe
        ref={iframeRef}
        title="rendered-output"
        className="rendered-iframe"
        sandbox="allow-scripts allow-same-origin allow-forms"
      />
    </div>
  );
});

export default CodeRenderer;
