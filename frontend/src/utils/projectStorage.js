const PROJECT_KEY_PREFIX = 'project_';

export const saveProject = (id, data) => {
  if (!data.createdAt) {
    data.createdAt = Date.now();
  }
  localStorage.setItem(`${PROJECT_KEY_PREFIX}${id}`, JSON.stringify(data));
};

export const getProject = (id) => {
  const projectData = localStorage.getItem(`${PROJECT_KEY_PREFIX}${id}`);
  return projectData ? JSON.parse(projectData) : null;
};

export const getAllProjects = () => {
  const projects = [];
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key.startsWith(PROJECT_KEY_PREFIX)) {
      const id = key.replace(PROJECT_KEY_PREFIX, '');
      const projectData = JSON.parse(localStorage.getItem(key));
      projects.push({ id, name: projectData.name, createdAt: projectData.createdAt });
    }
  }
  return projects.sort((a, b) => b.createdAt - a.createdAt);
};

export const createNewProject = (name) => {
  const projects = getAllProjects();
  const newId = projects.length > 0 ? Math.max(...projects.map(p => parseInt(p.id))) + 1 : 1;
  const newProject = { id: newId, name, htmlCode: '', cssCode: '', instructions: '', cssType: 'external', editClasses: false, createdAt: Date.now() };
  saveProject(newId, newProject);
  return newProject;
};

export const renameProject = (id, newName) => {
  const project = getProject(id);
  if (project) {
    project.name = newName;
    saveProject(id, project);
  }
};

export const deleteProject = (id) => {
  localStorage.removeItem(`${PROJECT_KEY_PREFIX}${id}`);
};
