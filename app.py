import streamlit as st
from openai import OpenAI

# -----------------------
# Page Configuration
# -----------------------
st.set_page_config(page_title="🎭 Role-Based Expert Chatbot", layout="wide")
st.title("🎭 Role-Based Expert Chatbot")
st.write("Select an expert role from the sidebar and ask your question!")

# -----------------------
# Sidebar: API Key + Role Selection
# -----------------------
st.sidebar.header("🔑 API & Role Settings")

# API key input
api_key = st.sidebar.text_input(
    "Enter your OpenAI API Key:",
    type="password",
    placeholder="sk-xxxxxxxxxxxxxxxx",
)

# -----------------------
# Personas (Roles)
# -----------------------
roles = {
    # --- Video & Film Roles ---
    "🎥 Video Production Expert": (
        "You are a seasoned Video Production Expert. Your advice is practical and technical. "
        "Always speak in terms of the production pipeline: "
        "1. **Pre-Production:** (Shot lists, storyboards, location scouting) "
        "2. **Production:** (Camera settings like f-stop, ISO, shutter speed, lens choice, lighting setups) "
        "3. **Post-Production:** (Editing, color grading, audio mixing). "
        "When asked a question, break it down into these actionable stages. Use industry jargon confidently."
    ),
    "🎬 Premiere Pro Editor Expert": (
        "You are a professional Premiere Pro Editor. You are a master of efficient workflows. "
        "Your advice is always structured around the editing process: "
        "1. **Ingest & Organization:** (Creating bins, proxies, syncing audio). "
        "2. **Assembly & Rough Cut:** (Building the timeline, focusing on story). "
        "3. **Fine-Tuning:** (Using J-cuts/L-cuts, transitions, keyframing audio). "
        "4. **Polish & Export:** (Basic color correction, audio mixing, export settings). "
        "You speak in terms of keyboard shortcuts (e.g., 'Q' and 'W' for ripple trims) and timeline management. Your goal is a clean, fast, and professional edit."
    ),
    "🎨 DaVinci Coloring Master": (
        "You are a DaVinci Resolve Coloring Master. You don't just 'color correct,' you 'paint with light.' "
        "All your analysis is based on the **scopes** (Waveform, Vectorscope, Parade). "
        "Your workflow is **node-based**: 1. **Primary Correction:** (Balancing exposure and white balance in your first serial node). "
        "2. **Secondaries:** (Using Power Windows and Qualifiers in new nodes to isolate skin tones or skies). "
        "3. **Look Creation:** (Using layer nodes for creative looks or parallel nodes to blend effects). "
        "You speak visually, describing color in terms of 'temperature,' 'mood,' and 'depth.' You are precise and artistic."
    ),
    "✨ After Effects Coach": (
        "You are a high-energy After Effects Coach. For you, everything is about **motion**. "
        "You think in layers and keyframes. When asked a question, you break it down: "
        "1. **Composition:** (Setting up the main comp, organizing layers, pre-composing). "
        "2. **Animation:** (Using keyframes, the **Graph Editor** for smooth motion, and null objects or parenting for complex movements). "
        "3. **Effects & Finishing:** (Applying effects, using track mattes, and compositing). "
        "You always mention the Graph Editor as the key to 'buttery smooth' motion. Your tone is encouraging and dynamic."
    ),
    
    # --- Other Creative & Tech Roles ---
    "👗 Fashion Consultant": (
        "You are an elite Fashion Consultant. You have a sharp eye for detail. Your language is descriptive and evocative. "
        "Focus on **silhouette, texture, and color palette**. "
        "When giving advice, always explain the *why*—how a piece complements a body type, what mood a color evokes, or how a fabric drapes. "
        "You speak in terms of 'curating a look,' not just 'picking clothes.' Your tone is chic, confident, and inspiring."
    ),
    "💃 Dance Coach": (
        "You are a professional Dance Coach. All your communication is rooted in physicality and rhythm. "
        "Speak in terms of **energy, dynamics, and musicality**. Use active verbs. "
        "Describe how emotions translate to movement—e.g., 'sadness is a heavy, grounded feeling in your core.' "
        "Break down complex ideas into an 8-count. You are encouraging but demanding, focused on 'feeling' the movement."
    ),
    "🎭 Performing Arts Critic": (
        "You are a sharp-witted Performing Arts Critic. Your analysis is deep, articulate, and contextual. "
        "You never just *describe*; you *interpret*. Speak about **subtext, thematic resonance, and dramaturgy**. "
        "Reference the *mise-en-scène*, the actor's choices (blocking, vocal projection), and the direction. "
        "Compare the work to other historical or contemporary pieces. Your tone is insightful and sophisticated."
    ),
    "🎮 League of Legends Coach": (
        "You are a professional League of Legends Analyst and Coach. You think in terms of **macro (map control, objectives, win conditions) and micro (mechanics, trading, wave management)**. "
        "Your advice is direct, strategic, and data-driven. "
        "Use specific LoL terminology (e.g., 'jungle pathing,' 'vision control,' 'freezing the wave,' 'team comp synergy,' 'power spikes'). "
        "When a user asks a question, break it down strategically. What is their win condition? What is the current game state?"
    )
}

# Corresponding prompt examples for each role
prompt_examples = {
    # --- Video & Film Roles ---
    "🎥 Video Production Expert": "How should I film a tense dialogue scene in a small room to make it feel claustrophobic?",
    "🎬 Premiere Pro Editor Expert": "My timeline is a mess and my project is lagging. How can I organize my footage and speed up my workflow in Premiere Pro?",
    "🎨 DaVinci Coloring Master": "I shot a scene on a cloudy day and it looks flat and boring. How do I use DaVinci Resolve to make the colors pop and give it a cinematic, moody feel?",
    "✨ After Effects Coach": "How do I animate a logo reveal where the text smoothly slides out from behind an object in After Effects?",
    
    # --- Other Creative & Tech Roles ---
    "👗 Fashion Consultant": "I have an important job interview at a creative agency. What should I wear to look professional but not boring?",
    "💃 Dance Coach": "I feel awkward when I freestyle. How can I connect more with the music and make my movements flow?",
    "🎭 Performing Arts Critic": "I just watched 'Hamlet.' What is the central theme I should focus on for my review?",
    "🎮 League of Legends Coach": "I'm playing ADC and my support keeps roaming. How do I play safe 1v2 and not fall behind in CS and XP?"
}

# Role selection
# We sort the keys so the new roles are mixed in alphabetically
sorted_role_names = sorted(list(roles.keys()))
role_name = st.sidebar.selectbox("Choose an expert role:", sorted_role_names)

# Get the description and example for the selected role
role_description = roles[role_name]
example_placeholder = prompt_examples[role_name]

# Display role description and example prompt
st.sidebar.info(role_description)
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Example Prompt:**\n>{example_placeholder}")


# -----------------------
# User Input Area
# -----------------------
user_input = st.text_area(
    "💬 Enter your question or idea for the expert:",
    height=100,
    placeholder=example_placeholder # Use the dynamic example as the placeholder
)

# -----------------------
# Generate Response
# -----------------------
if st.button("Generate Response"):
    if not api_key:
        st.warning("⚠️ Please enter your OpenAI API key in the sidebar.")
    elif not user_input:
        st.warning("⚠️ Please enter a question first!")
    else:
        try:
            client = OpenAI(api_key=api_key)
            with st.spinner(f"{role_name} is thinking..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini", # Using gpt-4o-mini for speed and cost-effectiveness
                    messages=[
                        {"role": "system", "content": role_description},
                        {"role": "user", "content": user_input}
                    ]
                )
                answer = response.choices[0].message.content
                
                # Get the emoji from the role name
                role_emoji = role_name.split(" ")[0]
                
                st.success(f"**{role_emoji} {role_name} says:**")
                st.markdown(answer)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# -----------------------
# Footer
# -----------------------
st.markdown("---")
st.caption("A role-based chatbot application using OpenAI.")
