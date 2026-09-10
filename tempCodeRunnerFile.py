import os
import numpy as np
from flask import Flask, request, render_template
import pickle

app = Flask(__name__, template_folder="./templates")

# paths to include the subfolder
model_path = r"C:\Users\sa\OneDrive\Desktop\Feild project\Placement_Prediction_Using_Machine-Learning\model.pkl"
model1_path = r"C:\Users\sa\OneDrive\Desktop\Feild project\Placement_Prediction_Using_Machine-Learning\model1.pkl"

# Check if files exist and load models
if os.path.exists(model_path) and os.path.exists(model1_path):
    model = pickle.load(open(model_path, 'rb'))
    model1 = pickle.load(open(model1_path, 'rb'))
else:
    raise FileNotFoundError("model.pkl or model1.pkl not found. Please check the file path and location.")

@app.route('/')
def h():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict():
    cgpa = request.args.get('cgpa', '0')
    projects = request.args.get('projects', '0')
    workshops = request.args.get('workshops', '0')
    mini_projects = request.args.get('mini_projects', '0')
    skills = request.args.get('skills', '')
    communication_skills = request.args.get('communication_skills', '0')
    internship = request.args.get('internship', '0')
    hackathon = request.args.get('hackathon', '0')
    tw_percentage = request.args.get('tw_percentage', '0')
    te_percentage = request.args.get('te_percentage', '0')
    backlogs = request.args.get('backlogs', '0')
    name = request.args.get('name', 'Candidate')

    # Count the number of skills by splitting with commas
    s = len(skills.split(',')) if skills else 1

    # Prepare the input array
    arr = np.array([cgpa, projects, workshops, mini_projects, s, communication_skills, internship, hackathon, tw_percentage, te_percentage, backlogs], dtype=float)
    output = model.predict([arr])[0]

    # Determine placement outcome
    p = '1' if output == 'Placed' else '0'

    # Prepare the salary prediction input array
    arr1 = np.array([cgpa, projects, workshops, mini_projects, s, communication_skills, internship, hackathon, tw_percentage, te_percentage, backlogs, p], dtype=float)
    salary = model1.predict([arr1])[0]
    
    # Format salary output
    salary_formatted = f"{int(salary):,}"

    if output == 'Placed':
        out = f'Congratulations {name} !! You have high chances of getting placed!!!'
        out2 = f'Your Expected Salary will be INR {salary_formatted} per annum'
    else:
        out = f'Sorry {name} !! You have low chances of getting placed. All the best!!!!'
        out2 = 'Improve your skills...'
    
    return render_template('output.html', output=out, output2=out2)

if __name__ == "__main__":
    app.run(debug=True)
