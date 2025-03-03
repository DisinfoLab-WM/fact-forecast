
import './style.css';
import 'ol/ol.css';
import View from 'ol/View';
import { transformExtent } from 'ol/proj';
import { fromLonLat } from 'ol/proj';

const imageExtent = [-175, -60, 190, 80];
const transformedExtent = transformExtent(imageExtent, 'EPSG:4326', 'EPSG:3857');

const extremeResolutions = [];
const desiredFirstResolution = 26905.83328125;

extremeResolutions.push(desiredFirstResolution);
const numResolutions = 20;
const resolutionStep = Math.pow(2, 12 / numResolutions);


for (let i = 1; i <= numResolutions; i++) {
    extremeResolutions.push(extremeResolutions[0] / Math.pow(resolutionStep, i));
}
for (let i = -1; i >= -5; i--) {
    extremeResolutions.unshift(extremeResolutions[0] * Math.pow(1.25, -i));
}

console.log(extremeResolutions);
const validExtent = [-18861403.350696743, -7654109.648557382, 22089274.90336576, 11960242.813473871];


const newCustomView = new View({
    constrainResolution: true,
    center: fromLonLat([0, 0]),
    pixelRatio: 1,
    smoothExtentConstraint: false,
    minZoom: -10,
    maxZoom: 5,
    resolutions: extremeResolutions,
    extent: validExtent,
    zoom: -1,
});
export default newCustomView