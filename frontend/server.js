const express = require('express');
const MBTiles = require('@mapbox/mbtiles');
const path = require('path');
const app = express();
const port = 3000;

// Set the path to your MBTiles file
const mbtilesFilePath = path.join(__dirname, 'frontend', 'assets', 'output.mbtiles');

// Function to serve tiles from MBTiles file
app.get('/tiles/:z/:x/:y.pbf', (req, res) => {
    const z = req.params.z;
    const x = req.params.x;
    const y = req.params.y;

    // Open the MBTiles file
    new MBTiles(mbtilesFilePath, (err, mbtiles) => {
        if (err) {
            return res.status(500).send("Error opening MBTiles file");
        }

        // Fetch the tile from MBTiles by zoom, x, and y
        mbtiles.getTile(z, x, y, (err, tile) => {
            if (err) {
                return res.status(404).send("Tile not found");
            }

            // Set the response header for vector tiles (MVT format)
            res.setHeader('Content-Type', 'application/vnd.mapbox-vector-tile');

            // Send the tile data as the response
            res.send(tile);
        });
    });
});

// Serve static files (like your HTML, JS, CSS)
app.use(express.static(path.join(__dirname, 'frontend')));

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
