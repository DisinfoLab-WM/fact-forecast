import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
const pinLayer = new VectorLayer({
    source: new VectorSource({
        features: [],
    }),
})
export default pinLayer;