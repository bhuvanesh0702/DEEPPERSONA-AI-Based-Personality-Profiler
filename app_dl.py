
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from tensorflow.keras.models import load_model
import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            height: 100vh;
            min-height: 100vh;
            color: white;
        }}
        h1, h2, h3, h4, h5, h6, p, label, div, span {{
            color: white !important;
        }}
        /* Make Next button visible */
        .stButton > button {{
            background-color: #4CAF50 !important;
            color: white !important;
            border-radius: 8px;
            border: none;
            padding: 8px 16px;
            font-weight: bold;
        }}
        .stButton > button:hover {{
            background-color: #45a049 !important;
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call it at the start of your app
add_bg_from_local("Image.png")

# ==== Load dataset & model ====
DATA_PATH = "16P (2).csv"
MODEL_PATH = "model_dl.h5"

df = pd.read_csv(DATA_PATH, encoding="latin1")
model = load_model(MODEL_PATH)

# ==== Prepare questions ====
question_columns = [col for col in df.columns if col not in ["Response Id", "Personality"]]
num_questions = len(question_columns)

# ==== Expanded Personality Descriptions & Styling ====
# ==== Expanded Personality Descriptions & Styling ====
personality_info = {
    "ISTP": {
        "desc": "You are practical, action-oriented, and excel in situations requiring hands-on problem-solving. "
                "Your calm and logical approach helps you navigate challenges without unnecessary stress. "
                "You enjoy figuring out how things work, often tinkering or experimenting until you master them. "
                "Freedom and independence are core to your personality, as you dislike being overly restricted. "
                "In crises, you remain level-headed, adapting quickly and effectively to achieve results. "
                "Your resourcefulness makes you a dependable problem-solver in any situation.",
        "color": "#A2D2FF", "emoji": "🔧", "motto": "The Skilled Problem-Solver"
    },
    "ESTP": {
        "desc": "You are energetic, adventurous, and thrive in fast-paced environments where quick thinking is key. "
                "Risk-taking excites you, and you inspire others with your enthusiasm and boldness. "
                "You prefer action over excessive planning, often trusting your instincts to guide you. "
                "You enjoy being at the center of excitement, keeping life dynamic and unpredictable. "
                "Challenges motivate you to push boundaries and explore new opportunities. "
                "Your charm and adaptability make you a natural at navigating both social and professional settings.",
        "color": "#FFC8DD", "emoji": "⚡", "motto": "The Energetic Adventurer"
    },
    "INTP": {
        "desc": "You are deeply curious, analytical, and constantly seeking to understand the world around you. "
                "Complex ideas and abstract concepts fascinate you, and you can spend hours exploring possibilities. "
                "Independence and intellectual freedom matter greatly to you, as you dislike rigid systems. "
                "You excel at spotting patterns and finding unconventional solutions to problems. "
                "Your creativity blends with logic, allowing you to approach challenges from unique perspectives. "
                "Though reserved, your insights can transform the way others think.",
        "color": "#BDE0FE", "emoji": "🧠", "motto": "The Logical Thinker"
    },
    "ENFJ": {
        "desc": "You are warm, charismatic, and deeply attuned to the emotions of those around you. "
                "Guiding and inspiring others comes naturally, and you often take on the role of a mentor or motivator. "
                "You have a strong vision for what people can become and work tirelessly to help them reach it. "
                "Your empathy allows you to connect with individuals from all walks of life. "
                "Leadership is your strength, as you combine decisiveness with compassion. "
                "You inspire trust and loyalty, making you a unifying force in any group.",
        "color": "#FFD6A5", "emoji": "🤝", "motto": "The Inspiring Leader"
    },
    "ISTJ": {
        "desc": "You are dependable, detail-oriented, and have a strong sense of duty. "
                "Structure and clear rules make you feel secure, and you take pride in fulfilling responsibilities. "
                "You approach tasks methodically, ensuring accuracy and efficiency in all you do. "
                "Tradition and stability matter to you, and you value loyalty in relationships. "
                "Others rely on you to provide order in chaotic situations. "
                "Your consistency and reliability make you a cornerstone in both personal and professional life.",
        "color": "#CDB4DB", "emoji": "📜", "motto": "The Reliable Planner"
    },
    "ISFJ": {
        "desc": "You are caring, responsible, and dedicated to creating a supportive environment for others. "
                "You have a strong sense of duty and quietly work to maintain harmony in your surroundings. "
                "Your kindness often goes unnoticed because you don’t seek recognition for your efforts. "
                "You value long-term relationships and are deeply loyal to those you care about. "
                "Your ability to anticipate the needs of others makes you a trusted friend and colleague. "
                "Stability, comfort, and security are core values that guide your actions.",
        "color": "#E2F0CB", "emoji": "🌿", "motto": "The Nurturing Protector"
    },
    "INFJ": {
        "desc": "You are insightful, compassionate, and driven by a deep sense of purpose. "
                "Your ability to understand complex emotions allows you to guide others through personal growth. "
                "You are idealistic, always searching for ways to create positive change in the world. "
                "While reserved, you form deep and meaningful connections with those you trust. "
                "You value authenticity and often serve as a moral compass for others. "
                "Your vision for the future inspires and motivates those around you to dream bigger.",
        "color": "#FDE2E4", "emoji": "🌌", "motto": "The Visionary"
    },
    "INTJ": {
        "desc": "You are strategic, focused, and driven by long-term goals. "
                "You naturally see the big picture and plan accordingly to achieve success. "
                "Efficiency and precision are important to you, and you dislike wasting time on unproductive tasks. "
                "You often take on leadership roles because of your confidence and clarity of vision. "
                "Your independent thinking allows you to find innovative solutions that others might miss. "
                "You inspire respect through your determination and ability to execute complex plans flawlessly.",
        "color": "#FFB5A7", "emoji": "🎯", "motto": "The Strategic Mastermind"
    },
    "ISFP": {
        "desc": "You are gentle, artistic, and live in the moment. "
                "You value beauty, harmony, and personal freedom in all aspects of life. "
                "Your creativity often shines through in the way you approach both work and relationships. "
                "You avoid unnecessary conflict, preferring peace and understanding. "
                "Your sensitivity allows you to connect deeply with others' emotions. "
                "You live authentically, guided by your values and love for simple joys.",
        "color": "#D8F3DC", "emoji": "🎨", "motto": "The Gentle Creator"
    },
    "ESFP": {
        "desc": "You are lively, spontaneous, and bring joy wherever you go. "
                "You thrive on excitement and seek out new experiences. "
                "Your social nature allows you to connect easily with people from all walks of life. "
                "You live in the moment and prefer to focus on enjoying life rather than overthinking it. "
                "Your adaptability helps you shine in changing environments. "
                "People are drawn to your vibrant and warm personality.",
        "color": "#FFD6E0", "emoji": "🎉", "motto": "The Fun-Loving Performer"
    },
    "INFP": {
        "desc": "You are idealistic, empathetic, and guided by a deep sense of personal values. "
                "Your imagination is rich, and you often dream about how the world could be improved. "
                "You value authenticity and seek meaningful connections over superficial ones. "
                "You are deeply moved by beauty, kindness, and creativity. "
                "Your compassion allows you to be a supportive friend and listener. "
                "You strive to live a life that aligns with your principles and dreams.",
        "color": "#E0BBE4", "emoji": "🌸", "motto": "The Gentle Idealist"
    },
    "ENFP": {
        "desc": "You are enthusiastic, creative, and full of curiosity. "
                "Life excites you, and you see endless possibilities in every situation. "
                "You love meeting new people and hearing their stories. "
                "Your optimistic energy inspires those around you to think bigger and bolder. "
                "You dislike routine, preferring variety and exploration. "
                "Your adaptability allows you to thrive in ever-changing environments.",
        "color": "#FFDEB4", "emoji": "🚀", "motto": "The Free-Spirited Inspirer"
    },
    "ESTJ": {
        "desc": "You are organized, efficient, and value clear structure in your life. "
                "You take pride in being dependable and making sure tasks are completed correctly. "
                "Your leadership style is straightforward and results-driven. "
                "You respect traditions and established systems. "
                "You excel at bringing order to chaos and making practical decisions. "
                "Your reliability makes you a trusted leader in your community or workplace.",
        "color": "#B5E48C", "emoji": "🏛️", "motto": "The Organized Leader"
    },
    "ESFJ": {
        "desc": "You are warm, caring, and dedicated to helping others. "
                "Your friendly personality makes you easy to talk to and trust. "
                "You value community and harmony, often going out of your way to support loved ones. "
                "You prefer clear expectations and thrive in structured environments. "
                "Your generosity and loyalty are central to your relationships. "
                "You believe that kindness is the foundation for a better world.",
        "color": "#FEC5BB", "emoji": "💐", "motto": "The Caring Supporter"
    },
    "ENTP": {
        "desc": "You are witty, inventive, and love exploring new ideas. "
                "You enjoy debates and challenging conventional thinking. "
                "Your quick thinking allows you to adapt and innovate effortlessly. "
                "You thrive in dynamic environments where creativity is valued. "
                "Your enthusiasm inspires those around you to explore new perspectives. "
                "You see possibilities where others see problems.",
        "color": "#A5FFD6", "emoji": "💡", "motto": "The Clever Innovator"
    },
    "ENTJ": {
        "desc": "You are confident, decisive, and naturally take charge of situations. "
                "You have a clear vision for the future and work strategically to achieve it. "
                "You value efficiency and expect the same from those around you. "
                "Your leadership style combines boldness with strategic planning. "
                "You excel at organizing people and resources to meet ambitious goals. "
                "You are driven to succeed and inspire others with your determination.",
        "color": "#FFA69E", "emoji": "🏆", "motto": "The Bold Commander"
    }
}


# ==== Initialize session state ====
if "answers" not in st.session_state:
    st.session_state.answers = []
if "question_index" not in st.session_state:
    st.session_state.question_index = 0

# ==== Page Header ====
st.title("🧩 AI-Powered 16 Personality Test")
st.markdown(
    "Welcome to the *AI-based Personality Profiler*! 🎯\n"
    "This test consists of carefully crafted questions to understand your personality traits.\n"
    "Answer each question honestly, and at the end, you'll discover your *personality type* "
    "with a detailed description and insightful graphs.\n"
    "Let’s get started!"
)
st.write("---")

# ==== Display current question or results ====
current_index = st.session_state.question_index

if current_index < num_questions:
    question = question_columns[current_index]
    st.markdown(f"### Question {current_index + 1} of {num_questions}")
    st.write(f"{question}")

    options = {
        "Strongly Disagree": -3,
        "Disagree": -2,
        "Slightly Disagree": -1,
        "Neutral": 0,
        "Slightly Agree": 1,
        "Agree": 2,
        "Strongly Agree": 3
    }

    answer_label = st.radio("Choose your answer:", options=list(options.keys()))
    answer_value = options[answer_label]

    if st.button("Next ➡"):
        st.session_state.answers.append(answer_value)
        st.session_state.question_index += 1
        st.rerun()
else:
    st.subheader("🎉 Your Personality Analysis")
    st.write("Based on your responses, here’s your personality type and confidence analysis:")

    input_data = pd.DataFrame([st.session_state.answers], columns=question_columns)
    prediction = model.predict(input_data)  
    predicted_class_index = np.argmax(prediction, axis=1)[0]
    labels = df["Personality"].unique()
    predicted_label = labels[predicted_class_index]

    info = personality_info[predicted_label]

    # ==== Personality Card ====
    st.markdown(
        f"""
        <div style="background-color:{info['color']}; padding:20px; border-radius:15px; text-align:center;">
            <h2 style="margin-bottom:5px;">{info['emoji']} <b>{predicted_label}</b></h2>
            <h4 style="margin-top:0; color:gray;">{info['motto']}</h4>
            <p style="font-size:16px;">{info['desc']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 🎊 Confetti Celebration
    st.markdown(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
        var duration = 3 * 1000;
        var animationEnd = Date.now() + duration;
        var defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 999 };

        function randomInRange(min, max) {
          return Math.random() * (max - min) + min;
        }

        var interval = setInterval(function() {
          var timeLeft = animationEnd - Date.now();

          if (timeLeft <= 0) {
            return clearInterval(interval);
          }

          var particleCount = 50 * (timeLeft / duration);
          confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } }));
          confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } }));
        }, 250);
        </script>
        """,
        unsafe_allow_html=True
    )

    # ==== Radar Chart ====
    scores = prediction[0]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=labels,
        fill='toself',
        name='Prediction Confidence'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        title="📊 Personality Confidence Chart"
    )
    st.plotly_chart(fig)

    # ==== Horizontal Bar Chart ====
    bar_df = pd.DataFrame({"Personality": labels, "Confidence": scores})
    fig_bar = px.bar(
        bar_df.sort_values("Confidence", ascending=True),
        x="Confidence", y="Personality",
        orientation='h',
        title="📈 Confidence Levels for Each Personality Type",
        color="Confidence",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_bar)

    if st.button("🔄 Restart Test"):
        st.session_state.question_index = 0
        st.session_state.answers = []
        st.rerun()
