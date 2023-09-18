# ESP32 Cloud

This Flask app has several routes and functions for handling and displaying data:

1. get_csv_file_path(): This function generates the CSV file path based on the current date. It ensures that a directory named "data" exists and returns a path to a CSV file with the current date in its name.

2. /flask/rec (POST request): The receive_data() function is responsible for receiving data from a POST request. It assumes that data is sent as a form field named 'data' and appends this data along with a timestamp to a CSV file. If the CSV file doesn't exist, it creates one with a header.

3. /flask/get (GET request): The get_data() function reads data from the CSV file, converts the 'timestamp' column to a datetime data type, and then filters the DataFrame to include only the rows from the last 5 minutes. The filtered data is converted to JSON and returned.

4. /flask/history (GET and POST requests): The history() function handles both GET and POST requests. When accessed via a GET request, it lists the CSV files in the "data" directory and renders a template named 'history.html', which allows users to select a CSV file for further exploration. When accessed via a POST request, it loads the selected CSV file, filters the data to include every 10th row, converts it to JSON, and renders it in a template named 'show_data.html'.

5. /flask (GET request): The index() function is the root route of the application and renders an 'index.html' template.

This Flask app appears is designed for receiving, storing, and displaying data, especially for time-series data with timestamps. It provides a web interface for exploring historical data and viewing the most recent data points from the last 5 minutes. Users can access these functionalities through their web browser by visiting the specified routes.
