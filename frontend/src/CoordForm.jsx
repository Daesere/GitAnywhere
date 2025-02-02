import { useState } from 'react';
import './App.css';


const CoordForm = ({ updateCallback, refreshMap }) => {
    const [latitude_1, setLatitude_1] = useState("");
    const [longitude_1, setLongitude_1] = useState("");
    const [latitude_2, setLatitude_2] = useState("");
    const [longitude_2, setLongitude_2] = useState("");
    const [isLocationConfirmed, setIsLocationConfirmed] = useState(false)

    const onSubmit = async (e) => {
        e.preventDefault()

        const data = {
            latitude_1,
            longitude_1,
            latitude_2,
            longitude_2
        }
        const url = "http://127.0.0.1:5000/create_coord"
        const options = {
            method: "POST",
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


const onConfirm = async (e) => {
    e.preventDefault()

    const url = "http://127.0.0.1:5000/create_path"
    const options = {
        method: "POST",
        headers: {
            'Content-Type': "application/json"
        }
    }
    const response = await fetch(url, options)
    if (response.status !== 201 && response.status !== 200) {
        const data = await response.json()
        alert(data.message)
    } else {
        refreshMap()
    }
}
    return <form onSubmit={onSubmit}>
        <div>
            <label htmlFor="latitude_1"><u>Starting Position</u><br></br>&nbsp;&nbsp;&nbsp;&nbsp;Latitude   :</label>
            <input
                className="input-box"
                type="text"
                id="latitude_1"
                value={latitude_1}
                onChange={(e) => setLatitude_1(e.target.value)}
            />
        </div>
        <div>
            <label htmlFor="longitude_1">&nbsp;&nbsp;&nbsp;&nbsp;Longitude  :</label>
            <input
                className="input-box"
                type="text"
                id="longitude_1"
                value={longitude_1}
                onChange={(e) => setLongitude_1(e.target.value)}
            />
        </div>
        <br></br>
        <div>
            <label htmlFor="latitude_2"><u>Destination</u><br></br>&nbsp;&nbsp;&nbsp;&nbsp;Latitude :</label>
            <input
                className="input-box"
                type="text"
                id="latitude_2"
                value={latitude_2}
                onChange={(e) => setLatitude_2(e.target.value)}
            />
        </div>
        <div>
            <label htmlFor="longitude_2">&nbsp;&nbsp;&nbsp;&nbsp;Longitude :</label>
            <input
                className="input-box"
                type="text"
                id="longitude_2"
                value={longitude_2}
                onChange={(e) => setLongitude_2(e.target.value)}
            />
        </div>
        <button
            onClick={() => setIsLocationConfirmed(true)}

            className="control-button"
            type="submit">Add Locations
        
        </button>

        {isLocationConfirmed && (<button className="confirm-box" onClick={onConfirm}>Confirm Location</button>)}
    </form>
}

export default CoordForm