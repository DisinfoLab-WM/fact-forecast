import "./style.css";
import "ol/ol.css";
import Map from "ol/Map";
import newCustomView from "./customMapView";
import { highlightLayer, highLightLayerSource } from "./layers/highlightLayer";
import {
  createRandomNarrative,
  emptyNarratives,
  getNArticles,
} from "./storyContainer";
import DoubleClickZoom from "ol/interaction/DoubleClickZoom";
let currentCountry = ""; // current hovered country
let hoverToggle = true;

let countrySelected = document.querySelector("#selectedCountry");
// highlightLayer
const map = new Map({
  target: "map",
  layers: [highlightLayer],
  view: newCustomView,
});
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
  highlightedFeatures.forEach((f) => f.set("isActive", false));
  highlightedFeatures = [];
  // get features
  let currentFeatures = highLightLayerSource.getFeaturesAtCoordinate(
    evt.coordinate,
  );
  if (currentFeatures.length > 0 && selectedFeature !== currentFeatures[0]) {
    currentFeatures[0].set("isActive", true);
    highlightedFeatures.push(currentFeatures[0]);
  }
});

// select a country
map.on("click", (evt) => {
  if (selectedFeature !== null && selectedFeature != undefined) {
    selectedFeature.set("isSelected", false);
  }
  selectedFeature = null;
  // deselect if click on ocean
  selectedFeature = highlightedFeatures.pop();
  if (selectedFeature !== null && selectedFeature != undefined) {
    selectedFeature.set("isActive", false);
    selectedFeature.set("isSelected", true);
    console.log(selectedFeature);
    currentCountry =
      selectedFeature.get("admin").length > 12
        ? selectedFeature.get("abbrev")
        : selectedFeature.get("admin"); // if name is too long get abbreviation
    //update stories
    console.log(currentCountry);
    if (countrySelected.textContent !== currentCountry) {
      emptyNarratives();
      let randomNumber = Math.min(
        Math.floor(Math.random() * 6 + 1),
        Math.floor(Math.random() * 6 + 1),
      );
      getNArticles("USA", randomNumber);
    }
    countrySelected.textContent = currentCountry;
  } else {
    currentCountry = "";
    countrySelected.textContent = "No Country";
    // rehighlight deselected country
    let currentFeatures = highLightLayerSource.getFeaturesAtCoordinate(
      evt.coordinate,
    );
    emptyNarratives();
    if (currentFeatures.length > 0 && selectedFeature !== currentFeatures[0]) {
      currentFeatures[0].set("isActive", true);
      highlightedFeatures.push(currentFeatures[0]);
    }
  }
});
