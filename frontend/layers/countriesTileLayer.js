import MVT from 'ol/format/MVT';
import VectorSource from 'ol/source/Vector';
import VectorTileLayer from 'ol/layer/VectorTile';
import VectorTileSource from 'ol/source/VectorTile';
import { defaultStyle } from '../countryStyles';
export const countryTileLayer = new VectorTileLayer({
    source: new VectorTileSource({
        url: 'https://api.maptiler.com/tiles/69f2b1b6-f70b-4d09-97b9-81bfa89d7fb6/{z}/{x}/{y}.pbf?key=C6lVjNBY1f8WGTANpsGs',
        format: new MVT(),
    }),
    preload: Infinity,
    style: defaultStyle, // Default style applied to all features
});