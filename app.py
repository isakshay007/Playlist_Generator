import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from lyzr_automata.tasks.task_literals import InputType, OutputType
import os

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]


st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Playlist Generator🎧")
st.markdown("### Welcome to the Lyzr Playlist Generator!!!")
st.markdown("Welcome to the Lyzr Playlist Generator! By simply entering your favorite songs, genres, or artists, our playlist generator will create a personalized musical journey just for you.")

input = st.text_input("Enter your favourite songs, your genre or your favourite artists : ",placeholder=f"""Type here""")

open_ai_text_completion_model = OpenAIModel(
    api_key=st.secrets["apikey"],
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)


def playlist_generation(code):
    generator_agent = Agent(
        role="PLAYLIST CURATOR expert",
        prompt_persona=f"Your task is to CREATE a CUSTOMIZED playlist that PERFECTLY aligns with the user's musical preferences."
    )

    prompt = f"""
You are an Expert PLAYLIST CURATOR and MUSIC ENTHUSIAST. Your task is to CREATE a CUSTOMIZED playlist that PERFECTLY aligns with the user's musical preferences.

To execute this task EFFECTIVELY, follow these steps:

1. COLLECT detailed insights regarding the user's FAVORITE SONGS, GENRES, and ARTISTS.

2. EXAMINE the gathered information to identify commonalities in BEATS, MELODIES, and THEMES.

3. SEARCH for tracks that ALIGN with these patterns, including both popular anthems and undiscovered gems.

4. ASSEMBLE a selection of 10-30 TRACKS that resonate with the user's taste while ensuring a seamless auditory journey.

5. SEQUENCE the songs strategically to maintain ENGAGEMENT, balancing energy levels throughout the playlist.

6. EVALUATE your choices for DIVERSITY and HARMONY to ensure each track enhances the collective mood.

7. TITLE the playlist CREATIVELY and DISPLAY it in an attractive format exclusively featuring the playlist title and songs.

You MUST ONLY display the CUSTOMIZED PLAYLIST TITLE followed by the song list.
    """

    generator_agent_task = Task(
        name="Playlist Generation",
        model=open_ai_text_completion_model,
        agent=generator_agent,
        instructions=prompt,
        default_input=code,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
    ).execute()

    return generator_agent_task 
   
if st.button("Generate!"):
    solution = playlist_generation(input)
    st.markdown(solution)

with st.expander("ℹ️ - About this App"):
    st.markdown("""
    This app uses Lyzr Automata Agent Optimize your code. For any inquiries or issues, please contact Lyzr.

    """)
    st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width=True)
    st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width=True)
    st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width=True)
    st.link_button("Slack",
                   url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw',
                   use_container_width=True)