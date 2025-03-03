import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import Style from 'ol/style/Style';
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';

export const countryVectorSource = new VectorSource({
    url: 'assets/ne_110m_admin_0_countries.json', // Same GeoJSON file
    format: new GeoJSON(), loadTilesWhileAnimating: true,
})

export const countriesLayer = new VectorLayer({
    source: countryVectorSource,
    wrapx: false,
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
