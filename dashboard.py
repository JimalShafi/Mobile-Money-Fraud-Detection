# dashboard.py
import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import requests

# Initialize Dash app
app = dash.Dash(__name__)

# Dummy data for initial visualization (you can connect this to a real-time database or API)
fraud_data = pd.DataFrame({
    "Time": ["2024-12-26 10:00", "2024-12-26 10:05", "2024-12-26 10:10"],
    "Fraud_Label": [0, 1, 0],
    "Amount": [1000, 50000, 1200]
})

# Layout for the dashboard
app.layout = html.Div(children=[
    html.H1("Mobile Money Fraud Detection Dashboard", style={'text-align': 'center'}),
    
    # Graph showing fraud detection rates
    dcc.Graph(id='fraud-detection-rate', style={'width': '80%', 'margin': '0 auto'}),
    
    # Graph showing transaction amounts
    dcc.Graph(id='transaction-amounts', style={'width': '80%', 'margin': '0 auto'}),
    
    # Button to trigger fraud detection prediction (simulating real-time detection)
    html.Button("Simulate Fraud Detection", id='simulate-btn', n_clicks=0),
    
    # Store data for interactivity between callbacks
    dcc.Store(id='fraud-data', data=fraud_data.to_dict('records')),
])

# Callback to update graphs based on simulated fraud detection
@app.callback(
    [dash.dependencies.Output('fraud-detection-rate', 'figure'),
     dash.dependencies.Output('transaction-amounts', 'figure'),
     dash.dependencies.Output('fraud-data', 'data')],
    dash.dependencies.Input('simulate-btn', 'n_clicks'),
    dash.dependencies.State('fraud-data', 'data')
)
def update_dashboard(n_clicks, fraud_data):
    # Simulate new transaction data (in a real case, fetch it from your backend API)
    if n_clicks > 0:
        new_transaction = {
            "Time": "2024-12-26 10:15",
            "Fraud_Label": random.choice([0, 1]),
            "Amount": random.randint(1000, 100000)
        }
        fraud_data.append(new_transaction)

    # Prepare the data for visualization
    df = pd.DataFrame(fraud_data)

    # Calculate fraud detection rates
    fraud_rate = df['Fraud_Label'].mean()

    # Create the fraud detection rate graph
    fraud_rate_fig = {
        'data': [go.Bar(
            x=["Fraudulent", "Legitimate"],
            y=[df['Fraud_Label'].sum(), len(df) - df['Fraud_Label'].sum()],
            marker={'color': ['red', 'green']}
        )],
        'layout': go.Layout(title="Fraud Detection Rate", xaxis={'title': 'Transaction Type'}, yaxis={'title': 'Count'})
    }

    # Create the transaction amount graph
    amount_fig = {
        'data': [go.Box(
            y=df['Amount'],
            boxmean='sd',
            name="Transaction Amount",
            marker={'color': 'blue'}
        )],
        'layout': go.Layout(title="Transaction Amount Distribution", yaxis={'title': 'Amount'})
    }

    return fraud_rate_fig, amount_fig, fraud_data

if __name__ == '__main__':
    app.run_server(debug=True)
