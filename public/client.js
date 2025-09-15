


document.getElementById('vo2-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    const response = await fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    const results = await response.json();

    if (response.ok) {
        displayResults(results);
        drawChart(data, results);
        
    } else {
        alert(results.error);
    }
});

function displayResults(results) {
    const resultsGrid = document.getElementById('results-grid');
    resultsGrid.innerHTML = `
        <div class="metric">
            <div class="metric-label">Estimated Absolute VO2 max (pre-correction)</div>
            <div class="metric-value">${results.vo2_abs} L/min</div>
        </div>
        <div class="metric">
            <div class="metric-label">Age Correction Factor</div>
            <div class="metric-value">${results.age_factor}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Age-Corrected Absolute VO2 max</div>
            <div class="metric-value">${results.vo2_abs_corrected} L/min</div>
        </div>
        <div class="metric">
            <div class="metric-label">Relative VO2 max</div>
            <div class="metric-value">${results.vo2_relative} ml/kg/min</div>
        </div>
        <div class="classification">Final Classification: ${results.classification}</div>
    `;
}

function drawChart(data, results) {
    const { avg_hr, workload, sex } = data;

    const hr_range = Array.from({length: 100}, (_, i) => 125 + (45/99) * i);
    const wl_range = Array.from({length: 100}, (_, i) => 150 + (450/99) * i);

    const z = [];
    for (let i = 0; i < wl_range.length; i++) {
        const row = [];
        for (let j = 0; j < hr_range.length; j++) {
            row.push(estimate_vo2_max_client(sex, hr_range[j], wl_range[i]));
        }
        z.push(row);
    }

    const contour = {
        x: hr_range,
        y: wl_range,
        z: z,
        type: 'contour',
        colorscale: 'Viridis',
        reversescale: true,
        colorbar: {
            title: 'VO2 max (L/min)'
        }
    };

    const point = {
        x: [avg_hr],
        y: [workload],
        mode: 'markers',
        type: 'scatter',
        marker: {
            color: 'red',
            size: 12
        },
        name: `Your Result (${avg_hr} bpm, ${workload} W)`
    };

    const layout = {
        title: 'Heart Rate vs. Workload for VO2 Max Estimation',
        xaxis: {
            title: 'Heart Rate (bpm)'
        },
        yaxis: {
            title: 'Workload (Watts)'
        },
        autosize: true
    };

    Plotly.newPlot('chart', [contour, point], layout, {responsive: true});
}

// This is a duplication of the backend logic for client-side chart generation.
// In a real-world scenario, you might have a shared library or fetch this data from the server.
function estimate_vo2_max_client(sex, hr, workload) {
    const HR_MIN = 125, HR_MAX = 170;
    const WL_MIN = 150, WL_MAX = 600;
    const VO2_MIN_M = 1.5, VO2_MAX_M = 5.0;
    const VO2_MIN_F = 1.2, VO2_MAX_F = 4.0;

    hr = Math.max(HR_MIN, Math.min(HR_MAX, hr));
    workload = Math.max(WL_MIN, Math.min(WL_MAX, workload));

    const hr_norm = (HR_MAX - hr) / (HR_MAX - HR_MIN);
    const wl_norm = (workload - WL_MIN) / (WL_MAX - WL_MIN);

    const vo2_norm = (hr_norm + wl_norm) / 2.0;

    let vo2_abs;
    if (sex.toUpperCase() === 'M') {
        vo2_abs = VO2_MIN_M + vo2_norm * (VO2_MAX_M - VO2_MIN_M);
    } else {
        vo2_abs = VO2_MIN_F + vo2_norm * (VO2_MAX_F - VO2_MIN_F);
    }

    return vo2_abs;
}
