# -*- encoding=utf-8 -*-
from os import path, devnull
from pocketsphinx.pocketsphinx import *

import speech_recognition as sr

# Configuracion del modelo en español de lenguaje

MODELDIR = path.join('model', 'spanish')

config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'voxforge'))
config.set_string('-lm', path.join(MODELDIR, 'palabras.lm'))
config.set_string('-dict', path.join(MODELDIR, 'pronunciacion.dict'))

config.set_string('-logfn', devnull)

decoder = Decoder(config)

def callback(recognizer, audio):
    print("/ Reconociendo...")

    raw_data = audio.get_raw_data(convert_rate=16000, convert_width=2)

    decoder.start_utt()
    decoder.process_raw(raw_data, False, True)
    decoder.end_utt()

    hypothesis = decoder.hyp()

    try:
        print("* Frase reconocida: {}".format(hypothesis.hypstr))
    except:
        print("! No se ha reconocido nada")

print("/ Creando un objeto de reconocimiento...")
recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.5    # tiempo minimo de espera sin hablar para procesar informacion
recognizer.phrase_threshold = 0.2   # tiempo minimo hablando para considerar que el audio incluye una frase
recognizer.energy_threshold = 500   # ruido minimo para empezar a grabar
recognizer.non_speaking_duration = 0.4 # tiempo sin hablar que dejamos antes y despues de la frase en el audio

try:
    print("/ Detectando microfono...")
    source = sr.Microphone()

    with source as s:
        print("/ Ajustando ruido de fondo...")
        recognizer.adjust_for_ambient_noise(s, duration=1)
        print("* Configurado a una ganancia de {}".format(recognizer.energy_threshold))

    print("/ Detectando frases...")
    stop_listen = recognizer.listen_in_background(source, callback)

    while True:
        pass
except KeyboardInterrupt:
    print("/ Cerrando programa...")
except Exception as err:
    print("! Error: {}".format(err))
