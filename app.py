from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game', methods=['GET'])
def game():
    scene_text = "You approach a mystical forest. Do you go left towards the glowing mushrooms, or right along the sparkling river?"
    return render_template('game.html', scene=scene_text)

if __name__ == '__main__':
    app.run(debug=True)