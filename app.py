from flask import Flask, request, render_template, send_file, jsonify
from gtts import gTTS
from pydub import AudioSegment
import random
from pydub.effects import compress_dynamic_range

app = Flask(__name__)


# Define a route to display the form
@app.route('/')
def home():
    return render_template('index.html')


# Define a route to handle speech processing
@app.route('/generate-speech', methods=['POST'])
def generate_speech():
    try:
        # Get the text from the form data
        text = request.form.get('text')

        # Check if text is provided
        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Process the text to generate speech
        audio_file_path = create_natural_speech(text)

        # Send the generated audio file as a response
        return send_file(audio_file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def create_natural_speech(text):
    sentences = text.split('. ')
    final_audio = AudioSegment.empty()

    breath_sound_path = "breath.mp3"

    for sentence in sentences:
        tts = gTTS(text=sentence, lang='en')
        tts.save("temp_sentence.mp3")
        sentence_audio = AudioSegment.from_mp3("temp_sentence.mp3")
        sentence_audio = compress_dynamic_range(sentence_audio, threshold=-10.0, ratio=2.0, attack=5, release=50)

        pause_duration = 400 if sentence.endswith(".") else 250
        silence = AudioSegment.silent(duration=pause_duration)

        final_audio += sentence_audio + silence

        if random.random() < 0.4:
            try:
                breath_sound = AudioSegment.from_mp3(breath_sound_path)
                final_audio += breath_sound
            except FileNotFoundError:
                print("Breath sound file not found. Skipping breathing effect.")

    final_audio = final_audio._spawn(final_audio.raw_data, overrides={"frame_rate": int(final_audio.frame_rate * 1.1)})

    output_file_path = "generated_speech.mp3"
    final_audio.export(output_file_path, format="mp3")
    return output_file_path


if __name__ == '__main__':
    app.run(debug=True)
