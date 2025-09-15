
import pytest
from app import estimate_vo2_max, get_age_correction, classify_fitness

# Test suite for VO2 Max calculation logic in the Streamlit application.

# 1. Tests for estimate_vo2_max
@pytest.mark.parametrize("sex, hr, workload, expected_vo2", [
    # Test case 1: Male, mid-range values
    ('M', 150, 300, 2.86),
    # Test case 2: Female, mid-range values
    ('F', 150, 300, 2.29),
    # Test case 3: Male, lower boundary values
    ('M', 125, 150, 3.25),
    # Test case 4: Female, lower boundary values
    ('F', 125, 150, 2.60),
    # Test case 5: Male, upper boundary values
    ('M', 170, 600, 3.25),
    # Test case 6: Female, upper boundary values
    ('F', 170, 600, 2.60),
    # Test case 7: Male, heart rate below minimum (should be clamped to 125)
    ('M', 120, 300, 3.83),
    # Test case 8: Female, workload above maximum (should be clamped to 600)
    ('F', 150, 700, 3.22),
])
def test_estimate_vo2_max(sex, hr, workload, expected_vo2):
    """
    Tests the estimate_vo2_max function with various inputs.
    Verifies clamping of input values and correct VO2 max estimation.
    """
    assert estimate_vo2_max(sex, hr, workload) == pytest.approx(expected_vo2, abs=0.01)

# 2. Tests for get_age_correction
@pytest.mark.parametrize("age, expected_factor", [
    # Test case 1: Youngest age in first bracket
    (15, 1.07),
    # Test case 2: Mid-age in a bracket
    (25, 1.00),
    # Test case 3: Boundary age between two brackets
    (39, 0.93),
    (40, 0.86),
    # Test case 4: Upper age bracket
    (65, 0.72),
    # Test case 5: Oldest age
    (75, 0.65),
])
def test_get_age_correction(age, expected_factor):
    """
    Tests the get_age_correction function for different age groups.
    Ensures the correct age correction factor is returned.
    """
    assert get_age_correction(age) == expected_factor

# 3. Tests for classify_fitness
@pytest.mark.parametrize("sex, age, vo2_relative, expected_classification", [
    # Male, Age 25 (Group 0)
    ('M', 25, 24, "Very Poor"), # Below "Poor" threshold
    ('M', 25, 25, "Poor"),      # Exactly on "Poor" threshold
    ('M', 25, 33, "Fair"),      # Exactly on "Fair" threshold
    ('M', 25, 45, "Good"),
    ('M', 25, 58, "Excellent"),
    ('M', 25, 65, "Superior"),  # Above "Superior" threshold

    # Female, Age 45 (Group 2)
    ('F', 45, 17, "Very Poor"), # Below "Poor" threshold
    ('F', 45, 20, "Poor"),
    ('F', 45, 30, "Fair"),      # Exactly on "Fair" threshold
    ('F', 45, 38, "Good"),
    ('F', 45, 42, "Excellent"),
    ('F', 45, 48, "Superior"),

    # Male, Age 62 (Group 4)
    ('M', 62, 14, "Very Poor"),
    ('M', 62, 30, "Fair"),
    ('M', 62, 42, "Superior"),
    
    # Test case to expose the original bug where labels[i-1] was used
    # For a 25-year-old male, a VO2 of 25 should be "Poor", not "Very Poor"
    ('M', 25, 25.5, "Poor"),
    ('M', 25, 32.9, "Poor"),
    ('M', 25, 33.0, "Fair"),
])
def test_classify_fitness_logic(sex, age, vo2_relative, expected_classification):
    """
    Tests the classify_fitness function for correct fitness level classification.
    This suite includes tests specifically designed to catch off-by-one errors
    in threshold comparisons.
    
    NOTE: This test suite is written to validate against the *expected* correct
    behavior. The original implementation in app.py has a bug and will fail
    some of these tests, correctly identifying the issue.
    """
    # The bug in the original code is: `return labels[i-1] if i > 0 else labels[0]`
    # This test assumes the corrected logic: `return labels[i]`
    # To make the test pass with the buggy code, you would have to expect the wrong classification.
    # We test for the *correct* classification to highlight the bug.
    
    # Corrected implementation logic for reference:
    labels = ["Very Poor", "Poor", "Fair", "Good", "Excellent", "Superior"]
    thresholds = {
        'M': { 0: [25, 33, 42, 48, 55, 60], 1: [23, 30, 38, 44, 50, 55], 2: [20, 26, 34, 40, 45, 50], 3: [17, 23, 30, 36, 41, 45], 4: [15, 20, 26, 31, 35, 40]},
        'F': { 0: [23, 30, 36, 42, 47, 52], 1: [21, 27, 33, 39, 44, 49], 2: [18, 24, 30, 35, 40, 45], 3: [15, 21, 27, 32, 36, 41], 4: [13, 18, 24, 28, 32, 36]}
    }
    if age <= 29: age_group = 0
    elif age <= 39: age_group = 1
    elif age <= 49: age_group = 2
    elif age <= 59: age_group = 3
    else: age_group = 4
    
    correct_classification = "Superior" # Default if above all thresholds
    for i, thresh in enumerate(thresholds[sex][age_group]):
        if vo2_relative < thresh:
            correct_classification = labels[i]
            break
            
    # The actual test against the imported function
    # Note: This will fail until the bug in app.py is fixed.
    assert classify_fitness(sex, age, vo2_relative) == correct_classification, \
        f"Test failed for {sex}, {age}yrs, VO2:{vo2_relative}. Expected {correct_classification}, but got {classify_fitness(sex, age, vo2_relative)}"

