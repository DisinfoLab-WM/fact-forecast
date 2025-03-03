import './style.css';
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import pinLayer from './layers/pinLayer';
import highlightedLayer, { highlightedSource } from './layers/highlightLayer.js';
import { countriesLayer, countryVectorSource } from './layers/countriesLayer';
import Feature from 'ol/Feature';
import { transformExtent } from 'ol/proj';
import vectorTileLayer from './layers/tileLayer.js';
import { fromLonLat } from 'ol/proj';
import newCustomView from './customMapView.js';


const map = new Map({
  target: 'map',
  renderer: 'webgl',
  layers: [countriesLayer, highlightedLayer, pinLayer],
  view: newCustomView,
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



