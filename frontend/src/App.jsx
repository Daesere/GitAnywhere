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
  const [seed, setSeed] = useState(1);
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

  
  const reset = () => {
        setSeed(Math.random());
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
  }
  
  return <>
     
    <br />
    <br />
    <div className="App">
    </div>

    
    <br />

    <div className="MapComponent">
      <iframe 
          key={seed}
          src="/route_map.html" // Ensure the file is inside the public folder
          width="100%"
          height="600px"
          frameBorder="0"
          title="Route Map"
        ></iframe>
      </div>

    <div className="App">
    {isBookOpen && (
      <div style={{
        position: 'absolute', // Or 'fixed' depending on your needs
        top: '0',
        left: '0',
        width: '100vw',
        height: '150vh',
        zIndex: 5, // Ensure it overlays on top
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}>
        <Notebook />
      </div>
    )}

      <button onClick={toggleBook}
        className="book-box"
        style={{
          position: 'relative', // Or 'fixed' depending on your needs
          zIndex: 10, // Higher than the overlay
        }}
        >
      </button>
    </div>
    <div>
      <CoordNuke />
    </div>
    <button onClick={reset} 
      style={{ zIndex: 10, }}>Reset
    </button>

    <div>
      <UserNuke />
    </div>
    <div>
      <PathNuke />
</div>
    

  </>
    
  
}

export default App
