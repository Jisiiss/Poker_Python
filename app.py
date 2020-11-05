# imports
from flask import Flask, render_template, request, escape, session, redirect
from fonctions.tirage import HAND_NB, init_deck, multiple_tirage
from fonctions.score import get_coeff

# const
POST = 'POST'
GET = 'GET'

# app
app = Flask(__name__)
app.secret_key = "PokerOnline"


# routes
@app.route('/')
def home():
    return render_template(
        'index.html',
        quitter=session['quitter'] if 'quitter' in session else None
    )


@app.route('/reset', methods=[GET])
def reset():
    session.clear()
    return redirect("/", code=302)

@app.route('/regle', methods=[GET])
def regle():
    return render_template('regle.html')


@app.route('/first-tirage', methods=[GET])
@app.route('/second-tirage', methods=[GET])
def go_home():
    return redirect("/", code=302)


@app.route('/first-tirage', methods=[POST])
def first_tirage():
    # banroll check
    quitter = int(escape(request.form['quitter']))
    bet = int(escape(request.form['bet']))
    if not quitter or not bet or quitter < 0 or bet < 0:
        return render_template(
            'error.html',
            error="La banque et la mise sont requises."
        )
    if bet > quitter:
        return render_template(
            'error.html',
            error="La mise doit être inférieure a la banque."
        )
    session['quitter'] = quitter
    session['bet'] = bet
    # tirage
    hand, deck = multiple_tirage(init_deck(), cards=[])
    session['deck'] = deck
    return render_template('first-tirage.html', hand=hand)


@app.route('/second-tirage', methods=[POST])
def second_tirage():
    # get hand
    hand = []
    for key in request.form:
        hand.append(escape(key))
    # tirage
    hand, deck = multiple_tirage(session['deck'], HAND_NB - len(hand), hand)
    # second tirage
    coeff, score_text = get_coeff(hand)
    session['quitter'] = session['quitter'] - session['bet'] \
        + session['bet'] * coeff
    return render_template(
        'second-tirage.html',
        hand=hand,
        quitter=session['quitter'],
        bet=session['bet'],
        coeff=coeff,
        score_text=score_text
    )


# run debug
app.run(debug=True)
