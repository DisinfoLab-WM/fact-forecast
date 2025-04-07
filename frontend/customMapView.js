import './style.css';
import 'ol/ol.css';
import View from 'ol/View';
import { transformExtent } from 'ol/proj';
import { fromLonLat } from 'ol/proj';

// Your image extent in EPSG:4326 (geographic coordinates)
const imageExtent = [-175, -85, 190, 82];
const transformedExtent = transformExtent(imageExtent, 'EPSG:4326', 'EPSG:3857');

// Initialize the resolutions array for custom zoom levels
const extremeResolutions = [];
const desiredFirstResolution = 26905.83328125;

// Start with the desired first resolution
extremeResolutions.push(desiredFirstResolution);

// Number of zoom levels you want to generate
const numResolutions = 30; // Increased to support more zoom-out levels
const resolutionStep = Math.pow(2, 12 / numResolutions);

// Generate resolutions for zoom levels
for (let i = 1; i <= numResolutions; i++) {
    extremeResolutions.push(extremeResolutions[0] / Math.pow(resolutionStep, i));
}

// Create additional zoom levels for extreme zoom-out
for (let i = -1; i >= -10; i--) {
    extremeResolutions.unshift(extremeResolutions[0] * Math.pow(1.25, -i));
}

// Ensure the resolutions array is correctly formed
console.log(extremeResolutions);

// Define the valid extent for your map (the visible area)
const validExtent = [-18861403.350696743, -10071868.8804, 21089274.90336576, 16979886.33];

// Set the custom view for the map
const newCustomView = new View({
    // constrainResolution: true,
    center: fromLonLat([0, 0]), // Center of the map
    pixelRatio: 1,
    smoothExtentConstraint: false,
    minZoom: 0, // Custom zoom-out (negative values)
    maxZoom: 4,   // Custom zoom-in (positive values)
    // resolutions: extremeResolutions, // Use the custom resolutions array
    extent: validExtent,  // Define valid map bounds
    zoom: 0, // Default zoom level
});


export default newCustomView;
