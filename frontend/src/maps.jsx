import React from 'react'
import { GoogleMap, useJsApiLoader } from '@react-google-maps/api'

const containerStyle = {
  width: '400px',
  height: '400px',
}

const center = {
  lat: -3.745,
  lng: -38.523,
}


function Maps({map_url, update}) {
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: 'AIzaSyBZc-TWI9acnxpjYfP9WnDbTRTKStQvvBA',
  })

  const [map, setMap] = React.useState(null)
  

  const onLoad = React.useCallback(function callback(map) {
//    const bounds = new window.google.maps.LatLngBounds(center)
//    map.fitBounds(bounds)

     
    setMap(map)

    const kmlLayer = new window.google.maps.KmlLayer({
      url: map_url,
      map: map,
    });
    update()

  }, [])

  const onUnmount = React.useCallback(function callback(map) {
    setMap(null)
  }, [])

  return isLoaded ? (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      zoom={10}
      onLoad={onLoad}
      onUnmount={onUnmount}
    >
      {/* Child components, such as markers, info windows, etc. */}
      <></>
    </GoogleMap>
  ) : (
          <></>
  )
}


export default React.memo(Maps)
