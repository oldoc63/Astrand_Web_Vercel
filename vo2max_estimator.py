
import sys

# Age Correction Factors (from Astrand protocol)
AGE_CORRECTION = {
    (15, 19): 1.07,
    (20, 29): 1.00,
    (30, 39): 0.93,
    (40, 49): 0.86,
    (50, 59): 0.79,
    (60, 69): 0.72,
    (70, 120): 0.65  # 70+
}

# Normative Data Classification (ml/kg/min) - simplified from ACSM/Astrand tables
# Format: { (sex, age_group): [thresholds for Very Poor, Poor, Fair, Good, Excellent, Superior] }
# Age groups: 0=15-29, 1=30-39, 2=40-49, 3=50-59, 4=60+
# Thresholds: [VP, P, F, G, E, S]  each level starts at this value
CLASSIFICATION_THRESHOLDS = {
    'M': {
        0: [25, 33, 42, 48, 55, 60],   # 15-29
        1: [23, 30, 38, 44, 50, 55],   # 30-39
        2: [20, 26, 34, 40, 45, 50],   # 40-49
        3: [17, 23, 30, 36, 41, 45],   # 50-59
        4: [15, 20, 26, 31, 35, 40],   # 60+
    },
    'F': {
        0: [23, 30, 36, 42, 47, 52],   # 15-29
        1: [21, 27, 33, 39, 44, 49],   # 30-39
        2: [18, 24, 30, 35, 40, 45],   # 40-49
        3: [15, 21, 27, 32, 36, 41],   # 50-59
        4: [13, 18, 24, 28, 32, 36],   # 60+
    }
}

# Astrand Nomogram Simulation (linear interpolation between HR and Workload)
# Nomogram scales (example values  actual nomogram is linear between axes)
# We simulate by defining min/max for HR and Workload, then interpolate VO2
# Male and Female scales differ slightly  we adjust VO2 accordingly

def estimate_vo2_max(sex, hr, workload):
    """
    Simulate Astrand-Rhyming nomogram.
    Returns absolute VO2 max in L/min before age correction.
    """
    # Nomogram ranges (based on standard Astrand chart)
    HR_MIN, HR_MAX = 125, 170   # bpm
    WL_MIN, WL_MAX = 150, 600   # Watts
    VO2_MIN_M, VO2_MAX_M = 1.5, 5.0  # L/min for males
    VO2_MIN_F, VO2_MAX_F = 1.2, 4.0  # L/min for females (approx 20% lower)

    # Clamp values to nomogram range
    hr = max(HR_MIN, min(HR_MAX, hr))
    workload = max(WL_MIN, min(WL_MAX, workload))

    # The relationship is inverse for heart rate: lower HR at same workload = higher VO2max
    hr_norm = (HR_MAX - hr) / (HR_MAX - HR_MIN)
    wl_norm = (workload - WL_MIN) / (WL_MAX - WL_MIN)

    # Average the two normalized positions (simulating straight line intersection)
    vo2_norm = (hr_norm + wl_norm) / 2.0

    # Scale to VO2 max range
    if sex.upper() == 'M':
        vo2_abs = VO2_MIN_M + vo2_norm * (VO2_MAX_M - VO2_MIN_M)
    else:
        vo2_abs = VO2_MIN_F + vo2_norm * (VO2_MAX_F - VO2_MIN_F)

    return vo2_abs

def get_age_correction(age):
    for (low, high), factor in AGE_CORRECTION.items():
        if low <= age <= high:
            return factor
    return 1.0  # default

def classify_fitness(sex, age, vo2_relative):
    # Determine age group index
    if age <= 29:
        age_group = 0
    elif age <= 39:
        age_group = 1
    elif age <= 49:
        age_group = 2
    elif age <= 59:
        age_group = 3
    else:
        age_group = 4

    thresholds = CLASSIFICATION_THRESHOLDS[sex.upper()][age_group]
    labels = ["Very Poor", "Poor", "Fair", "Good", "Excellent", "Superior"]

    for i, thresh in enumerate(thresholds):
        if vo2_relative < thresh:
            return labels[i]
    return labels[-1]  # Superior

def draw_nomogram(hr, workload, vo2_abs, sex):
    print("\n" + "="*60)
    print("         ASTRAND-RHYMING NOMOGRAM (SIMULATED)")
    print("="*60)

    # Define scale heights
    HEIGHT = 20
    HR_MIN, HR_MAX = 125, 170
    WL_MIN, WL_MAX = 150, 600
    VO2_MIN = 1.2 if sex.upper() == 'F' else 1.5
    VO2_MAX = 4.0 if sex.upper() == 'F' else 5.0

    # Normalize input to scale position (0.0 to 1.0)
    hr_pos = (hr - HR_MIN) / (HR_MAX - HR_MIN)
    wl_pos = (workload - WL_MIN) / (WL_MAX - WL_MIN)
    vo2_pos = (vo2_abs - VO2_MIN) / (VO2_MAX - VO2_MIN)

    # Convert to line index (inverted for top-down display)
    hr_line = int((1 - hr_pos) * (HEIGHT - 1))
    wl_line = int((1 - wl_pos) * (HEIGHT - 1))
    vo2_line = int((1 - vo2_pos) * (HEIGHT - 1))

    # Build nomogram lines
    for i in range(HEIGHT):
        # Left: Heart Rate
        hr_val = int(HR_MIN + (HR_MAX - HR_MIN) * (1 - i/(HEIGHT-1)))
        hr_str = f"{hr_val:3d}" if i % 3 == 0 else "   "

        # Middle: VO2 max
        vo2_val = VO2_MIN + (VO2_MAX - VO2_MIN) * (1 - i/(HEIGHT-1))
        vo2_str = f"{vo2_val:4.1f}" if i % 3 == 0 else "    "

        # Right: Workload
        wl_val = int(WL_MIN + (WL_MAX - WL_MIN) * (1 - i/(HEIGHT-1)))
        wl_str = f"{wl_val:3d}" if i % 3 == 0 else "   "

        # Draw connector line
        line = list(" " * 60)
        # HR axis at col 2
        if i == hr_line:
            line[2] = '?'
        # VO2 axis at col 30
        if i == vo2_line:
            line[30] = '?'
        # WL axis at col 58
        if i == wl_line:
            line[58] = '?'

        # Draw line between HR and WL
        if hr_line <= wl_line:
            slope = (58 - 2) / (wl_line - hr_line) if wl_line != hr_line else 0
            if hr_line <= i <= wl_line:
                x = int(2 + slope * (i - hr_line))
                if 2 <= x <= 58:
                    line[x] = '\\'
        else:
            slope = (58 - 2) / (wl_line - hr_line) if wl_line != hr_line else 0
            if wl_line <= i <= hr_line:
                x = int(2 + slope * (i - hr_line))
                if 2 <= x <= 58:
                    line[x] = '/'

        # Assemble line
        output = f"{hr_str} | {''.join(line[5:55])} | {wl_str}"
        if i == vo2_line:
            output += f" ? ESTIMATED ABSOLUTE VO2 = {vo2_abs:.2f} L/min"
        print(output)

    print(" HR  |" + " " * 48 + "| WL")
    print("(bpm)|              VO2 max (L/min)                |(Watts)")
    print("="*60)

# Main CLI Application
def main():
    print("=== VO2 Max Estimator (Astrand-Rhyming Protocol) ===\n")

    # 1. Data Input
    name = input("Enter Name: ").strip()
    age = int(input("Enter Age: "))
    sex = input("Enter Sex (M/F): ").strip().upper()
    while sex not in ['M', 'F']:
        sex = input("Invalid. Enter Sex (M/F): ").strip().upper()
    weight = float(input("Enter Body Weight (kg): "))
    workload = int(input("Enter Workload (Watts, e.g., 300, 450, 600): "))
    avg_hr = int(input("Enter Average Heart Rate (bpm, final 2 min): "))

    print("\n--- CONFIRMED SUBJECT DATA ---")
    print(f"Name: {name}")
    print(f"Age: {age}")
    print(f"Sex: {sex}")
    print(f"Weight: {weight} kg")
    print(f"Workload: {workload} W")
    print(f"Avg HR: {avg_hr} bpm")
    print("-" * 40)

    # 2. Estimate Absolute VO2 max
    vo2_abs = estimate_vo2_max(sex, avg_hr, workload)
    print(f"\n[Step 1] Estimated Absolute VO2 max (pre-correction): {vo2_abs:.2f} L/min")

    # Apply age correction
    age_factor = get_age_correction(age)
    vo2_abs_corrected = vo2_abs * age_factor
    print(f"[Step 2] Age Correction Factor ({age} yrs): {age_factor:.2f}")
    print(f"[Step 3] Age-Corrected Absolute VO2 max: {vo2_abs_corrected:.2f} L/min")

    # Calculate relative VO2 max
    vo2_relative = (vo2_abs_corrected * 1000) / weight
    print(f"[Step 4] Relative VO2 max: {vo2_relative:.1f} ml/kg/min")

    # 3. Draw Nomogram
    draw_nomogram(avg_hr, workload, vo2_abs, sex)

    # 4. Classify Fitness
    classification = classify_fitness(sex, age, vo2_relative)
    print(f"\n>>> FINAL CLASSIFICATION: {classification.upper()} <<<\n")

if __name__ == "__main__":
    main()
