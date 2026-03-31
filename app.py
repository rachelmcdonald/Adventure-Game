from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "mosslit-secret-key"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():

    if request.method == 'POST':
        choice = request.form.get('choice')

        if choice:
            session['scene'] = choice

        return redirect(url_for('game'))

    if 'gold' not in session:
        session['gold'] = 0
        session['xp'] = 0
        session['courage'] = 1
        session['blessing'] = False
        session['scene'] = 'start'
        session['wizard_interacted'] = False
        session['fairy_interacted'] = False
        session['fairy_mood'] = "neutral"
        

    scene = session.get('scene', 'start')
    scene_text = ""
    options = []

    if scene == 'start':
        session['class'] = 'elven_ranger'

        scene_text = (
            "You are Elven — a ranger of the wilds.\n\n"
            "You steady your breath as the forest watches.\n\n"
            "You stand at the edge of an ancient forest. "
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
            "The river whispers ancient songs. "
            "A moss-robed wizard stands before you, staff glowing softly.."
        )
        options = [
            ('wizard_talk', 'Speak respectfully to the wizard'),
            ('wizard_pass', 'Attempt to sneak past')
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
            "The fairy watches silently as you pass. "
            "The forest feels a little colder without her light."
        )
        options = [('werewolf', 'Continue quietly')]

    elif scene == 'wizard_talk':
        session['wizard_interacted'] = True
        session['came_from'] = 'wizard_talk'
        session['courage'] += 1
        session['gold'] +=1
        
        scene_text = (
            "The wizard nods slowly. "
            "He taps his staff, filling you with quiet strength."
        )
        options = [('continue', 'Continue along the glowing path')]

    elif scene == 'wizard_pass':
        session['wizard_interacted'] = True
        session['came_from'] = 'wizard_pass'
        session['courage'] -= 1
        
        scene_text = (
            "The wizard senses your hesitation. "
            "The forest grows colder around you."
        )
        options = [('continue', 'Push forward uneasily')]

    elif scene == 'werewolf':
        session['werewolf_max_hp'] = 5
        session['werewolf_hp'] = session.get('werewolf_hp', 5)

        scene_text = (
            "A feral werewolf leaps from the shadows! "
            "Its glowing eyes lock onto you."
        )
        options = [
            ('attack_werewolf', 'Attack the werewolf'),
            ('run', 'Try to escape')
        ]

    elif scene == 'attack_werewolf':
        session['werewolf_hp'] -= 1
        session['just_hit'] = True

        if session['werewolf_hp'] <= 0:
            session['gold'] += 2
            session['xp'] += 3
            session.pop('entered_werewolf', None)
            session.pop('werewolf_hp', None)
            session.pop('just_hit', None)
            session['scene'] = 'werewolf_defeated'

            return redirect(url_for('game'))
        else:
            scene_text = (
                f"You strike the werewolf! "
                f"It still has {session['werewolf_hp']} HP."
            )
            options = [('attack_werewolf', 'Attack again'),
                        ('run', 'Attempt to escape')
            ]

    elif scene == 'werewolf_defeated': 
        scene_text = ( 
            "The werewolf collapses into the moss. " "Its glowing eyes fade into darkness." 
        ) 
        options = [('continue', 'Continue down the path')]

    elif scene == 'run':
        session['courage'] -= 1
        session.pop('came_from', None)

        scene_text = (
            "You flee through the dark forest, the werewolf's howl fading behind you."
            "\n\nYou escape… but the forest feels heavier now."
        )

        options = [('continue', 'Keep moving')]

    elif scene == 'troll':
        session['player_hp'] = session.get('player_hp', 10)
        session['player_max_hp'] = session.get('player_max_hp', 10)
        session['troll_max_hp'] = 6
        session['troll_hp'] = 6

        scene_text = (
            "A massive troll blocks your path! "
            "It grips a crude club and snarls."
        )

        options = [
            ('attack_troll', 'Attack the troll'),
            ('run_troll', 'Try to escape')
        ]

    elif scene == 'attack_troll':
        session['player_hp'] = session.get('player_hp', 10)
        session['player_max_hp'] = session.get('player_max_hp', 10)
        session['troll_hp'] -= 1
        session['player_hp'] -= 2
        session['just_hit'] = True

        if session['player_hp'] <= 0:
            scene_text = (
                "The troll's club crashes down.\n\n"
                "Everything fades to black...\n\n"
                "💀 You were defeated."
            )
            options = [('restart', 'Try again')]
            return render_template(
                'game.html', 
                scene_text=scene_text, 
                scene_name=scene, 
                options=options
            )

        if session['troll_hp'] <= 0:
            session['gold'] += 3
            session['xp'] += 4

            session.pop('troll_hp', None)
            session.pop('just_hit', None)

            session['scene'] = 'troll_defeated'
            return redirect(url_for('game'))

        scene_text = (
            f"You strike the troll! "
            f"It still has {session['troll_hp']} HP."
        )

        options = [
            ('attack_troll', 'Attack again'),
            ('run_troll', 'Attempt to escape')
        ]

    elif scene == 'troll_defeated':
        session['troll_defeated'] = True
        session.pop('troll_hp', None)
        session.pop('escaped_troll', None)
        scene_text = (
            "The troll collapses with a heavy thud. "
            "The path is clear once more."
        )

        options = [('continue', 'Continue forward')]

    elif scene == 'run_troll':
        session['courage'] -= 1
        session['escaped_troll'] = True
        session.pop('came_from', None)

        scene_text = (
            "You scramble away as the troll bellows behind you. "
            "Each step shakes the ground beneath your feet...\n\n"
            "You escape... but your nerves are rattled."
        )

        options = [('continue', 'Keep moving')]

    elif scene == 'continue':

        if (
            session.get('came_from') == 'wizard_pass'
            and not session.get('troll_defeated')
            and not session.get('escaped_troll')
        ):
            session.pop('came_from', None)
            session['scene'] = 'troll'
            return redirect(url_for('game'))
        
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
                "Fireflies dance as dawn breaks.\n\n"
                "🌿 Adventure Complete\n\n"
                f"⭐ XP Earned: {session['xp']}\n"
                f"🪙 Gold Collected: {session['gold']}\n"
                f"🌱 Courage Remaining: {session['courage']}\n\n"
                "Ending: Mosslit Wanderer"
            )
            options = [('restart', 'Play again')]

    elif scene == 'restart':
        session.clear()
        session['player_max_hp'] = 10
        session['player_hp'] = 10
        return redirect(url_for('game'))

    else:
        scene_text = "The forest grows quiet... too quiet."
        options = [('restart', 'Begin again')]

    return render_template('game.html', scene_text=scene_text, scene_name=scene, options=options, just_hit=session.pop('just_hit', False))


if __name__ == '__main__':
    app.run(debug=True)