import React from "react"

const PathNuke = ({}) => {
    const onPathDelete = async () => {
        try {
            const options = {
                method: "DELETE"
            }
            const response = await fetch("http://127.0.0.1:5000/delete_path", options)
        } catch (error) {
            alert(error)
        }
    }
    return <>
        <button onClick = {() => onPathDelete()}>Delete All Paths /dev/</button>

    </>
}


export default PathNuke