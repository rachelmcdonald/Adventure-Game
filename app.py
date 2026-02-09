from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    scene_text = (
        "You stand at the edge of an ancient forest. "
        "Do you go left toward the glowing mushrooms, or right along the sparkling river?"
    )
    options = [
        ('left', 'Go left toward the glowing mushrooms'),
        ('right', 'Go right along the sparkling river')
    ]

    if request.method == 'POST':
        choice = request.form.get('choice')

        if choice == 'left':
            scene_text = (
                "You follow the soft glow of bioluminescent mushrooms. "
                "Fireflies drift lazily through the air."
            )
            options = [
                ('investigate', 'Investigate the humming'),
                ('continue', 'Continue down the mossy path')
            ]

        elif choice == 'right':
            scene_text = (
                "You walk beside the sparkling river. "
                "A rickety wooden bridge sways ahead."
            )
            options = [
                ('cross', 'Cross the bridge'),
                ('follow', 'Follow the riverbank')
            ]

    return render_template('game.html', scene=scene_text, options=options)


if __name__ == '__main__':
    app.run(debug=True)