import React, { useEffect, useState } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Project from './components/Project'
import Sidebar from './components/Sidebar'
import Reset from './components/Reset'
import { collection, getDocs } from 'firebase/firestore/lite'
import { db } from './firebase'

export var globalProjects = {}

export const addProject = (id, projectData) => {
    globalProjects[id] = projectData
}

const AppRouter = () => {
    const [projects, setProjects] = useState([])
    const [newProject, setNewProject] = useState(false)
    const [socket, setSocket] = useState(null)

    useEffect(() => {
        const fetchProjects = async () => {
            const snapshot = await getDocs(collection(db, 'projects'))
            setProjects(snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() })))
        }
        fetchProjects()
    }, [])

    const handleNewProject = () => {
        console.log("new project created")
        setNewProject(true)
    }

    return (
        <div className="app-layout">
            <Sidebar projects={projects} setProjects={setProjects} onNewProject={handleNewProject} setSocket={setSocket} />
            <div className="main-content">
                <Routes>
                    <Route path="/" element={<Project projects={projects} setProjects={setProjects} newProject={newProject} setNewProject={setNewProject} socket={socket} />} />
                    <Route path="/project/:id" element={<Project projects={projects} setProjects={setProjects} socket={socket} />} />
                    <Route path="/reset" element={<Reset />} />
                </Routes>
            </div>
        </div>
    )
}

export default AppRouter
