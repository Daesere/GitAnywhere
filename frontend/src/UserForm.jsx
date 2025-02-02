import { useState } from 'react';

const UserForm = ({ existingUser = {}, updateCallback }) => {
    const [firstName, setFirstName] = useState(existingUser.firstName || "");
    const [weight, setWeight] = useState(existingUser.weight || "");
    const [height, setHeight] = useState(existingUser.height || "");

    const updating = Object.entries(existingUser).length !== 0;

    const onSubmit = async (e) => {
        e.preventDefault()

        const data = {
            firstName,
            weight,
            height
        }
        const url = "http://127.0.0.1:5000/" + ( updating  ? `update_user/${existingUser.id}` : "create_user")
        const options = {
            method: updating ? "PATCH" : "POST",
            headers: {
                'Content-Type': "application/json"
            },
            body: JSON.stringify(data)
        }
        const response = await fetch(url, options)
        if (response.status !== 201 && response.status !== 200) {
            const data = await response.json()
            alert(data.message)
        } else {
            updateCallback()
        }
    }
    return <form onSubmit={onSubmit}>
        <div>
            <label htmlFor="firstName">&nbsp;&nbsp;&nbsp;&nbsp;First Name:  </label>
            <input
                type="text"
                id="firstName"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
            />
        </div>
        <div>
            <label htmlFor="weight">&nbsp;&nbsp;&nbsp;&nbsp;Weight: </label>
            <input
                type="text"
                id="weight"
                value={weight}
                onChange={(e) => setWeight(e.target.value)}
            />
        </div>
        <div>
            <label htmlFor="height">&nbsp;&nbsp;&nbsp;&nbsp;Height: </label>
            <input
                type="text"
                id="height"
                value={height}
                onChange={(e) => setHeight(e.target.value)}
            />
        </div>
        <button type="submit">{updating ? "Update" : "Create"}</button>
    </form>
}

export default UserForm