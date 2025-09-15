
// Age Correction Factors (from Astrand protocol)
const AGE_CORRECTION = {
    "15-19": 1.07,
    "20-29": 1.00,
    "30-39": 0.93,
    "40-49": 0.86,
    "50-59": 0.79,
    "60-69": 0.72,
    "70-120": 0.65, 
};

// Normative Data Classification (ml/kg/min)
const CLASSIFICATION_THRESHOLDS = {
    'M': {
        "15-29": [25, 33, 42, 48, 55, 60],
        "30-39": [23, 30, 38, 44, 50, 55],
        "40-49": [20, 26, 34, 40, 45, 50],
        "50-59": [17, 23, 30, 36, 41, 45],
        "60+": [15, 20, 26, 31, 35, 40],
    },
    'F': {
        "15-29": [23, 30, 36, 42, 47, 52],
        "30-39": [21, 27, 33, 39, 44, 49],
        "40-49": [18, 24, 30, 35, 40, 45],
        "50-59": [15, 21, 27, 32, 36, 41],
        "60+": [13, 18, 24, 28, 32, 36],
    }
};

function estimate_vo2_max(sex, hr, workload) {
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

function get_age_correction(age) {
    for (const ageRange in AGE_CORRECTION) {
        const [low, high] = ageRange.split('-').map(Number);
        if (age >= low && age <= high) {
            return AGE_CORRECTION[ageRange];
        }
    }
    return 1.0;
}

function classify_fitness(sex, age, vo2_relative) {
    let age_group;
    if (age <= 29) age_group = "15-29";
    else if (age <= 39) age_group = "30-39";
    else if (age <= 49) age_group = "40-49";
    else if (age <= 59) age_group = "50-59";
    else age_group = "60+";

    const thresholds = CLASSIFICATION_THRESHOLDS[sex.toUpperCase()][age_group];
    const labels = ["Very Poor", "Poor", "Fair", "Good", "Excellent", "Superior"];

    for (let i = 0; i < thresholds.length; i++) {
        if (vo2_relative < thresholds[i]) {
            return labels[i];
        }
    }
    return labels[labels.length - 1]; // Superior
}

module.exports = { 
    estimate_vo2_max, 
    get_age_correction, 
    classify_fitness,
    AGE_CORRECTION,
    CLASSIFICATION_THRESHOLDS 
};
