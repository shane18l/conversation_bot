from groq import Groq
import speech_recognition as sr

client = Groq(api_key="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")

recognizer = sr.Recognizer()

# Use microphone as the audio source
with sr.Microphone() as source:
    print("Speak now...")
    # Adjust for ambient noise
    recognizer.adjust_for_ambient_noise(source)
    # Capture the audio
    audio = recognizer.listen(source)

try:
    # Convert speech to text
    text = recognizer.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Sorry, I could not understand the audio.")
except sr.RequestError as e:
    print(f"Could not request results; {e}")

chat_completion = client.chat.completions.create(
    #
    # Required parameters
    #
    messages=[
        # Set an optional system message. This sets the behavior of the
        # assistant and can be used to provide specific instructions for
        # how it should behave throughout the conversation.
        {
            "role": "system",
            "content": "you are a helpful assistant."
        },
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            "content": text,
        }
    ],

    # The language model which will generate the completion.
    model="llama3-8b-8192",

    #
    # Optional parameters
    #

    # Controls randomness: lowering results in less random completions.
    # As the temperature approaches zero, the model will become deterministic
    # and repetitive.
    temperature=0.5,

    # The maximum number of tokens to generate. Requests can use up to
    # 32,768 tokens shared between prompt and completion.
    max_tokens=1024,

    # Controls diversity via nucleus sampling: 0.5 means half of all
    # likelihood-weighted options are considered.
    top_p=1,

    # A stop sequence is a predefined or user-specified text string that
    # signals an AI to stop generating content, ensuring its responses
    # remain focused and concise. Examples include punctuation marks and
    # markers like "[end]".
    stop=None,

    # If set, partial message deltas will be sent.
    stream=False,
)



import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()


# Convert text to speech
engine.say(chat_completion.choices[0].message.content)

# Wait for the speaking to finish
engine.runAndWait()