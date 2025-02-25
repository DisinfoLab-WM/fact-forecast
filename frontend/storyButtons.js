import { fromLonLat } from 'ol/proj';         // For converting coordinates
import Feature from 'ol/Feature';              // For creating features
import Point from 'ol/geom/Point';            // For defining point geometry
import { Style, Fill, Stroke } from 'ol/style'; // For styling features
import Icon from 'ol/style/Icon';              // For defining icons
import pinLayer from './layers/pinLayer';      // Import the pin layer (assuming it's defined separately)


function getRandomCoordinates() {
    // Latitude between -50° and +50° (to avoid too far south or north)
    const latitude = (Math.random() * 100 - 50).toFixed(6); // Between -50 and +50 with 6 decimal places

    // Longitude between -180° and +180° (full range)
    const longitude = (Math.random() * 360 - 180).toFixed(6); // Between -180 and +180 with 6 decimal places
    const coordinateArray = [parseFloat(longitude), parseFloat(latitude)];
    const lonLat = fromLonLat(coordinateArray);
    return lonLat;
}

function spawnRandomPins() {
    const randomCoordinates = getRandomCoordinates()

    console.log(randomCoordinates);
    const newPinFeature = new Feature({
        geometry: new Point(randomCoordinates),
    });

    const pinStyle = new Style({
        image: new Icon({
            src: 'assets/images/pin1.png',  // Example pin icon
            scale: .1,  // Adjust size of the icon
        }),
    });

    newPinFeature.setStyle(pinStyle);
    const pinsArray = pinLayer.getSource();
    pinsArray.addFeature(newPinFeature);
}

const buttons = document.querySelectorAll("button")
buttons.forEach(button => {
    button.addEventListener('click', () => {
        console.log("click")
        for (let i = 0; i < 8; i++) {
            setTimeout(() => {
                spawnRandomPins();
            }, i * 300);  // 2000 milliseconds = 2 seconds
        }
    })
})
