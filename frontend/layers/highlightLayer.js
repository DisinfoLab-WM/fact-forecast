import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import { highlightStyle } from '../countryStyles';


export const highlightLayer = new VectorLayer({
    source: new VectorSource(),
    style: highlightStyle,
    visible: true,
});