import Style from 'ol/style/Style';
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';
export const defaultStyle = new Style({
    fill: new Fill({
        color: '#ccc',
    }),
    stroke: new Stroke({
        color: '#333',
        width: 0.5,
    }),
});

export const highlightStyle = new Style({
    fill: new Fill({
        color: 'rgba(255, 204, 0, 1)', // Fill color
    }),
    stroke: new Stroke({
        color: '#333', // Stroke color
        width: 0.5, // Stroke width
    }),
});