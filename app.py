from flask import Flask, render_template, request
from gtts import gTTS
import os

app = Flask(__name__)
chemin_voix = os.path.join("static", "voix")

# 1. Descriptions vocales
descriptions = {
    "rouge":      ("le singe", "Rouge ! Voici le singe plein d'énergie qui grimpe partout avec joie."),
    "bleu":       ("le dauphin", "Bleu ! Voici le dauphin gentil et joueur qui nage dans les histoires."),
    "jaune":      ("le poussin", "Jaune ! Voilà le poussin joyeux qui aime chanter le matin."),
    "vert":       ("la grenouille", "Vert ! C’est la grenouille curieuse qui saute dans les découvertes."),
    "rose":       ("le chaton", "Rose ! C’est le petit chaton doux qui adore les câlins."),
    "orange":     ("le renard", "Orange ! C’est le renard malin qui apprend vite et aime jouer."),
    "violet":     ("le papillon", "Violet ! Le papillon calme qui aime les couleurs et la nature."),
    "blanc":      ("l’agneau", "Blanc ! L’agneau paisible qui partage et aime les histoires douces."),
    "noir":       ("le panda", "Noir ! Le panda calme qui observe le monde avec ses grands yeux."),
    "marron":     ("l’ours", "Marron ! Voici l’ours tendre qui aime se reposer et rêver tranquillement.")
}

# 2. Couleurs visuelles
couleur_styles = {
    "rouge": "#e74c3c",
    "bleu": "#3498db",
    "jaune": "#f1c40f",
    "vert": "#2ecc71",
    "rose": "#ff66cc",
    "orange": "#e67e22",
    "violet": "#9b59b6",
    "blanc": "#ecf0f1",
    "noir": "#2c3e50",
    "marron": "#8e5c42"
}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html",
                           couleurs=descriptions.keys(),
                           couleur_styles=couleur_styles,
                           fichier_audio=None)

@app.route("/voix", methods=["POST"])
def voix():
    couleur = request.form["couleur"]
    animal, phrase = descriptions.get(couleur, ("l'animal magique", "Cette couleur est spéciale comme toi."))
    nom_fichier = f"{couleur}.mp3"
    chemin_fichier = os.path.join(chemin_voix, nom_fichier)

    # Créer le dossier voix si besoin
    os.makedirs(chemin_voix, exist_ok=True)

    # Générer le fichier vocal si absent
    tts = gTTS(text=phrase, lang="fr")
    tts.save(chemin_fichier)

    return render_template("index.html",
                           couleurs=descriptions.keys(),
                           couleur_styles=couleur_styles,

                           fichier_audio=nom_fichier)




# Dictionnaire des scènes du jeu Coco
scenes = {
    "scene1": {
        "voix": "scene1.mp3",
        "texte": "Tu entres dans la Forêt des Couleurs. Un papillon violet vole autour de toi. Veux-tu le suivre ou t’asseoir sur une souche moelleuse ?",
        "choix": [("papillon", "Suivre le papillon"), ("souche", "S’asseoir sur la souche")]
    },
    "papillon": {
        "voix": "papillon.mp3",
        "texte": "Le papillon t’emmène vers une cascade arc-en-ciel qui chante doucement.",
        "choix": []
    },
    "souche": {
        "voix": "souche.mp3",
        "texte": "La souche se met à parler : 'Raconte-moi ta couleur préférée, petit aventurier !'",
        "choix": []
    }
}

def generer_voix_scene(scene_id):
    chemin_voix = os.path.join("static", "voix", scenes[scene_id]["voix"])
    if not os.path.exists(chemin_voix):
        tts = gTTS(text=scenes[scene_id]["texte"], lang="fr")
        tts.save(chemin_voix)



@app.route("/python-lecon/<numero>", methods=["GET", "POST"])
def lecon_python(numero):
    lecons = {
        "1": {
            "titre": "Afficher un message",
            "instruction": "Écris : print(\"Bonjour !\")",
            "attendu": "print(\"Bonjour !\")",
            "voix": "lecon1.mp3",
            "texte_voix": "En Python, pour afficher un message, on utilise la fonction print. Écris : print Bonjour entre guillemets."
        },
        "2": {
            "titre": "Compter avec Python",
            "instruction": "Écris : print(2 + 3)",
            "attendu": "print(2 + 3)",
            "voix": "lecon2.mp3",
            "texte_voix": "Voici comment faire une addition. Écris print, parenthèse, deux plus trois, parenthèse."
        },
        "3": {
            "titre": "Stocker un mot",
            "instruction": "Écris : nom = \"Lumi\"",
            "attendu": "nom = \"Lumi\"",
            "voix": "lecon3.mp3",
            "texte_voix": "Pour créer une variable, tu écris un nom, égal, et une valeur entre guillemets. Lumi est un joli prénom, non ?"
        }
    }

    if numero not in lecons:
        return "Leçon inconnue", 404

    lecon = lecons[numero]
    voix_path = os.path.join("static", "voix", lecon["voix"])
    if not os.path.exists(voix_path):
        gTTS(text=lecon["texte_voix"], lang="fr").save(voix_path)

    if request.method == "POST":
        code = request.form["code"].strip().lower()
        attendu = lecon["attendu"].strip().lower()
        juste = code == attendu.strip().lower()
        prochain = str(int(numero) + 1) if juste and str(int(numero) + 1) in lecons else None
        return render_template("lecon.html", lecon=lecon, numero=numero, code=code, juste=juste, prochain=prochain)

    return render_template("lecon.html", lecon=lecon, numero=numero, code="", juste=None, prochain=None)




from flask import Flask, render_template, request, session, redirect, url_for
from gtts import gTTS
import os
import re

app.secret_key = "clé_super_magique"
chemin_voix = os.path.join("static", "voix")
os.makedirs(chemin_voix, exist_ok=True)

etapes = {
    "1": {
        "instruction": "Écris : print(\"Papillon étoile\")",
        "solution": "print(\"Papillon étoile\")",
        "voix": "etape1.mp3",
        "intro": "Bienvenue jeune {genre}. Pour appeler le papillon étoile, écris print papillon étoile.",
        "suivant": "2"
    },
    "2": {
        "instruction": "Maintenant écris : print(\"Il brille en violet\")",
        "solution": "print(\"Il brille en violet\")",
        "voix": "etape2.mp3",
        "intro": "Magnifique ! Le papillon arrive. Pour continuer, écris : Il brille en violet.",
        "suivant": None
    }
}

def nettoyer(code):
    return re.sub(r'\s+', '', code.strip().lower().replace("’", "'").replace("“", "\"").replace("”", "\""))

def generer_voix(nom, texte):
    chemin = os.path.join(chemin_voix, nom)
    if not os.path.exists(chemin):
        gTTS(text=texte, lang="fr").save(chemin)

@app.route("/choisir-genre", methods=["GET", "POST"])
def choisir_genre():
    if request.method == "POST":
        session["genre"] = request.form["genre"]
        return redirect("/jeu")
    generer_voix("accueil.mp3", "Bonjour ! Es-tu un garçon ou une fille ?")
    return render_template("choix_genre.html")

@app.route("/jeu")
def debut_jeu():
    genre = session.get("genre", "aventurier")
    titre = "aventurière" if genre == "fille" else "aventurier"
    etape_id = "1"
    etape = etapes[etape_id]
    texte = etape["intro"].replace("{genre}", titre)
    generer_voix(etape["voix"], texte)
    return render_template("jeu.html", etape=etape_id, data=etape, code_accumule="", erreur=False)

@app.route("/valider", methods=["POST"])
def valider():
    etape_id = request.form["etape"]
    code = request.form["code"]
    code_accumule = request.form["code_accumule"]
    etape = etapes[etape_id]

    if nettoyer(code) == nettoyer(etape["solution"]):
        code_accumule += code + "\n"
        suivant = etape["suivant"]
        if suivant:
            nouvelle = etapes[suivant]
            generer_voix(nouvelle["voix"], nouvelle["intro"])
            return render_template("jeu.html", etape=suivant, data=nouvelle, code_accumule=code_accumule, erreur=False)
        else:
            felic = os.path.join(chemin_voix, "felicitation.mp3")
            if not os.path.exists(felic):
                gTTS("Bravo, tu as terminé ton aventure !", lang="fr").save(felic)
            return render_template("fin.html", code_accumule=code_accumule)
    else:
        encouragement = os.path.join(chemin_voix, "essaie.mp3")
        if not os.path.exists(encouragement):
            gTTS("Essaie encore, tu es tout proche !", lang="fr").save(encouragement)
        return render_template("jeu.html", etape=etape_id, data=etape, code_accumule=code_accumule, erreur=True)
    
if __name__ == "__main__":
    app.run(debug=True)
