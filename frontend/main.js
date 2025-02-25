import './style.css';
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import { Fill, Stroke, Style as OLStyle } from 'ol/style';
import pinLayer from './layers/pinLayer';
import geojsonLayer from './layers/geojsonLayer';
import tileLayer from './layers/tileLayer';


const map = new Map({
  target: 'map',
  layers: [tileLayer, geojsonLayer, pinLayer],
  view: new View({
    center: [0, 0],
    zoom: 2,
  }),
});

// highlight country
map.on('click', (event) => {
  unhighlightAllFeatures(geojsonLayer)
  map.forEachFeatureAtPixel(event.pixel, function (feature, layer) {
    feature.setStyle(new OLStyle({
      stroke: new Stroke({
        color: 'rgba(30, 144, 255, 0.8)',
        width: 3,
      }),
      fill: new Fill({
        color: 'rgba(30, 144, 255, 0.15)', // Highlight with red fill
      }),
    }));
	document.getElementById("countryInfo").hidden=false;
	document.getElementById("countryName").textContent=feature.get("ADMIN");
  })
});

function unhighlightAllFeatures(vectorLayer) {
  const source = vectorLayer.getSource();
  source.getFeatures().forEach((feature) => {
    feature.setStyle(null); // Reset to default style
  });
  document.getElementById("countryInfo").hidden=true;
}
