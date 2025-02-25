import './style.css';
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import XYZ from 'ol/source/XYZ';

import { Feature } from 'ol';
import { Point } from 'ol/geom';
import { Icon, Style } from 'ol/style';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import { fromLonLat } from 'ol/proj';
import { toLonLat } from 'ol/proj';
import GeoJSON from 'ol/format/GeoJSON';
import { Fill, Stroke, Style as OLStyle } from 'ol/style';

const apiKey = 'yrljQvG34pz4TuGaGmTY';
const mapStyle = 'outdoor';
const language = 'en';

const tileLayer = new TileLayer({
  source: new XYZ({
    url: `https://api.maptiler.com/maps/${mapStyle}/256/{z}/{x}/{y}.png?key=${apiKey}&language=${language}`,
  }),
})

const pinLayer = new VectorLayer({
  source: new VectorSource({
    features: [],
  }),
})

const geojsonLayer = new VectorLayer({
  source: new VectorSource({
    url: 'ne_110m_admin_0_countries.json', // This assumes `countries.geojson` is in the same directory as `main.js`
    format: new GeoJSON(),
  }),
  style: new OLStyle({
    stroke: new Stroke({
      color: 'purple',
      width: 1,
    }),
    fill: new Fill({
      color: 'rgba(0, 150, 255, 0.2)', // Light blue with transparency
    }),
  }),
});

const map = new Map({
  target: 'map',
  layers: [tileLayer, pinLayer, geojsonLayer],
  view: new View({
    center: [0, 0],
    zoom: 2,
  }),
});






map.on('click', (event) => {
  const clickedCoordinates = event.coordinate;

  const newPinFeature = new Feature({
    geometry: new Point(clickedCoordinates),
  });

  const pinStyle = new Style({
    image: new Icon({
      src: 'images/pin1.png',  // Example pin icon
      scale: .1,  // Adjust size of the icon
    }),
  });

  newPinFeature.setStyle(pinStyle);
  const vectorLayer = map.getLayers().getArray()[1]; // Get the vector layer
  const pinsArray = vectorLayer.getSource();
  pinsArray.addFeature(newPinFeature);
})

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
      src: 'images/pin1.png',  // Example pin icon
      scale: .1,  // Adjust size of the icon
    }),
  });

  newPinFeature.setStyle(pinStyle);
  const vectorLayer = map.getLayers().getArray()[1]; // Get the vector layer
  const pinsArray = vectorLayer.getSource();
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