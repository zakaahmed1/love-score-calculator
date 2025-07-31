import random
import statistics
from flask import Flask, render_template, request

app = Flask(__name__)

# Sample pool of names to simulate score distribution
sample_names = [
    "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank",
    "Isla", "Jack", "Karen", "Leo", "Mona", "Nate", "Olivia", "Paul",
    "Quincy", "Rita", "Steve", "Tina", "Uma", "Victor", "Wendy", "Xavier",
    "Yasmin", "Zack"
]

def calculate_love_score_raw(name1, name2):
    combined = (name1 + name2).lower()
    true_score = sum(combined.count(letter) for letter in "true")
    love_score = sum(combined.count(letter) for letter in "love")
    return int(f"{true_score}{love_score}")

def generate_score_distribution(n=10000):
    scores = []
    for _ in range(n):
        name1 = random.choice(sample_names)
        name2 = random.choice(sample_names)
        score = calculate_love_score_raw(name1, name2)
        scores.append(score)
    return scores

def get_statistics(scores):
    mean = statistics.mean(scores)
    stdev = statistics.stdev(scores)
    return mean, stdev

def interpret_score(score, mean, stdev):
    z = (score - mean) / stdev
    if z > 2:
        return "🔥 Perfect match!"
    elif z > 1.0:
        return "😊 Strong match!"
    elif z > 0:
        return "🙂 Decent match"
    elif z > -0.5:
        return "😐 Might need some work"
    else:
        return "💔 Not looking good..."

# Cache distribution at app startup
distribution = generate_score_distribution()
mean = statistics.mean(distribution)
stdev = statistics.stdev(distribution)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name1 = request.form['name1']
        name2 = request.form['name2']
        score = calculate_love_score_raw(name1, name2)
        interpretation = interpret_score(score, mean, stdev)
        result = {
            'name1': name1,
            'name2': name2,
            'score': score,
            'interpretation': interpretation
        }
        return render_template('index.html', result=result)
    
    # For GET requests, show page with no result
    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)
