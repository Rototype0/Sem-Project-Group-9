from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt

app = Flask(__name__)

# Example data from database
desk_activity = {
    "up": [0.5],  # Hours standing up
    "down": [1, 1, 1, 1, 1],  # Hours sitting down
}

# Function to generate health tips
def generate_health_tips(age, activity):
    standing_hours = len(activity["up"])
    sitting_hours = len(activity["down"])

    if standing_hours >= 2:
        return "Great job maintaining your activity! Aim for 2-4 hours standing daily."
    else:
        return "Consider standing more often during work, for at least 2 hours a day."

# Route for health tips generation
@app.route("/generate-tips", methods=["POST"])
def generate_tips():
    age = int(request.form.get("age"))
    tips = generate_health_tips(age, desk_activity)
    return jsonify({"tips": tips})

# Route for rendering chart and input form
@app.route("/")
def index():
    # Generate the bar chart using Matplotlib
    labels = ["8 AM", "10 AM", "12 PM", "2 PM", "4 PM"]
    up_data = desk_activity["up"] + [0] * (len(labels) - len(desk_activity["up"]))
    down_data = desk_activity["down"]

    fig, ax = plt.subplots()
    bar_width = 0.35
    x = range(len(labels))
    ax.bar(x, up_data, bar_width, label="Standing (Up)", color="rgba(75, 192, 192, 0.6)")
    ax.bar(x, down_data, bar_width, bottom=up_data, label="Sitting (Down)", color="rgba(255, 99, 132, 0.6)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    # Save the chart as an image
    plt.savefig("static/activity_chart.png")
    plt.close()

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
