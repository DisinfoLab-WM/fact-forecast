import './style.css';
import 'ol/ol.css';
import Map from 'ol/Map';
import newCustomView from './customMapView';
import { highlightLayer } from './layers/highlightLayer';
import { countryTileLayer } from './layers/countriesTileLayer';


const map = new Map({
  target: 'map',
  layers: [countryTileLayer, highlightLayer], // Add both layers to the map
  view: newCustomView,
});

// Hover effect
let highlightedFeature = null;
map.on('pointermove', function (event) {
  const pixel = event.pixel;
  const featuresAtPixel = map.getFeaturesAtPixel(pixel);

  let featureToHighlight = null;

  if (featuresAtPixel && featuresAtPixel.length > 0) {
    featureToHighlight = featuresAtPixel[0];
    const featureCountryName = featureToHighlight.get('name');
    if (featureToHighlight !== highlightedFeature) {
      // Clear the previous highlight
      if (highlightedFeature) {
        highlightLayer.getSource().clear();
      }
      // Clone feature
      const clonedFeature = featureToHighlight.clone();
      highlightLayer.getSource().addFeature(clonedFeature);
      highlightedFeature = featureToHighlight;

      // update country selected
      document.getElementById("countryInfo").hidden = false;
      document.getElementById("countryName").textContent = featureCountryName;
    }
  } else {
    // Reset highlight if no feature is hovered
    if (highlightedFeature) {
      highlightLayer.getSource().clear();
      highlightedFeature = null;
    }
    document.getElementById("countryInfo").hidden = true;
  }
});
