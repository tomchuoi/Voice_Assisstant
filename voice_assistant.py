import openai
import pyttsx3
import speech_recognition as sr

openai.api_key = "ENTER YOUR API HERE"

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def transcribe_audio(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Unknown error occurred")

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        temperature=0.5,
        max_tokens=4000,
        prompt=prompt,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    # Wait for user to say "hello"
    print("Say 'hello' to start recording the question...")

    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        audio = recognizer.listen(source, phrase_time_limit=3, timeout=3)

        try:
            transcription = recognizer.recognize_google(audio)

            # Check if the user said "hello"
            if transcription.lower() == "hello":
                print("Listening...")

                # Record audio
                with sr.Microphone() as source:
                    recognizer = sr.Recognizer()
                    audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)

                    # Save audio to file
                    filename = "input.wav"
                    with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())

                # Transcribe the audio to text
                text = transcribe_audio(filename)
                if text:
                    print(text)
                    response = generate_response(text)
                    print("Assistant:", response)

                    # Read the response
                    speak_text(response)

        except Exception as e:
            print("An error occurred:", e)


if __name__ == "__main__":
    main()
