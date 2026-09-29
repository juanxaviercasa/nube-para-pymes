txt = open("js/analizador-titulares.js", "r", encoding="utf-8").read()
import re
# look for Spanish text
spanish_samples = ["Motor analítico", "Escribe tu titular", "Puntuación general", "Huella emocional"]
for s in spanish_samples:
    print(f"'{s}' in JS bundle:", s in txt)
