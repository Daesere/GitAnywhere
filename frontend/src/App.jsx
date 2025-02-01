import { useState, useEffect } from 'react'
import UserList from './UserList'
import './App.css'
import UserForm from './UserForm'
import CoordForm from './CoordForm'

function App() {
  const [users, setUsers] = useState([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [currentUser, setCurrentUser] = useState([])
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
    <UserList users={users} updateUser={openEditModal} updateCallback={ onUpdate } />
    <button onClick={openCreateModal}>Create New User</button>
    {isModalOpen && <div className="modal">
      <div classname="modal-content">
        <span classname="close" onClick={closeModal}>&times;</span>
        <UserForm existingUser={currentUser} updateCallback={ onUpdate } />
        </div>
    </div>
    }
    <div>
      <br />
      {
        <CoordForm updateCallback={ onUpdate } />
      }
    </div>
    
  </>
    
  
}

export default App
