import React, { useState, useEffect } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import '../styles/components/Sidebar.css'
import { FaPlus, FaPencilAlt, FaTrash } from 'react-icons/fa'
import { getAllProjects, createNewProject, renameProject, deleteProject } from '../utils/projectStorage'

const Sidebar = () => {
    const [projects, setProjects] = useState([])
    const [editingId, setEditingId] = useState(null)
    const navigate = useNavigate()
    const location = useLocation()

    useEffect(() => {
        setProjects(getAllProjects())
    }, [])

    const handleCreateNewProject = () => {
        const newProject = createNewProject(`Project ${projects.length + 1}`)
        setProjects(getAllProjects())
        navigate(`/project/${newProject.id}`)
    }

    const handleRename = (id, newName) => {
        renameProject(id, newName)
        setProjects(getAllProjects())
        setEditingId(null)
    }

    const handleDelete = (id) => {
        deleteProject(id)
        setProjects(getAllProjects())
        if (location.pathname === `/project/${id}`) {
            navigate('/new')
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
                                <Link 
                                    to={`/project/${project.id}`} 
                                    className="project-link"
                                >
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
                </div>
            </div>
        </div>
    )
}

export default Sidebar
