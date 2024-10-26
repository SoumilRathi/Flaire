import React, { useState, useEffect } from 'react'
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
import { addDoc, collection, doc, onSnapshot, updateDoc } from 'firebase/firestore'
import { db } from '../firebase'

const SOCKET_SERVER_URL = 'http://localhost:7777'

const Project = ({ newProject, setNewProject }) => {
    const { id } = useParams()
    const navigate = useNavigate()
    const [projectID, setProjectID] = useState(id)
    const [activeTab, setActiveTab] = useState('html')
    const [codeType, setCodeType] = useState('html')
    const [htmlCode, setHtmlCode] = useState('')
    const [cssCode, setCssCode] = useState('')
    const [instructions, setInstructions] = useState('')
    const [renderKey, setRenderKey] = useState(0)
    const [cssType, setCssType] = useState('external')
    const [editClasses, setEditClasses] = useState(false)
    const [isNewProject, setIsNewProject] = useState(true)
    const [socket, setSocket] = useState(null)

    useEffect(() => {
        const newSocket = io(SOCKET_SERVER_URL)
        setSocket(newSocket)

        newSocket.on('styled_code', (data) => {
            console.log("Received styled code:", data)
            if (data.code && data.id === projectID) {
                setCssCode(data.code)
                setActiveTab('css')
                updateProjectInDB(projectID, { cssCode: data.code, updated: true })
            }
        })

        return () => newSocket.close()
    }, [projectID])

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
            updateProjectInDB(projectID, { htmlCode: newCode, updated: true })
        }
    }

    const handleCssChange = (newCode) => {
        setCssCode(newCode)
        if (!isNewProject) {
            updateProjectInDB(projectID, { cssCode: newCode, updated: true })
        }
    }

    const updateProjectInDB = async (id, data) => {
        const projectRef = doc(db, 'projects', id)
        await updateDoc(projectRef, data)
    }

    const styleCode = async () => {
        let projectId = id

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
        }

        if (socket) {
            socket.emit('style_code', { 
                htmlCode, 
                cssCode, 
                cssType, 
                editClasses,
                id: projectId
            })
        }
    }

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
                    <CodeRenderer key={renderKey} htmlCode={htmlCode} cssCode={cssCode} codeType={codeType} />
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
