import React from 'react'
import { GoogleMap, useJsApiLoader } from '@react-google-maps/api'

const containerStyle = {
  width: '90vw',
  height: '90vh',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  margin: '0 auto',
  zIndex:5,
}

const center = {
  lat: -3.745,
  lng: -38.523,
}

function Maps() {
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
      url: 'https://raw.githubusercontent.com/magrey0/map/main/path.kml',
      map: map,
    });

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
