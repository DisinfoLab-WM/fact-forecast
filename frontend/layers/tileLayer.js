import TileLayer from 'ol/layer/Tile';
import XYZ from 'ol/source/XYZ';

const apiKey = 'yrljQvG34pz4TuGaGmTY';
const mapStyle = 'dataviz';
const language = 'en';

const tileLayer = new TileLayer({
    source: new XYZ({
        url: `https://api.maptiler.com/maps/${mapStyle}/256/{z}/{x}/{y}.png?key=${apiKey}&language=${language}`,
    }),
})

export default tileLayer;