import './style.css';
import 'ol/ol.css';
import {getCenter} from 'ol/extent';
import {easeOut} from 'ol/easing';
import Map from 'ol/Map';
import newCustomView from './customMapView';
import { highlightLayer, highLightLayerSource } from './layers/highlightLayer';
import { loadArticlesForCountry, emptyNarratives } from './storyContainer';
import DoubleClickZoom from 'ol/interaction/DoubleClickZoom';
let currentCountry = ""; // current hovered country
let hoverToggle = true;


let countrySelected = document.querySelector("#selectedCountry");
// highlightLayer
const map = new Map({
  target: 'map',
  layers: [highlightLayer],
  view: newCustomView
});

//flyOut(map.getView());

// Disable double-click zoom by removing the interaction
map.getInteractions().forEach(function (interaction) {
  if (interaction instanceof DoubleClickZoom) {
    map.removeInteraction(interaction);
  }
});

// highlight on pointer move
let highlightedFeatures = [];
let selectedFeature = null;
map.on("pointermove", (evt) => {
  // reset highlight
  highlightedFeatures.forEach((f) => f.set('isActive', false));
  highlightedFeatures = [];
  // get features
  let currentFeatures = highLightLayerSource.getFeaturesAtCoordinate(evt.coordinate);
  if (currentFeatures.length > 0 && selectedFeature !== currentFeatures[0]) {
    currentFeatures[0].set("isActive", true);
    highlightedFeatures.push(currentFeatures[0])
  }

});

// select a country
map.on("click", (evt) => {
  if (selectedFeature !== null && selectedFeature != undefined) {
    selectedFeature.set('isSelected', false);
  }
  
  selectedFeature = null;
  
  // deselect if click on ocean
  selectedFeature = highlightedFeatures.pop();
  if (selectedFeature !== null && selectedFeature != undefined) {
    selectedFeature.set('isActive', false);
    selectedFeature.set('isSelected', true);
    console.log(selectedFeature);
    // Get country name and map it to a supported country code
    let countryName = selectedFeature.get("admin");
    let countryCode = mapToSupportedCountry(countryName);
    currentCountry = countryCode;
    //update stories
    console.log(currentCountry)
    if (countrySelected.textContent !== currentCountry) {
      // Load articles from the backend API
      loadArticlesForCountry(currentCountry);
      
      // Fly to the selected country
      flyTo(selectedFeature, function () {}, map.getView());
    }
    countrySelected.textContent = currentCountry;
  } else if (countrySelected.textContent == "No Country"){
      
  } else {
	  currentCountry = "";
    countrySelected.textContent = "No Country";
    // rehighlight deselected country
    let currentFeatures = highLightLayerSource.getFeaturesAtCoordinate(evt.coordinate);
    emptyNarratives();
    if (currentFeatures.length > 0 && selectedFeature !== currentFeatures[0]) {
      currentFeatures[0].set("isActive", true);
      highlightedFeatures.push(currentFeatures[0]);
    }
	flyOut(map.getView());
  }
	
});

function flyTo(selectedFeature, done, view) {
  let ext = selectedFeature.get("geometry").getExtent();
  let location = getCenter(ext);
  let z = view.getZoomForResolution(view.getResolutionForExtent(ext)) - 3;
  const duration = 1500;
  view.animate(
    {
      center: location,
      duration: duration,
	  zoom: z
    }
  );
}

function flyOut(view) {
  // console.log("flying out");
  const duration = 1000;
  view.animate(
    {
      center: [0,0],
      duration: duration,
	  zoom: 0,
	  easing: easeOut
    }
  );
}

/**
 * Map country names to supported country codes
 * @param {string} countryName - The country name from the map feature
 * @returns {string} - The supported country code
 */
function mapToSupportedCountry(countryName) {
  // Map of country names to supported country codes
  const countryMapping = {
    "United States of America": "USA"
    // Add more mappings as needed
  };

  // Check if we have a direct mapping
  if (countryMapping[countryName]) {
    return countryMapping[countryName];
  }

  // If no direct mapping, use the country name as is
  // This might not work for all countries, but it's a fallback
  console.log(`No mapping found for country: ${countryName}, using as is`);
  return countryName.toUpperCase();
}

