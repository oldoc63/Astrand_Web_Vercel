# Project Overview

This project is a web-based tool for estimating VO2 max using the Astrand-Rhyming submaximal cycle ergometer protocol. It provides a user-friendly interface to calculate and visualize VO2 max based on user-provided data.

The project has two separate implementations:

1.  **Node.js/Express + HTML/JS:** A web application with a Node.js and Express backend that serves a static HTML, CSS, and JavaScript frontend. The backend exposes a `/calculate` endpoint that performs the VO2 max calculation.
2.  **Python/Streamlit:** A standalone Python application using the Streamlit library to create an interactive web interface for the same VO2 max calculation.

The core calculation logic is duplicated in both JavaScript (`vo2max.js`) and Python (`vo2max_estimator.py`).

# Building and Running

## Node.js Application

To run the Node.js application, you need to have Node.js and npm installed.

1.  Install dependencies:
    ```bash
    npm install
    ```
2.  Start the server:
    ```bash
    npm start
    ```
The application will be available at `http://localhost:3000`.

## Python Application

To run the Python application, you need to have Python and pip installed.

1.  Install dependencies:
    ```bash
    pip install streamlit matplotlib numpy
    ```
2.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

# Development Conventions

*   The project contains both JavaScript and Python code.
*   The core VO2 max estimation logic is duplicated in `vo2max.js` and `vo2max_estimator.py`. Any changes to the calculation logic should be applied to both files.
*   The Node.js application follows a standard Express.js structure, with a `public` directory for static assets.
*   The Python application uses Streamlit for the user interface.
*   The `test_main.py` file suggests that there are Python tests, which can be run with `pytest`.
