import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Project from './components/Project'
import Sidebar from './components/Sidebar'
import Reset from './components/Reset'

const AppRouter = () => {
  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-content">
        <Routes>
          <Route path="/" element={<Navigate to="/new" replace />} />
          <Route path="/new" element={<Project />} />
          <Route path="/project/:id" element={<Project />} />
          <Route path="/reset" element={<Reset />} />
        </Routes>
      </div>
    </div>
  )
}

export default AppRouter
