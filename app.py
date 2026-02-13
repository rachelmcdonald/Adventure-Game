from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "mosslit-secret-key"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'gold' not in session:
        session['gold'] = 0
        session['courage'] = 1
        session['blessing'] = False
        session['scene'] = 'start'

    if 'fairy_interacted' not in session:
        session['fairy_interacted'] = False   

    if 'fairy_mood' not in session:
        session['fairy_mood'] = "neutral"
    
    scene = session['scene']
    scene_text = ""
    options = []

    if scene == 'start':
        scene_text = (
            "You stand at the edge of an ancient forest. "
            "Moonlight glimmers on moss-covered roots."
        )
        options = [
            ('left', 'Go left toward the glowing mushrooms'),
            ('right', 'Go right along the sparkling river')
        ]

    elif scene == 'left':
        scene_text = (
            "Bioluminescent mushrooms hum softly. "
            "A tiny forest fairy floats into view."
        )
        options = [
            ('fairy_help', 'Greet the fairy politely'),
            ('fairy_ignore', 'Ignore the fairy and move on')
        ]

    elif scene == 'right':
        scene_text = (
            "The river whispers ancient songs."
            "A moss-robed wizard blocks the path."
        )
        options = [
            ('wizard_talk', 'Speak with the wizard'),
            ('wizard_pass', 'Try to pass quietly')
        ]

    elif scene == 'fairy_help':
        session['gold'] += 1
        session['blessing'] = True
        session['fairy_interacted'] = True
        session['fairy_mood'] = "happy"

        scene_text = (
            "The fairy smiles warmly and sprinkles glowing spores over you. "
            "You feel a gentle protective magic surround you."
        )
        options = [('continue', 'Thank her and continue')]

    elif scene == 'fairy_ignore':
        session['courage'] -= 1
        session['fairy_interacted'] = True
        session['fairy_mood'] = "angry"

        scene_text = (
            "The fairy watches silently as you pass."
            "The forest feels a little colder without her light."
        )
        options = [('continue', 'Continue quietly')]

    elif scene == 'wizard_talk':
        session['courage'] += 1
        scene_text = (
            "The wizard nods approvingly at your bravery "
            "and allows you safe passage."
        )
        options = [('continue', 'Proceed down the path')]

    elif scene == 'wizard_pass':
        session['courage'] -= 1
        scene_text = (
            "The wizard frowns. The path twists unnaturally around you."
        )
        options = [('continue', 'Push forward anyway')]

    elif scene == 'continue':
        if session['courage'] <= 0:
            scene_text = (
                "The forest overwhelms you. "
                "You curl beneath the moss and drift into sleep."
                "\n\n🌑 Bad Ending"
            )
            options = [('restart', 'Begin again')]
        else:
            scene_text = (
                "You emerge into a mosslit clearing. "
                "Fireflies dance as dawn breaks."
                "\n\n🌿 Cozy Ending — You Win"
            )
            options = [('restart', 'Play again')]

    elif scene == 'restart':
        session.clear()
        return redirect(url_for('game'))

    if request.method == 'POST':
        choice = request.form.get('choice')
        session['scene'] = choice
        return redirect(url_for('game'))

    return render_template('game.html', scene=scene_text, options=options)


if __name__ == '__main__':
    app.run(debug=True)