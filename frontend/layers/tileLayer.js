import TileLayer from 'ol/layer/Tile';
import XYZ from 'ol/source/XYZ';

const apiKey = 'C6lVjNBY1f8WGTANpsGs';
const mapStyle = '51f130a6-9fcc-45d4-b015-4d963c430814'; // MapTiler style ID
const language = 'en';

const tileLayer = new TileLayer({
    source: new XYZ({
        url: `https://api.maptiler.com/maps/${mapStyle}/256/{z}/{x}/{y}.png?key=${apiKey}&language=${language}`,
        maxZoom: 5, // Prevents higher-detail tile loading
        wrapX: false,
    }),
    preload: Infinity,
});

export default tileLayer;
