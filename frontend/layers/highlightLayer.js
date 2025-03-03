import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import { Style, Stroke, Fill } from 'ol/style';

export const highlightedSource = new VectorSource();

// Layer for the clicked polygon (initially empty)
const highlightedLayer = new VectorLayer({
    source: highlightedSource,
    wrapX: false,
    style: new Style({
        fill: new Fill({
            color: 'rgba(255, 204, 0, 1)',  // Fill color
        }),
        stroke: new Stroke({
            color: '#333',  // Stroke color
            width: 0.5,  // Stroke width
        }),
    })
});
export default highlightedLayer