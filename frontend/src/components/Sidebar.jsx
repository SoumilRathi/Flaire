import React, { useState, useEffect } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import '../styles/components/Sidebar.css'
import { FaPlus, FaPencilAlt, FaTrash } from 'react-icons/fa'
import { db } from '../firebase'
import { doc, updateDoc, deleteDoc, onSnapshot, collection } from 'firebase/firestore'

const Sidebar = ({ onNewProject }) => {
    const [projects, setProjects] = useState([])
    const [editingId, setEditingId] = useState(null)
    const navigate = useNavigate()
    const location = useLocation()

    useEffect(() => {
        const unsubscribe = onSnapshot(collection(db, 'projects'), (snapshot) => {
            const updatedProjects = snapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data(),
                updated: doc.data().updated || false
            }))
            setProjects(updatedProjects)
        })

        return () => unsubscribe()
    }, [])

    const handleCreateNewProject = () => {
        navigate('/')
        onNewProject()
    }

    const handleRename = async (id, newName) => {
        const projectRef = doc(db, 'projects', id)
        await updateDoc(projectRef, { name: newName })
        setEditingId(null)
    }

    const handleDelete = async (id) => {
        const projectRef = doc(db, 'projects', id)
        await deleteDoc(projectRef)
        if (location.pathname === `/project/${id}`) {
            navigate('/')
        }
    }

    return (
        <div className="sidebar">
            <div className='sidebar_header'>
                <h2 className="sidebar-title">Styler</h2>
                <FaPlus onClick={handleCreateNewProject} className="new-project-icon" />
            </div>
            
            <div className='projects-container'>
                <div className='projects'>
                    {projects.map((project) => (
                        <div key={project.id} className={`project-item ${location.pathname === `/project/${project.id}` ? 'active' : ''}`}>
                            <div className='project_updated_icon'>
                                {project.updated && <div className="glowing-indicator"></div>}
                            </div>
                            {editingId === project.id ? (
                                <input
                                    type="text"
                                    defaultValue={project.name}
                                    onBlur={(e) => handleRename(project.id, e.target.value)}
                                    onKeyPress={(e) => {
                                        if (e.key === 'Enter') {
                                            handleRename(project.id, e.target.value)
                                        }
                                    }}
                                    autoFocus
                                />
                            ) : (
                                <Link to={`/project/${project.id}`} className="project-link">
                                    <span className="project-name">{project.name}</span>
                                </Link>
                            )}
                            <div className="project-actions">
                                <FaPencilAlt 
                                    className="project-action-icon" 
                                    onClick={() => setEditingId(project.id)}
                                />
                                <FaTrash 
                                    className="project-action-icon" 
                                    onClick={() => handleDelete(project.id)}
                                />
                            </div>
                        </div>
                    ))}
                    {projects.length === 0 && (
                        <div className="no_projects">No projects yet!</div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default Sidebar
