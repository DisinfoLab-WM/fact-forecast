import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import Style from 'ol/style/Style';
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';
import { transformExtent } from 'ol/proj';
import { buffer } from 'ol/extent';
// Assuming the map projection is 'EPSG:3857' (as used in your custom view)
const mapProjection = 'EPSG:3857';  // Map projection
const bufferDistance = 90000000;

export const countryVectorSource = new VectorSource({
    loader: function (extent, resolution, projection) {
        // Transform the extent from the projection of the source data (GeoJSON) to the map projection
        const viewExtent = transformExtent(extent, projection, mapProjection);

        const bufferedExtent = buffer(viewExtent, bufferDistance)
        // Fetch the GeoJSON file and filter based on the transformed extent
        fetch('assets/ne_110m_admin_0_countries.json')
            .then(response => response.json())
            .then((data) => {
                const geojson = new GeoJSON();
                // Filter the features based on the current map's view extent
                const features = geojson.readFeatures(data, {
                    extent: bufferedExtent,
                    dataProjection: 'EPSG:4326',  // GeoJSON is in EPSG:4326
                    featureProjection: mapProjection,  // The features should be reprojected to map's projection
                });

                // Clear existing features and add the new ones for this extent
                countryVectorSource.clear();
                countryVectorSource.addFeatures(features);
            })
            .catch(err => console.error('Error loading GeoJSON:', err));
    },
    format: new GeoJSON(),
    wrapx: false,
    preload: Infinity, // Preload all features
});

export const countriesLayer = new VectorLayer({
    source: countryVectorSource,
    wrapx: false,
    preload: Infinity,
    style: new Style({
        fill: new Fill({
            color: '#ccc',
        }),
        stroke: new Stroke({
            color: '#333',
            width: 0.5,
        }),
    }),
});
