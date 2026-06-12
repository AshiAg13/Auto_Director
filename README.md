#  AutoDirector: Vertical Cinematic Feed Generator

AutoDirector is an end-to-end multi-agent AI pipeline that transforms a single-sentence story idea into a fully realized, 27-shot vertical cinematic storyboard. Built for speed and visual storytelling.

##  How It Works
1. **Input:** The user provides a raw story concept.
2. **Screenwriter Agent:** Google Gemini processes the prompt and writes a structured 3-act story.
3. **Cinematographer Agent:** Gemini breaks the story down into exactly 9 scenes and 27 distinct camera shots with rich visual descriptions.
4. **Visual Artist Agent:** The Hugging Face API (FLUX.1-schnell) generates a unique, high-quality image for every single shot in real-time.
5. **Output:** A dynamic, vertically scrolling UI that displays the Acts, Scenes, and Images sequentially, just like a professional storyboard.

##  Tech Stack
* **Frontend/UI:** Streamlit
* **LLM / Text Processing:** Google Gemini API 
* **Image Generation:** Hugging Face API (FLUX.1-schnell)
* **Language:** Python

##  How to Run Locally
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file in the root directory with your API keys:
   ```text
   GEMINI_API_KEY=your_gemini_key_here
   HUGGINGFACE_API_KEY=your_huggingface_key_here

## 📺 Project Demo Video
Click the link below to watch the full walkthrough of the AutoDirector pipeline:
[**Watch the Demo Video on Google Drive**](https://drive.google.com/drive/folders/1ZNkD_3ZwPZ4YmdKxESsjM4tpUbOA-xqE?usp=drive_link)
