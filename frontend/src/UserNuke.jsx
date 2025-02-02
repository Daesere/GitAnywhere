import React from "react"

const UserNuke = ({}) => {
    const onUserDelete = async () => {
        try {
            const options = {
                method: "DELETE"
            }
            const response = await fetch("http://127.0.0.1:5000/delete_user", options)
        } catch (error) {
            alert(error)
        }
    }
    return <>
        <button onClick = {() => onUserDelete()}>Delete All Users /dev/</button>

    </>
}


export default UserNuke