import { useState, useEffect } from 'react'
import UserList from './UserList'
import './App.css'
import UserForm from './UserForm'
import CoordForm from './CoordForm'
import CoordNuke from './CoordNuke'
import Notebook from "./Flipbook";
import Maps from "./maps";


function App() {
  const [users, setUsers] = useState([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [currentUser, setCurrentUser] = useState([])
  const [isBookOpen, setIsBookOpen] = useState(false)

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    const response = await fetch('http://127.0.0.1:5000/users');
    const data = await response.json();
    setUsers(data.users);
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

    

  </>
    
  
}

export default App
