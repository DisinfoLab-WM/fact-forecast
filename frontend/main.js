import './style.css';
import 'ol/ol.css';
import Map from 'ol/Map';
import newCustomView from './customMapView';
import { highlightLayer, highLightLayerSource } from './layers/highlightLayer';
import { countryTileLayer } from './layers/countriesTileLayer';

let currentCountry = ""; // current hovered country


//countryTileLayer, highlightLayer
const map = new Map({
  target: 'map',
  layers: [countryTileLayer, highlightLayer],
  view: newCustomView,
});
// highlight on pointer move
let highlightedFeatures = [];
map.on("pointermove", (evt) => {
  highlightedFeatures.forEach((f) => f.set('isActive', false));
  highlightedFeatures = []
  let currentFeatures = highLightLayerSource.getFeaturesAtCoordinate(evt.coordinate);
  if (currentFeatures.length > 0) {
    currentFeatures[0].set("isActive", true);
    highlightedFeatures.push(currentFeatures[0])
    currentCountry = currentFeatures[0].get("ADMIN");
    console.log(currentCountry)
  }
});
