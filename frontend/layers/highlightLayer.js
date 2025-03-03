import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import { Style, Stroke, Fill } from 'ol/style';

export const highlightedSource = new VectorSource();

// Layer for the clicked polygon (initially empty)
const highlightedLayer = new VectorLayer({
    source: highlightedSource,
    style: new Style({
        stroke: new Stroke({
            color: 'rgba(30, 144, 255, 0.8)', // Blue border
            width: 3
        }),
        fill: new Fill({
            color: 'rgba(30, 144, 255, 0.15)' // Light blue fill
        })
    })
});
export default highlightedLayer