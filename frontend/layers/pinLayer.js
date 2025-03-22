import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
const pinLayer = new VectorLayer({
    source: new VectorSource({
        features: [],
        wrapX: false,
    }),
    preload: Infinity,
})
export default pinLayer;