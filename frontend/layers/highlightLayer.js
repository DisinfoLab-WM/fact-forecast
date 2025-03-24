import Fill from 'ol/style/Fill.js';
import Stroke from 'ol/style/Stroke.js';
import Style from 'ol/style/Style.js';
import GeoJSON from 'ol/format/GeoJSON.js';
import geoJsonFeatures from '../assets/ne_110m_admin_0_countries.json';
import VectorSource from 'ol/source/Vector';
import VectorLayer from 'ol/layer/Vector';
import { defaultStyle, highlightStyle, selectedStyle } from '../countryStyles';

export const highLightLayerSource = new VectorSource({
    features: new GeoJSON({
        dataProjection: "EPSG:4326",
        featureProjection: "EPSG:3857",
    }).readFeatures(geoJsonFeatures)
});

export const highlightLayer = new VectorLayer({
    source: highLightLayerSource,
    style: (feature) => {
        const isActive = feature.get("isActive") === true;
        const isSelected = feature.get("isSelected") === true;
        return isSelected ? selectedStyle :
            isActive ? highlightStyle
                : defaultStyle;
    },
    updateWhileAnimating: true,
    updateWhileInteracting: true,
});