import Style from 'ol/style/Style';
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';
export const defaultStyle = new Style({
    fill: new Fill({
        color: '#ccc',
    }),
    stroke: new Stroke({
        color: '#333',
        width: 0.5,
    }),
});

export const highlightStyle = new Style({
    stroke: new Stroke({
        color: 'black',
        width: .5,
    }),
    fill: new Fill({
        color: 'rgba(255, 204, 0, .7)',
    })
})

export const selectedStyle = new Style({
    stroke: new Stroke({
        color: 'black',
        width: 1,
    }),
    fill: new Fill({
        color: 'rgba(255, 204, 0, 1)',
    })
})


