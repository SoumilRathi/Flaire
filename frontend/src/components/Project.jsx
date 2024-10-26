import React, { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import CodeRenderer from './CodeRenderer'
import ChatComponent from './ChatComponent'
import AceEditor from 'react-ace'
import 'ace-builds/src-noconflict/mode-jsx'
import 'ace-builds/src-noconflict/mode-html'
import 'ace-builds/src-noconflict/mode-css'
import 'ace-builds/src-noconflict/theme-monokai'
import '../styles/components/Project.css'
import { HiSparkles } from 'react-icons/hi'
import { addDoc, collection, doc, onSnapshot, updateDoc } from 'firebase/firestore'
import { db } from '../firebase'
import { addProject, globalProjects } from '../Router'

const Project = ({ newProject, setNewProject, socket }) => {
    const { id } = useParams()
    const navigate = useNavigate()
    const [projectID, setProjectID] = useState(id)

    console.log("Project ID", id)

    const [activeTab, setActiveTab] = useState('html')
    const [codeType, setCodeType] = useState('html')
    const [htmlCode, setHtmlCode] = useState('')
    const [cssCode, setCssCode] = useState('')
    const [instructions, setInstructions] = useState('')
    const [renderKey, setRenderKey] = useState(0)
    const [cssType, setCssType] = useState('external')
    const [editClasses, setEditClasses] = useState(false)
    const [isNewProject, setIsNewProject] = useState(true)
    const [messages, setMessages] = useState([])
    const codeRendererRef = useRef(null)

    useEffect(() => {
        if (socket) {
            socket.on('styled_code', (data) => {
                if (data.project_id === projectID) {
                    if (data.htmlCode) {
                        setHtmlCode(data.htmlCode)
                    }
                    setCssCode(data.code)
                    setActiveTab('css')
                    updateProjectInDB(projectID, { cssCode: data.code, updated: true })
                }
            })

            socket.on('agent_response', (data) => {
                if (data.project_id === projectID) {
                    setMessages((prevMessages) => [...prevMessages, { text: data.message, sender: 'agent' }])
                }
            })

            socket.on('screenshot', (data) => {
                console.log("Screenshot received", data)
                if (data.project_id === projectID && codeRendererRef.current) {
                    codeRendererRef.current.captureImage().then(imageDataUrl => {
                        socket.emit('screenshot_response', { screenshot: imageDataUrl, project_id: projectID });
                    }).catch(error => {
                        console.error('Error capturing screenshot:', error);
                        socket.emit('screenshot_response', { error: 'Failed to capture screenshot', project_id: projectID });
                    });
                } else {
                    console.error("Screenshot received for wrong project", data)
                    socket.emit('screenshot_unavailable', { error: 'Failed to capture screenshot', project_id: projectID });
                }
            })
        }

        return () => {
            if (socket) {
                socket.off('styled_code')
                socket.off('agent_response')
                socket.off('screenshot')
            }
        }
    }, [socket, projectID])

    useEffect(() => {
        if (id) {
            setIsNewProject(false)
            const unsubscribe = onSnapshot(doc(db, 'projects', id), (doc) => {
                if (doc.exists()) {
                    const data = doc.data()
                    setHtmlCode(data.htmlCode || '')
                    setCssCode(data.cssCode || '')
                    setInstructions(data.instructions || '')
                    setCssType(data.cssType || 'external')
                    setMessages(data.messages || [])
                    setEditClasses(data.editClasses || false)
                    if (data.updated) {
                        updateDoc(doc.ref, { updated: false })
                    }
                }
            })
            return () => unsubscribe()
        } else {
            setIsNewProject(true)
        }
    }, [id])

    useEffect(() => {
        if (newProject) {
            setHtmlCode('')
            setCssCode('')
            setInstructions('')
            setCssType('external')
            setMessages([])
            setEditClasses(false)
            setNewProject(false)
        }
    }, [newProject])

    useEffect(() => {
        setRenderKey(prevKey => prevKey + 1)
    }, [htmlCode, cssCode, codeType])

    const handleCodeChange = (newCode) => {
        setHtmlCode(newCode)

        if (!isNewProject) {
            console.log("Updating HTML code locally", projectID)
            updateProjectLocally(projectID, { htmlCode: newCode })
        }
    }

    const handleCssChange = (newCode) => {
        setCssCode(newCode)

        if (!isNewProject) {
            updateProjectLocally(projectID, { cssCode: newCode })
        }
    }

    const updateProjectLocally = async (id, data) => {
        globalProjects[id] = { ...globalProjects[id], ...data }
    }

    const handleCaptureImage = (imageDataUrl) => {
        setCapturedImage(imageDataUrl);
        // The image is now downloaded directly in the CodeRenderer component
        // You can still use this function if you need to do anything else with the captured image
    };

    // Comment out or remove the sendImageToBackend function
    /*
    const sendImageToBackend = (imageDataUrl) => {
        if (socket && socket.connected) {
            socket.emit('send_image', { 
                image: imageDataUrl,
                id: projectID,
            });
        } else {
            console.error("Socket is not connected");
        }
    };
    */

    const styleCode = async () => {
        let projectId = id

        console.log("Initiating style code process")

        if (isNewProject) {
            const projectRef = collection(db, 'projects')
            const newDoc = await addDoc(projectRef, {
                name: "Untitled Project",
                htmlCode,
                cssCode,
                cssType,
                editClasses,
                updated: false
            })
            setProjectID(newDoc.id)
            projectId = newDoc.id
            navigate(`/project/${newDoc.id}`)
        } else {
            console.log("Updating project in DB", projectID)
            const projectRef = doc(db, 'projects', projectID)
            await updateDoc(projectRef, { 
                htmlCode, 
                cssCode,
                cssType, 
                editClasses 
            })
        }

        if (socket && socket.connected) {
            socket.emit('style_code', { 
                htmlCode, 
                cssCode, 
                cssType, 
                editClasses,
                id: projectId,
                messages,
            });
            console.log("Style code data emitted successfully");
        } else {
            console.error("Socket is not connected");
        }
    }

    // handling the chat section
    const sendMessage = (message) => {
        setMessages((prevMessages) => [...prevMessages, message])
    }

    useEffect(() => {
        if (messages.length > 0) {
            styleCode();
        }
    }, [messages])

    return (
        <div className="project">
            <div className="instructions">
                <div className='instruction edit_classes'>
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

                <div className='instruction css_type_selector'>
                    <label style={{marginRight: ".5rem"}}>CSS Type: </label>
                    <select value={cssType} onChange={(e) => setCssType(e.target.value)} className='css_type_selector_select'>
                        <option value="css">CSS</option>
                        <option value="scss">SCSS</option>
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
                        ref={codeRendererRef}
                        key={renderKey} 
                        htmlCode={htmlCode} 
                        cssCode={cssCode} 
                        codeType={codeType} 
                    />
                    <ChatComponent messages={messages} setMessages={setMessages} sendMessage={sendMessage} />
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
                            setOptions={{
                                useWorker: false,
                                highlightActiveLine: false,
                                showGutter: true,
                                gutterStyle: { backgroundColor: 'var(--primary50)' }
                            }}
                            style={{ backgroundColor: 'transparent' }}
                            theme="github"
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
                            setOptions={{
                                useWorker: false,
                                highlightActiveLine: false,
                                showGutter: true,
                                gutterStyle: { backgroundColor: 'var(--primary50)' }
                            }}
                            style={{ backgroundColor: 'transparent' }}
                            theme="github"
                        />
                    )}
                </div>
            </div>
        </div>
    )
}

export default Project
