from flask import Flask, jsonify, request, render_template
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification
import librosa
from librosa import get_duration
import torch
from pydub.utils import make_chunks
from pydub import AudioSegment
from math import exp
from werkzeug.utils import secure_filename
import os

model = AutoModelForAudioClassification.from_pretrained(r'/Users/amrsamer/Desktop/Senior/Superb-W2V2-large-ic-AC-8h-final5')
feature_extractor = AutoFeatureExtractor.from_pretrained('superb/wav2vec2-large-superb-ic')

def prediction_model(audio, top_k=3):

    dialects = ['Algeria','Bahrain','Egypt','Iraq','Jordan','Saudi Arabia','Kuwait','Lebanon','Libya','Mauritania',
             'Morocco','Oman','Palestine','Qatar','Sudan','Syria','Tunisia','United Arab Emirates','Yemen']

    speech, _ = librosa.load(audio, sr=16000, mono=True)
    input = feature_extractor(speech, sampling_rate=16000, padding='max_length', max_length=160000, return_tensors="pt")
    logits = model(**input).logits[0][:19]
    predicted_ids = torch.topk(logits, top_k, dim=-1).indices.squeeze()

    print(logits)

    maximum = max(logits)
    minimum = min(logits)

    confidence_rates = []
    for i in logits:
        rate = 1/(1+exp(-i/((maximum-minimum)) * 4))
        confidence_rates.append(rate)

    minimum2 = min(confidence_rates)
    for i in range(len(confidence_rates)):
        confidence_rates[i] -= minimum2*0.8

    maximum2 = max(confidence_rates)
    for i in range(len(confidence_rates)):
        confidence_rates[i] /= maximum2

    predicted_labels = []
    for i in predicted_ids:
        predicted_labels.append(dialects[i])

    output = {}

    for i,dialect in enumerate(predicted_labels):
        output[dialect] = confidence_rates[predicted_ids[i]]

    return output

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'mp3','wav','mp4'}


senior_app = Flask(__name__)
senior_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@senior_app.route("/")
def main():
    return render_template('index.html')

def convert_to_wav(audio_path):
    sound = AudioSegment.from_file(audio_path)
    wav_path = audio_path.rsplit('.', 1)[0] + '.wav'
    sound.export(wav_path, format='wav')
    return wav_path

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@senior_app.route("/predict", methods=["POST"])
def predictions():
    print(request.files)
    if 'audiofile' not in request.files:
        return jsonify(msg="No file part"), 400
    file = request.files['audiofile']
    
    if file.filename == '':
        return jsonify(msg="No selected file"), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(senior_app.config['UPLOAD_FOLDER'], filename))

        filename = 'static//' + filename

        if not filename.lower().endswith('.wav'):
            new_file_path = convert_to_wav(filename)
            results = prediction_model(new_file_path)
            os.remove(new_file_path)  
            os.remove(filename)
        else:
            results = prediction_model(filename)
            os.remove(filename)

        return jsonify(results)

print(senior_app.url_map)

if __name__ == "__main__":
    senior_app.run(host="0.0.0.0", port=8500)
