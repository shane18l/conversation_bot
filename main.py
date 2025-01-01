from groq import Groq
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

client = Groq(api_key="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")

recognizer = sr.Recognizer()

# Use microphone as the audio source
def user_input():
    with sr.Microphone() as source:
        print("Speak now...")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        # Capture the audio
        audio = recognizer.listen(source, timeout=5)

    try:
        # Convert speech to text
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        return "Fail!!"

def bot_response(text, context):
    context.append(f"User: {text}")
    context_str = ''.join(context)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": context_str
            },
            {
                "role": "user",
                "content": text,
            }
        ],
        model="llama3-8b-8192",
        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic
        # and repetitive.
        temperature=0.5,
        max_tokens=50,

        # Controls diversity via nucleus sampling: 0.5 means half of all
        # likelihood-weighted options are considered.
        top_p=1,

        # A stop sequence is a predefined or user-specified text string that
        # signals an AI to stop generating content, ensuring its responses
        # remain focused and concise. Examples include punctuation marks and
        # markers like "[end]".
        stop=".",

        # If set, partial message deltas will be sent.
        stream=False,
    )
    bot_text = chat_completion.choices[0].message.content
    context.append(f"Bot: {bot_text}")

    tts = gTTS(text=bot_text, lang="en", slow=False)
    tts.save("output.mp3")
    playsound("output.mp3")

context = ["""You are going to have a conversation with the user. Try to simulate a
           real conversation, so keep responses to around 10 seconds."""]

print("Give me a scenario, and we can have a conversation")
bot_settings = user_input()
context.append(bot_settings)

while True:
    user_text = user_input()
    if user_text: 
        bot_response(user_text, context)
    elif user_text == "Fail!!":
        tts = gTTS(text = "The request to the API failed. Please try again.")
        tts.save("output.mp3")
        playsound("output.mp3")
    else:
        tts = gTTS(text = "Have a good day!")
        tts.save("output.mp3")
        playsound("output.mp3")
        break

