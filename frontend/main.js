import './style.css';
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import pinLayer from './layers/pinLayer';
import highlightedLayer, { highlightedSource } from './layers/highlightLayer.js';
import { countriesLayer, countryVectorSource } from './layers/countriesLayer';
import Feature from 'ol/Feature';
import { transformExtent } from 'ol/proj';
import VectorSource from 'ol/source/Vector.js';

const imageExtent = [-175, -60, 190, 80];
const transformedExtent = transformExtent(imageExtent, 'EPSG:4326', 'EPSG:3857');

const newView = new View({
  constrainResolution: true,
  center: [0, 0],
  zoom: 0,
  minZoom: 0,  // Set the minimum zoom level
  maxZoom: 6,
  extent: transformedExtent,
  pixelRatio: 1,
  smoothExtentConstraint: false,
})

const map = new Map({
  target: 'map',
  renderer: 'webgl',
  layers: [countriesLayer, highlightedLayer, pinLayer],
  view: newView,
  controls: [],

});


map.on('pointermove', function (event) {
  const pixel = event.pixel;
  highlightedLayer.getSource().clear();

  map.forEachFeatureAtPixel(pixel, function (feature) {
    const geometry = feature.getGeometry();

    if (geometry.getType() === 'GeometryCollection') {
      const geometries = geometry.getGeometries();

      geometries.forEach((geom) => {
        if (geom.intersectsCoordinate(event.coordinate)) {
          const highlightedFeature = new Feature(geom);
          highlightedLayer.getSource().addFeature(highlightedFeature);
        }
      });
    } else {
      if (geometry.intersectsCoordinate(event.coordinate)) {
        highlightedLayer.getSource().addFeature(feature);
      }
    }
  });
});
// tile loading optimizations
function preloadVectorFeatures() {
  const extent = map.getView().calculateExtent(map.getSize());

  // Filter features that are within the current extent
  countryVectorSource.forEachFeatureInExtent(extent, (feature) => {
    // If you need to do something with each feature (like setting a property to "loaded")
    feature.set('loaded', true); // Example: setting a property to mark it as loaded
  });
}

// Listen for pointerdrag event to preload vector features
map.on('pointerdrag', function () {
  preloadVectorFeatures();
});