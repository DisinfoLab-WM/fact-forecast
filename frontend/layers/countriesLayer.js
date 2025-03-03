import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import Style from 'ol/style/Style';
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';

const countriesLayer = new VectorLayer({
    source: new VectorSource({
        url: 'assets/ne_110m_admin_0_countries.json', // Use the new file here
        format: new GeoJSON(),
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

export default countriesLayer;