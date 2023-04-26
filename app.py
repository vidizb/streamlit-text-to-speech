import streamlit as st
import os
import time
import glob
import os
import openai
from streamlit_chat import message


from gtts import gTTS
from googletrans import Translator

try:
    os.mkdir("temp")
except:
    pass
st.title("Text to speech")
translator = Translator()
input_text = st.text_input("Pertanyaan : ","", key="input")
openai.api_key = st.secrets["model"]

def generate_response(prompt):
	completions = openai.Completion.create(
		engine = "text-davinci-003", # Untuk menggunakan model 
		prompt = prompt,             # Untuk menghasilkan teks 
		max_tokens = 1024,           # Jumlah maksimum token (kata dan tanda baca)
		n = 1,                       # Jumlah tanggapan
		stop = None,                 # Untuk berhenti menghasilkan teks
		temperature = 0.5,           # Untuk mengontrol teks yang dihasilkan
	)
	message = completions.choices[0].text
	return message


# Menyimpan obrolan chatbot
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

# Input Penguna 
def get_text():
    
    return input_text 
    

# Respone Chatbot
user_input = get_text()
   
if user_input:
    output = generate_response(user_input)
    # Menyimpan output
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)
	
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        input_text2 = st.session_state["generated"][i]

def text_to_speech(input_language, output_language, input_text2, tld):
    translation = translator.translate(input_text2, src="id", dest="id")
    trans_text = translation.text
    tts = gTTS(trans_text, lang="id", tld="com", slow=False)
    try:
        my_file_name = input_text2[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text


display_output_text = st.checkbox("Display output text")

if st.button("convert"):
    result, output_text = text_to_speech("id", "id",input_text2, "com")
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown(f"## Your audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    if display_output_text:
        st.markdown(f"## Output text:")
        st.write(f" {output_text}")


def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)


remove_files(7)
