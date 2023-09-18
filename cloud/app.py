from flask import Flask, request, jsonify, render_template
import pandas as pd
from datetime import datetime, timedelta
import os

app = Flask(__name__)

def get_csv_file_path():
    # Create a directory for data if it doesn't exist
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    # Generate the CSV file path based on the current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(data_dir, f"{current_date}.csv")

@app.route('/flask/rec', methods=['POST'])
def receive_data():
    try:
        print("Received data")
        received_data = request.form.get('data')  # Assuming the ESP32 sends the data as a form field named 'data'

        # Create a timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        csv_file_path = get_csv_file_path()

        # Check if the CSV file exists, and if not, create it with a header
        if not os.path.exists(csv_file_path):
            df = pd.DataFrame(columns=['timestamp', 'data'])
            df.to_csv(csv_file_path, index=False)

        data_df = pd.read_csv(csv_file_path)

        data_to_append = {'timestamp': timestamp, 'data': received_data}
        data_df = data_df.append(data_to_append, ignore_index=True)

        # Append the new data to the CSV file
        data_df.to_csv(csv_file_path, index=False)

        print(f"Received data: {received_data}")
        return "Data received successfully", 200
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return str(e), 500

@app.route('/flask/get', methods=['GET'])
def get_data():
    try:
        csv_file_path = get_csv_file_path()
        data_df = pd.read_csv(csv_file_path)
        # last_100_data_df = data_df.tail(100)
        data_df['timestamp'] = pd.to_datetime(data_df['timestamp'])

        # Calculate the timestamp for 5 minutes ago
        
        five_minutes_ago = datetime.now() - timedelta(minutes=5)

        # Filter the DataFrame to include only rows within the last 5 minutes
        last_5_minutes_data_df = data_df[data_df['timestamp'] >= five_minutes_ago]
        last_5_minutes_data_df['timestamp'] = last_5_minutes_data_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        return last_5_minutes_data_df.to_json(orient='records')
    except Exception as e:
        return str(e), 500

@app.route('/flask/history', methods=['GET', 'POST'])
def history():
    try:
        data_dir = "data"
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        
        if request.method == 'POST':
            selected_csv_file = request.form.get('csv_file')

            if not selected_csv_file:
                return "Please select a CSV file.", 400

            csv_file_path = os.path.join("data", selected_csv_file)
            data_df = pd.read_csv(csv_file_path)
            filtered_data_df = data_df.iloc[::10]

            # Convert DataFrame to JSON
            data_json = filtered_data_df.to_json(orient='records')

            return render_template('show_data.html', data=data_json)

        return render_template('history.html', csv_files=csv_files)
    except Exception as e:
        return str(e), 500

@app.route('/flask', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
