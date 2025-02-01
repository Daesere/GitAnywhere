import React from "react"

const UserList = ({ users, updateUser, updateCallback }) => {
    const onDelete = async (id) => { 
        try {
            const options = {
                method: "DELETE"
            }
            const response = await fetch(`http://127.0.0.1:5000/delete_user/${id}`, options)
            if (response.status === 200) {
                updateCallback()
            } else {
                console.error("Failed to delete")
            }
        } catch (error) {
            alert(error)
        }
    }

    return <div>
        <h2>Users</h2>
        <table>
            <thead>
                <tr>
                    <th>First Name</th>
                    <th>Weight</th>
                    <th>Height</th>
                    <th>Actions</th>
                </tr>
            </thead>
        <tbody>
        {users.map((user) => (
        <tr key={user.id}>
            <td>{user.firstName}</td>
            <td>{user.weight}</td>
            <td>{user.height}</td>
            <td>
                <button onClick={() => updateUser(user)}>Update</button>
                <button onClick = {() => onDelete(user.id)}>Delete</button>
            </td>
        </tr>
        ))}
    </tbody>
    </table>
    </div>
}
export default UserList