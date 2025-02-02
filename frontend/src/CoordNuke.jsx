import React from "react"

const CoordNuke = ({}) => {
    const onCoordDelete = async () => {
        try {
            const options = {
                method: "DELETE"
            }
            const response = await fetch("http://127.0.0.1:5000/delete_coord", options)
        } catch (error) {
            alert(error)
        }
    }
    return <>
        <button onClick = {() => onCoordDelete()}>Delete Earliest Coords /dev/</button>

    </>
}


export default CoordNuke