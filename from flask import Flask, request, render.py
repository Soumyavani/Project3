from flask import Flask, request, render_template
from featureExtractor import featureExtraction
from pycaret.classification import load_model, predict_model

# Load the model
model_path = r'C:\Users\Lenovo\OneDrive\Desktop\ProjectMajo\model\phishingdetection'
try:
    model = load_model(model_path)
except FileNotFoundError:
    print(f"Error: Model file not found at {model_path}. Please check the file path and name.")
    raise

def predict(url):
    data = featureExtraction(url)
    result = predict_model(model, data=data)
    prediction_score = result['prediction_score'][0]  
    prediction_label = result['prediction_label'][0] 
    
    return {
        'prediction_label': prediction_label,
        'prediction_score': prediction_score * 100,
    }

# Initialize Flask app
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    url = None  # Initialize 'url' with a default value
    if request.method == "POST":
        url = request.form["url"]  # Assign 'url' only if the request is POST
        data = predict(url)
    return render_template(r'index (1).html', url=url, data=data)  # Ensure 'url' is always defined

if __name__ == "__main__":
    app.run(debug=True)
