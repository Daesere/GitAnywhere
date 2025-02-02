import { useState, useEffect } from 'react'
import UserList from './UserList'
import './App.css'
import UserForm from './UserForm'
import CoordForm from './CoordForm'
import CoordNuke from './CoordNuke'
import UserNuke from './UserNuke'
import PathNuke from './PathNuke'
import Notebook from "./Flipbook";
import Maps from "./maps";


function App() {
  const [users, setUsers] = useState([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [currentUser, setCurrentUser] = useState([])
  const [isBookOpen, setIsBookOpen] = useState(false)
  const [map, setMap] = useState([])

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    const response = await fetch('http://127.0.0.1:5000/users');
    const data = await response.json();
    setUsers(data.users);
  }
  
  const fetchMap = async () => {
    const response = await fetch('http://127.0.0.1:5000/maps');
    const data = await response.json();
    setMap(data.map);
  }

  const closeModal = () => {
    setIsModalOpen(false)
    setCurrentUser({})
  }

  const closeBook = () => {
    setIsBookOpen(false)
  }

  const openBook = () => {
    if (!isBookOpen) setIsBookOpen(true)
  }

  const toggleBook = () => {
    setIsBookOpen(!isBookOpen)
  }


  const openCreateModal = () => { 
    if (!isModalOpen) setIsModalOpen(true)
  }
  
  const openEditModal = (user) => {
    if (isModalOpen) return 
    setCurrentUser(user)
    setIsModalOpen(true)
  }

  const onUpdate = () => {
    closeModal()
    fetchUsers()
    
  }

  const refreshMap = () => {
    // DO SOMETHING HERE TO REFRESH MAP
    fetchMap()
  }
  
  return <>
    <br />
    <br />
    <div className="App">
    </div>

    <div className="App">
    {isBookOpen && <Notebook />}
      <button onClick={toggleBook}>
        {isBookOpen ? 'Hide Notebook' : 'Show Notebook'}
      </button>
      
    </div>
    <br />

    <Maps />

    <div>
      <CoordNuke />
    </div>
    <div>
      <UserNuke />
    </div>
    <div>
      <PathNuke />
</div>
    

  </>
    
  
}

export default App
