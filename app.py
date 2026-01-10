import pickle
from flask import Flask, request, app, jsonify, url_for, render_template
import numpy as np
import pandas as pd 

app = Flask(__name__)

# Load the model and scaler
model = pickle.load(open('models/regmodel.pkl', 'rb'))
scalar = pickle.load(open('models/scaling.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

# Keep your API route as is
@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    new_data = scalar.transform(np.array(list(data.values())).reshape(1,-1))
    output = model.predict(new_data)
    print(output[0])
    return jsonify(output[0])

# --- UPDATED PREDICT FUNCTION FOR DASHBOARD ---
@app.route('/predict', methods=['POST'])
def predict():
    # 1. Capture values from HTML form
    # Note: The order of inputs in HTML must match the order in feature_names below
    data = [float(x) for x in request.form.values()]
    
    # 2. Define the exact feature names used during training (excluding 'medv')
    feature_names = ['crim', 'zn', 'indus', 'chas', 'nox', 'rm', 'age', 
                     'dis', 'rad', 'tax', 'ptratio', 'b', 'lstat']
    
    # 3. Create a DataFrame
    # This gives the scaler the column names it expects, fixing the warning
    df_input = pd.DataFrame([data], columns=feature_names)
    
    # 4. Transform and Predict
    final_input = scalar.transform(df_input)
    output = model.predict(final_input)[0]
    
    # 5. Return JSON
    return jsonify({'price': round(output, 2)})
# ----------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)