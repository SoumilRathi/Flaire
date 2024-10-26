import React, { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import io from 'socket.io-client'
import CodeRenderer from './CodeRenderer'
import ChatComponent from './ChatComponent'
import AceEditor from 'react-ace'
import 'ace-builds/src-noconflict/mode-jsx'
import 'ace-builds/src-noconflict/mode-html'
import 'ace-builds/src-noconflict/mode-css'
import 'ace-builds/src-noconflict/theme-monokai'
import '../styles/components/Project.css'
import { HiSparkles } from 'react-icons/hi'
import { getProject, saveProject } from '../utils/projectStorage'

const SOCKET_SERVER_URL = 'http://localhost:7777'

const Project = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('html')
  const [codeType, setCodeType] = useState('html')
  const [htmlCode, setHtmlCode] = useState('')
  const [cssCode, setCssCode] = useState('')
  const [instructions, setInstructions] = useState('')
  const [renderKey, setRenderKey] = useState(0)
  const [cssType, setCssType] = useState('external')
  const [editClasses, setEditClasses] = useState(false)
  const [socket, setSocket] = useState(null)

  useEffect(() => {
    const newSocket = io(SOCKET_SERVER_URL)
    setSocket(newSocket)

    newSocket.on('styled_code', (data) => {
      console.log("Received styled code:", data)
      if (data.code) {
        setCssCode(data.code)
        setActiveTab('css')
        saveProject(id, { ...getProject(id), cssCode: data.code })
      }
    })

    return () => newSocket.close()
  }, [id])

  useEffect(() => {
    const projectData = getProject(id)
    if (projectData) {
      setHtmlCode(projectData.htmlCode || '')
      setCssCode(projectData.cssCode || '')
      setInstructions(projectData.instructions || '')
      setCssType(projectData.cssType || 'external')
      setEditClasses(projectData.editClasses || false)
    } else {
      // Handle case when project doesn't exist
      navigate('/new')
    }
  }, [id, navigate])

  useEffect(() => {
    setRenderKey(prevKey => prevKey + 1)
  }, [htmlCode, cssCode, codeType])

  useEffect(() => {
    const handleMessage = (event) => {
      if (event.data.type === 'INTERACTION') {
        console.log('Interaction in CodeRenderer:', event.data);
        // Handle the interaction here, e.g., update state or trigger actions
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  const handleCodeChange = (newCode) => {
    setHtmlCode(newCode)
    saveProject(id, { ...getProject(id), htmlCode: newCode })
  }

  const handleCssChange = (newCode) => {
    setCssCode(newCode)
    saveProject(id, { ...getProject(id), cssCode: newCode })
  }

  const styleCode = () => {
    if (socket) {
      socket.emit('style_code', { 
        htmlCode, 
        cssCode, 
        cssType, 
        editClasses 
      })
    }
  }

  return (
    <div className="project">
      <div className="instructions">
        <div className='edit_classes'>
          <div
            className="checkbox"
            style={{
              border: "1px solid var(--primary)",
              width: ".7rem",
              height: ".7rem",
              borderRadius: "20%",
              backgroundColor: editClasses ? "var(--primary)" : "transparent",
              cursor: "pointer",
              marginRight:"0.5rem"
            }}
            onClick={(event) => {
              event.stopPropagation();
              setEditClasses(!editClasses);
            }}
          />
          <label>Edit Classes</label>
        </div>

        <div className='css_type_selector'>
          <label>CSS Type: </label>
          <select value={cssType} onChange={(e) => setCssType(e.target.value)}>
            <option value="external">External</option>
            <option value="inline">In-Line</option>
            <option value="internal">Internal</option>
            <option value="tailwind">Tailwind</option>
          </select>
        </div>

        <button className='style_button' onClick={styleCode}>
          <HiSparkles style={{marginRight: ".5rem"}} />
          Style
        </button>
      </div>

      <div className='body'>
        <div className='section left'>
            <CodeRenderer 
              key={renderKey} 
              htmlCode={htmlCode} 
              cssCode={cssCode} 
              codeType={codeType} 
            />
            <ChatComponent socket={socket} />
        </div>

        <div className='section right'>
          <div className="code-header">
            <div className="tab-switcher">
              <button 
                className={`tab ${activeTab === 'html' ? 'active' : ''}`}
                onClick={() => setActiveTab('html')}
              >
                HTML
              </button>
              <button 
                className={`tab ${activeTab === 'css' ? 'active' : ''}`}
                onClick={() => setActiveTab('css')}
              >
                CSS
              </button>
            </div>
          </div>
          
          {activeTab === 'html' ? (
            <AceEditor
              mode="html"
              onChange={handleCodeChange}
              value={htmlCode}
              name="html-editor"
              editorProps={{ $blockScrolling: true }}
              width="100%"
              height="92.5%"
            />
          ) : (
            <AceEditor
              mode="css"
              onChange={handleCssChange}
              value={cssCode}
              name="css-editor"
              editorProps={{ $blockScrolling: true }}
              width="100%"
              height="92.5%"
            />
          )}
        </div>
      </div>
    </div>
  )
}

export default Project
