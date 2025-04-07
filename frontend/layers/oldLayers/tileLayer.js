import TileLayer from 'ol/layer/Tile';
import XYZ from 'ol/source/XYZ';

const mapStyle = 'streets'; // MapTiler style ID
const language = 'en';

const tileLayer = new TileLayer({
    source: new XYZ({
        url: `https://api.maptiler.com/tiles/69f2b1b6-f70b-4d09-97b9-81bfa89d7fb6/tiles.json?key=`,
        maxZoom: 5, // Prevents higher-detail tile loading
        wrapX: false,
    }),
    preload: Infinity,
});

export default tileLayer;
