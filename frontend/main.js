import './style.css';
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import pinLayer from './layers/pinLayer';
import highlightedLayer, { highlightedSource } from './layers/highlightLayer.js';
import countriesLayer from './layers/countriesLayer.js';
import Feature from 'ol/Feature';
import { transformExtent } from 'ol/proj';
const imageExtent = [-180, -60, 180, 85];
const transformedExtent = transformExtent(imageExtent, 'EPSG:4326', 'EPSG:3857');

const newView = new View({
  constrainResolution: true,
  center: [0, 0],
  zoom: 0,
  minZoom: 1,  // Set the minimum zoom level
  maxZoom: 6,
  extent: transformedExtent,
  pixelRatio: 1,
})

const map = new Map({
  target: 'map',
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

document.getElementById("countryInfo").hidden = false;