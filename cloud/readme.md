# Flask App

```
from flask import Flask, request, jsonify, render_template
import pandas as pd
from datetime import datetime  # Import the datetime module

app = Flask(__name__)

# Create an empty DataFrame to store the data
data_df = pd.DataFrame(columns=['timestamp', 'data'])

@app.route('/flask/rec', methods=['POST'])
def receive_data():
    try:
        global data_df
        print("Received data")
        received_data = request.form.get('data')  # Assuming the ESP32 sends the data as a form field named 'data'

        # Create a timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data_to_append = {'timestamp': timestamp, 'data': received_data}
        data_df = data_df.append(data_to_append, ignore_index=True)  # Append the received data with timestamp to the DataFrame
        print(f"Received data: {received_data}")
        return "Data received successfully", 200
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return str(e), 500

@app.route('/flask/get', methods=['GET'])
def get_data():
    try:
        global data_df
        return data_df.to_json(orient='records')  # Convert the DataFrame to JSON and return it
    except Exception as e:
        return str(e), 500

@app.route('/flask', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

```

## index.html

```
<!DOCTYPE html>
<html>
<head>
    <title>Received Data</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <!-- Add a div for the Plotly chart with a range slider -->
    <div id="data-plot"></div>

    <!-- Add a button to pause/continue data fetching -->
    <button id="pause-button" onclick="toggleFetching()">Pause</button>

    <script>
        let jsonData = []; // Store all received data
        let isFetching = true; // Flag to track whether fetching is active or paused
        let fetchInterval;

        // Function to create and update the Plotly chart with a range slider
        function updatePlot(data) {
            jsonData = JSON.parse(data);

            // Extract timestamps and data values
            const timestamps = jsonData.map(entry => entry.timestamp);
            const dataValues = jsonData.map(entry => entry.data);

            // Create a trace for the data
            const trace = {
                x: timestamps,
                y: dataValues,
                mode: 'lines',
                type: 'scatter',
                line: { color: 'blue', width: 2 },
            };

            // Create a layout with a range slider
            const layout = {
                title: 'Data vs. Timestamp',
                xaxis: {
                    title: 'Timestamp',
                    type: 'date',
                    rangeslider: {},
                },
                yaxis: {
                    title: 'Data',
                },
            };

            // Create or update the Plotly chart
            Plotly.newPlot('data-plot', [trace], layout);
        }

        // Function to toggle data fetching pause/continue
        function toggleFetching() {
            isFetching = !isFetching;

            const pauseButton = document.getElementById('pause-button');
            if (isFetching) {
                pauseButton.innerText = 'Pause';
                fetchInterval = setInterval(fetchData, 5000); // Continue fetching
            } else {
                pauseButton.innerText = 'Continue';
                clearInterval(fetchInterval); // Pause fetching
            }
        }

        // Function to fetch data from Flask app
        function fetchData() {
            fetch('/flask/get')
                .then(response => response.text())
                .then(data => {
                    // Update the Plotly chart with a range slider
                    updatePlot(data);
                })
                .catch(error => console.error('Error fetching data:', error));
        }

        // Fetch data initially when the page loads
        fetchData();

        // Start fetching data initially
        fetchInterval = setInterval(fetchData, 5000); // Update every 5 seconds
    </script>
</body>
</html>

```

# Simulation App

```
import requests
import random
import time

# Define the URL where you want to send the POST request
url = 'http://10.0.0.106:5000/flask/rec'

# Iterate 10,000 times
for _ in range(10000):
    # Generate a new random number
    random_number = random.randint(1, 100)
    
    # Define the data to send in the POST request
    data_to_send = {'data': str(random_number)}
    
    try:
        # Send the POST request
        response = requests.post(url, data=data_to_send)

        # Check the response
        if response.status_code == 200:
            print(f'POST request with data {random_number} was successful!')
            print('Response content:')
            print(response.text)
        else:
            print(f'POST request with data {random_number} failed with status code:', response.status_code)

    except Exception as e:
        print('An error occurred:', str(e))
    
    # Wait for 1 second before the next iteration
    time.sleep(1)

```

# Esp32 code to cloud

```
/*
  Connect ESP32 to AskSensors
 * Description:  This sketch connects to a website (https://asksensors.com) using an ESP32 Wifi module.
 *  Author: https://asksensors.com, 2018
 *  github: https://github.com/asksensors
 */
 
#include <WiFi.h>
#include <WiFiMulti.h>
#include <HTTPClient.h>

WiFiMulti WiFiMulti;
HTTPClient ask;
// TODO: user config
const char* ssid     = "xxx"; //Wifi SSID
const char* password = "xxx"; //Wifi Password
const char* serverUrl = "http://34.29.140.126/flask/rec";
const unsigned int writeInterval = 25000;   // write interval (in ms)

// ASKSENSORS API host config
//const char* host = "api.asksensors.com";  // API host name
//const int httpPort = 80;      // port
  
void setup(){
  
  // open serial
  Serial.begin(115200);
  Serial.println("*****************************************************");
  Serial.println("********** Program Start : Connect ESP32 to AskSensors.");
  Serial.println("Wait for WiFi... ");

  // connecting to the WiFi network
  WiFiMulti.addAP(ssid, password);
  while (WiFiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  // connected
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


void loop() {
    // Generate a random number between 10 and 100
    int randomValue = random(10, 101); // Generates a value between 10 (inclusive) and 101 (exclusive)
    String dataToSend = "Random Value: " + String(randomValue);

    // Send POST request to Flask server
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    int httpResponseCode = http.POST("data=" + dataToSend);

    if (httpResponseCode > 0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
    } else {
        Serial.print("Error sending POST request!");
    }

    http.end();

    delay(5000); // Send data every 5 seconds
}


```

# ESP32 Debug code

## Send to ask sensors

```
/*
  Connect ESP32 to AskSensors
 * Description:  This sketch connects to a website (https://asksensors.com) using an ESP32 Wifi module.
 *  Author: https://asksensors.com, 2018
 *  github: https://github.com/asksensors
 */
 
#include <WiFi.h>
#include <WiFiMulti.h>
#include <HTTPClient.h>

WiFiMulti WiFiMulti;
HTTPClient ask;
// TODO: user config
const char* ssid     = "xx"; //Wifi SSID
const char* password = "xx"; //Wifi Password
const char* apiKeyIn = "xx";      // API KEY IN
const unsigned int writeInterval = 25000;   // write interval (in ms)

// ASKSENSORS API host config
const char* host = "api.asksensors.com";  // API host name
const int httpPort = 80;      // port
  
void setup(){
  
  // open serial
  Serial.begin(115200);
  Serial.println("*****************************************************");
  Serial.println("********** Program Start : Connect ESP32 to AskSensors.");
  Serial.println("Wait for WiFi... ");

  // connecting to the WiFi network
  WiFiMulti.addAP(ssid, password);
  while (WiFiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  // connected
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


void loop(){

  // Use WiFiClient class to create TCP connections
  WiFiClient client;


  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }else {

    // Create a URL for updating module1 and module 2
  String url = "http://api.asksensors.com/write/";
  url += apiKeyIn;
  url += "?module1=";
  url += random(10, 100);
  url += "&module2=";
  url += random(10, 100);
    
  Serial.print("********** requesting URL: ");
  Serial.println(url);
   // send data 
   ask.begin(url); //Specify the URL
  
    //Check for the returning code
    int httpCode = ask.GET();          
 
    if (httpCode > 0) { 
 
        String payload = ask.getString();
        Serial.println(httpCode);
        Serial.println(payload);
      } else {
      Serial.println("Error on HTTP request");
    }
 
    ask.end(); //End 
    Serial.println("********** End ");
    Serial.println("*****************************************************");

  }

  client.stop();  // stop client
  
  delay(writeInterval);    // delay
}


```

## Webserver Connect to Wifi (not working)

```
#include <WiFi.h>

// Access Point (AP) credentials
const char* ssid = "MyESP32AP";
const char* password = "MyPassword";
IPAddress staticIP(192, 168, 4, 1); // Set your desired static IP address
IPAddress gateway(192, 168, 4, 1);
IPAddress subnet(255, 255, 255, 0);

// Create an instance of the server
WiFiServer server(80);

// Store the selected Wi-Fi credentials
String selectedSSID;
String selectedPassword;
bool connecting = false;

void setup() {
  // Start serial communication for debugging
  Serial.begin(115200);

  // Create an Access Point
  WiFi.softAP(ssid, password);
  WiFi.softAPConfig(staticIP, gateway, subnet); // Set the static IP configuration

  Serial.println("Access Point created");
  Serial.print("AP IP address: ");
  Serial.println(WiFi.softAPIP());

  // Start the server
  server.begin();
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    Serial.println("New client connected");
    String response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n";
    response += "<html><body>";
    response += "<h1>Hello, World!</h1>";

    if (connecting) {
      response += "<p>Connecting to ";
      response += selectedSSID;
      response += "...</p>";
    } else if (client.available()) {
      String request = client.readStringUntil('\r');
      if (request.indexOf("GET /scan") != -1) {
        response += "<h2>Available Wi-Fi Networks:</h2>";
        scanAndDisplayNetworks(response);
        response += "<form action=\"/\" method=\"get\"><input type=\"submit\" value=\"Back\"></form>";
      } else if (request.indexOf("POST /connect") != -1) {
        selectedSSID = client.readStringUntil('&');
        selectedSSID = selectedSSID.substring(selectedSSID.indexOf('=') + 1);
        selectedPassword = client.readStringUntil('\r');
        selectedPassword = selectedPassword.substring(selectedPassword.indexOf('=') + 1);
        connecting = true;
        connectToWiFi();
        response += "<p>Connection in progress...</p>";
      } else {
        response += "<form action=\"/scan\" method=\"get\"><input type=\"submit\" value=\"Scan Wi-Fi Networks\"></form>";
      }
    } else {
      response += "<form action=\"/scan\" method=\"get\"><input type=\"submit\" value=\"Scan Wi-Fi Networks\"></form>";
    }

    response += "</body></html>";
    client.print(response);
    delay(1);
    client.stop();
    Serial.println("Client disconnected");
  }
}

void scanAndDisplayNetworks(String& response) {
  int numNetworks = WiFi.scanNetworks();
  response += "<form action=\"/connect\" method=\"post\">";
  for (int i = 0; i < numNetworks; i++) {
    response += "<input type=\"radio\" name=\"ssid\" value=\"";
    response += WiFi.SSID(i);
    response += "\"> ";
    response += WiFi.SSID(i);
    response += " (Signal: ";
    response += WiFi.RSSI(i);
    response += " dBm)<br>";
  }
  response += "<input type=\"text\" name=\"password\" placeholder=\"Enter Password\"><br>";
  response += "<input type=\"submit\" value=\"Connect\"></form>";
}

void connectToWiFi() {
  Serial.print("Connecting to Wi-Fi...");
  Serial.print("SSID: ");
  Serial.println(selectedSSID);
  Serial.print("Password: ");
  Serial.println(selectedPassword);
  
  WiFi.begin(selectedSSID.c_str(), selectedPassword.c_str());
  
  int retries = 0;
  while (WiFi.status() != WL_CONNECTED && retries < 5) {
    delay(1000);
    Serial.print(".");
    retries++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected to WiFi");
  } else {
    Serial.println("\nConnection failed. Check SSID and password.");
    connecting = false;
  }
}

```
