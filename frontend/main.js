import './style.css';
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import { Fill, Stroke, Style as OLStyle } from 'ol/style';
import pinLayer from './layers/pinLayer';
import geojsonLayer from './layers/geojsonLayer';
import highlightedLayer, { highlightedSource } from './layers/highlightLayer.js';
import tileLayer from './layers/tileLayer';
import { toLonLat } from 'ol/proj';
import TileLayer from 'ol/layer/Tile';
import GeoJSON from 'ol/format/GeoJSON.js';
import { get } from 'ol/proj';
import { transform } from 'ol/proj';

const newView = new View({
  constrainResolution: true,
  center: [0, 0],
  zoom: 0,
  minZoom: 1,  // Set the minimum zoom level
  maxZoom: 6,
})
const map = new Map({
  target: 'map',
  layers: [tileLayer, highlightedLayer, pinLayer],
  view: newView,
  controls: [],

});

// new highlight country 
let geojsonData = null;

// **Step 1: Preload the GeoJSON data but don't render it**
fetch('assets/countries.json')
  .then(response => response.json())
  .then(data => {
    geojsonData = data; // Store it for later queries
  })
  .catch(error => console.error('Error loading GeoJSON:', error));

// **Step 2: Click event to find country by coordinates**
map.on('click', (event) => {
  if (!geojsonData) {
    console.error("GeoJSON not loaded yet!");
    return;
  }

  const format = new GeoJSON();
  const features = format.readFeatures(geojsonData, {
    featureProjection: 'EPSG:3857', // Match OpenLayers projection
  });

  // Convert clicked point to WGS84 (lat/lon)
  const clickedCoord = transform(event.coordinate, 'EPSG:3857', 'EPSG:4326');

  // **Find the closest country polygon**
  let closestFeature = null;
  let minDistance = Infinity;

  features.forEach(feature => {
    if (feature.getGeometry().intersectsCoordinate(event.coordinate)) {
      closestFeature = feature;
    }
  });

  // **Step 3: Highlight only the clicked polygon**
  if (closestFeature) {
    highlightedSource.clear(); // Clear old selection
    highlightedSource.addFeature(closestFeature); // Add new selection

    document.getElementById("countryInfo").hidden = false;
    document.getElementById("countryName").textContent = closestFeature.get("ADMIN");
  }
});