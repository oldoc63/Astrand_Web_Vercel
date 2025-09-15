
const express = require('express');
const path = require('path');
const { estimate_vo2_max, get_age_correction, classify_fitness } = require('./vo2max.js');

const app = express();
const port = 3000;

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

app.post('/calculate', (req, res) => {
    const { age, sex, weight, workload, avg_hr } = req.body;

    if (!age || !sex || !weight || !workload || !avg_hr) {
        return res.status(400).json({ error: 'Missing required fields' });
    }

    const vo2_abs = estimate_vo2_max(sex, avg_hr, workload);
    const age_factor = get_age_correction(age);
    const vo2_abs_corrected = vo2_abs * age_factor;
    const vo2_relative = (vo2_abs_corrected * 1000) / weight;
    const classification = classify_fitness(sex, age, vo2_relative);

    res.json({
        vo2_abs: vo2_abs.toFixed(2),
        age_factor: age_factor.toFixed(2),
        vo2_abs_corrected: vo2_abs_corrected.toFixed(2),
        vo2_relative: vo2_relative.toFixed(1),
        classification: classification.toUpperCase(),
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
