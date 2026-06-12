import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests

# 1. SECURITY
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
hf_api_key = os.getenv("HUGGINGFACE_API_KEY")

# 2. UI
st.title("🎬 The Auto-Director")
st.markdown("### Vertical Cinematic Feed Generator")
user_prompt = st.text_input("Enter your single-line story idea:")

# -----------------------------------------
# AGENT 1: THE SCREENWRITER (Now with Memory!)
# -----------------------------------------
@st.cache_data # <-- THIS SAVES YOUR API QUOTA!
def run_screenwriter(idea):
    instructions = "Write a concise 3-Act story based on this idea: "
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(instructions + idea)
    return response.text

# -----------------------------------------
# AGENT 2: THE CINEMATOGRAPHER (Updated for 27 Shots!)
# -----------------------------------------
@st.cache_data
def run_cinematographer(story):
    instructions = """
    Break this story down into EXACTLY 3 acts. 
    For EACH act, create EXACTLY 3 scenes. 
    For EACH scene, create EXACTLY 3 camera shots.
    This means you will generate exactly 9 scenes and 27 shots in total.
    
    You MUST format your response EXACTLY like this example:
    
    ACT: Act 1 - The Setup
    SCENE: Scene 1 - The Vault Entrance
    SHOT: Wide Shot | A massive neon door glowing in the dark.
    SHOT: Close Up | Sweat on the thief's face.
    SHOT: Insert | A glowing cyber-tool overriding the lock.
    
    Story: 
    """
    model = genai.GenerativeModel('gemini-2.5-flash') # Make sure this matches the model you swapped to!
    response = model.generate_content(instructions + story)
    return response.text

# -----------------------------------------
# AGENT 3: THE VISUAL ARTIST (FLUX.1-schnell)
# -----------------------------------------
@st.cache_data
def run_visual_artist(prompt):
    # FLUX.1-schnell is officially supported by the new Hugging Face router!
    API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {hf_api_key}"}
    
    # FLUX doesn't need weird trigger words, just good descriptions
    cinematic_prompt = f"{prompt}, highly detailed, cinematic lighting, movie still, 8k"
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": cinematic_prompt})
        
        if response.status_code == 200:
            return response.content
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Connection Error: {str(e)}"

# -----------------------------------------
# BUTTON LOGIC & THE VERTICAL FEED
# -----------------------------------------
if st.button("Generate Storyboard"):
    if user_prompt:
        
        # Step 1: Screenwriter
        st.info("✍️ The Screenwriter is writing the story...")
        story = run_screenwriter(user_prompt)
        with st.expander("View Screenwriter's 3-Act Story"):
            st.write(story)
            
        # Step 2: Cinematographer
        st.info("🎥 The Cinematographer is planning the shots...")
        shots_text = run_cinematographer(story)
        
        st.success("🎬 Vertical Cinematic Feed Generated! Now painting the scenes...")
        st.markdown("---")
        
        # -----------------------------------------
        # THE MAGIC PARSER (Now with Progress Bar!)
        # -----------------------------------------
        lines = shots_text.split('\n')
        
        # 1. Count the total number of shots to set up the progress bar
        total_shots = sum(1 for line in lines if line.strip().startswith("SHOT:"))
        current_shot = 0
        
        # 2. Create the progress bar at the top of the feed
        if total_shots > 0:
            progress_bar = st.progress(0, text=f"Preparing to generate {total_shots} images...")
        
        # 3. Read the text and build the UI
        for line in lines:
            line = line.strip()
            
            if line.startswith("ACT:"):
                st.markdown(f"## {line.replace('ACT:', '').strip()}")
                
            elif line.startswith("SCENE:"):
                st.markdown(f"#### 📍 {line.replace('SCENE:', '').strip()}")
                
            elif line.startswith("SHOT:"):
                shot_info = line.replace('SHOT:', '').strip()
                
                if "|" in shot_info:
                    shot_type, shot_desc = shot_info.split("|", 1)
                    
                    st.markdown(f"**🎥 {shot_type.strip()}**")
                    st.write(shot_desc.strip())
                    
                    # Update the progress bar text
                    current_shot += 1
                    if total_shots > 0:
                        progress_bar.progress(current_shot / total_shots, text=f"🎨 Painting Image {current_shot} of {total_shots}...")
                    
                    # Call the Visual Artist
                    with st.spinner(f"Generating Shot {current_shot}..."):
                        image_data = run_visual_artist(shot_desc.strip())
                        
                        if isinstance(image_data, bytes):
                            st.image(image_data, use_container_width=True)
                        else:
                            st.error(f"⚠️ {image_data}")
                    
                    st.markdown("<br>", unsafe_allow_html=True) 
        
        # 4. When the loop finishes, clean up and celebrate!
        if total_shots > 0:
            progress_bar.empty() # Hides the progress bar
            st.balloons() # Fun Streamlit animation!
            st.success("🎉 All shots generated successfully!")

    else:
        st.warning("Please enter an idea first!")
