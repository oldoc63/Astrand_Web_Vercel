# Astrand-Rhyming VO2max Estimator

## 1. Overview and Introduction

The Astrand-Rhyming Test is one of the most widely used submaximal exercise tests for estimating maximum oxygen uptake (VO2 max) without requiring individuals to exercise to exhaustion. Developed by Swedish physiologist Per-Olof Astrand and Irma Rhyming in the 1950s, this test provides a safe and practical alternative to direct VO2 max measurement in laboratory settings. This tool provides a web-based implementation of the Astrand-Rhyming nomogram for estimating VO2 max.

## 2. Features

*   Estimates VO2 max using the Astrand-Rhyming submaximal cycle ergometer protocol.
*   Accepts heart rate and workload data through a user-friendly web interface.
*   Provides an age-corrected VO2 max value.
*   Responsive design that works on desktops, tablets, and mobile devices.

## 3. Prerequisites

* npm 11.5.2
* node 24.8.0

## 4. Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/oldoc63/Astrand_Web_Mobile.git
    cd Astrand_Web_Mobile
    ```
2.  Run `npm start` file in your (Windows, Linux, Android, Mac) terminal. Follow the link (ctrl + click) http://localhost:3000 to your browser.

## 5. Usage Instructions

Open the tab `V02 Max Estimator` in your web browser. Fill in the required fields in the form and click the "Calculate" button.

*   **Gender**: (male/female)
*   **Age**: (years)
*   **Weight**: (kg)
*   **Exercise Heart Rate**: (bpm)
*   **Workload**: (kpm/min)

## 6. How the Calculation Works

The calculation is based on the Astrand-Rhyming nomogram, which is a graphical tool used to estimate VO2 max from heart rate and workload data. The nomogram is based on the linear relationship between heart rate, workload, and oxygen uptake.

The estimated VO2 max is then corrected for age using the following formula:

`Corrected VO2max = Estimated VO2max * (1.11 - 0.007 * age)`

## 7. Output Interpretation

The estimated VO2 max will be displayed on the web page in ml/kg/min. This value represents the maximum amount of oxygen your body can utilize during intense exercise. The higher the value, the better your cardiorespiratory fitness.

| Fitness Level | Males (ml/kg/min) | Females (ml/kg/min) |
| :--- | :--- | :--- |
| Superior | > 60 | > 56 |
| Excellent | 52-60 | 47-56 |
| Good | 44-51 | 39-46 |
| Fair | 35-43 | 31-38 |
| Poor | < 35 | < 31 |

## 8. Limitations of the Test

*   The test is a submaximal test and provides an estimation, not a direct measurement, of VO2 max.
*   The accuracy of the test can be affected by factors such as caffeine, medication, and emotional state.
*   The test is not suitable for individuals with cardiovascular or respiratory conditions.

## 9. License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
