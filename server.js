const express = require('express');
const app = express();
const port = 3000;
const { spawn } = require('child_process');

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.static('scripts'));

// Function to run the Python script
const runScript = (script, url) => {
    return new Promise((resolve, reject) => {
        const py = spawn('python', [script, url]);

        let data = '';
        py.stdout.on('data', (chunk) => {
            data += chunk.toString();
        });

        py.stderr.on('data', (err) => {
            console.error(err.toString());
            reject(err.toString());
        });

        py.on('close', (code) => {
            if (code === 0) {
                try {
                    console.log(data)
                    const result = JSON.parse(data);
                    resolve(result);
                } catch (err) {
                    reject('Failed to parse JSON');
                }
            } else {
                reject(`Python script exited with code ${code}`);
            }
        });
    });
};

app.get('/', async (req, res) => {
    res.render('index');
});

app.get('/get_data', async (req, res) => {
    console.log('Scanning URL:', req.query.url);

    try {
        const url = req.query.url;
        const script = 'python/script.py';
        const data = await runScript(script, url);
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: error });
    }
});

app.listen(port, () => {
    console.log(`App listening at http://localhost:${port}`);
});
