import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import Style from 'ol/style/Style';
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';

const geojsonLayer = new VectorLayer({
    source: new VectorSource({
        url: 'assets/countries.json', // Use the new file here
        format: new GeoJSON(),
        wrapX: false,
    }),
    preload: Infinity,
    style: new Style({
        fill: new Fill({
            color: '#ccc',  // Fill color
        }),
        stroke: new Stroke({
            color: '#333',  // Stroke color
            width: 0.5,  // Stroke width
        }),

    }),
});

export default geojsonLayer;