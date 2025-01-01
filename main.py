import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import paho.mqtt.client as mqtt

global current_temperature, current_humidity, current_co2
current_temperature = "NaN"
current_humidity = "NaN"
current_co2 = "NaN"

mqttc = mqtt.Client()
mqttc.connect("mqtt.eclipseprojects.io", 1883, 60)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    mqttc.subscribe("ooffice/temperature")
    mqttc.subscribe("ooffice/humidity")
    mqttc.subscribe("ooffice/co2")

def on_message(client, userdata, msg):
    global current_temperature, current_humidity, current_co2
    if msg.topic == "ooffice/temperature":
        current_temperature = msg.payload.decode()
    elif msg.topic == "ooffice/humidity":
        current_humidity = msg.payload.decode()
    elif msg.topic == "ooffice/co2":
        current_co2 = msg.payload.decode()

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.loop_start()

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
app.title = "Office Monitor"

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Office Monitor", className="text-center my-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Temperature"),
            html.H4(id="temperature")
        ])), width=4),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Humidity"),
            html.H4(id="humidity")
        ])), width=4),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("CO2"),
            html.H4(id="co2")
        ])), width=4),
    ]),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,
        n_intervals=0
    )
])

@app.callback(
    Output("temperature", "children"),
    Output("humidity", "children"),
    Output("co2", "children"),
    Input("interval-component", "n_intervals")
)
def update_metrics(n):
    return f"{current_temperature}°C", f"{current_humidity}%", f"{current_co2}ppm"

if __name__ == "__main__":
    app.run_server(debug=True)