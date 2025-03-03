import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import { Style, Stroke, Fill } from 'ol/style';

export const highlightedSource = new VectorSource();

// Layer for the clicked polygon (initially empty)
const highlightedLayer = new VectorLayer({
    source: highlightedSource,
    style: new Style({
        stroke: new Stroke({
            color: '#00000', // Blue border
            width: 1
        }),
        fill: new Fill({
            color: '#ffcc00' // Light blue fill
        })
    })
});
export default highlightedLayer