import streamlit as st
import requests

# Streamlit UI
st.title("AI Prompt Restructurer with RISEN Framework")
st.write("Refine your AI prompts using the RISEN framework for better results!")

# Sidebar for API Key and Model Selection
st.sidebar.header("API Settings")
api_key = st.sidebar.text_input("Enter OpenRouter API Key:", type="password")


# Fetch available models from OpenRouter API
def get_models(api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get("https://openrouter.ai/api/v1/models", headers=headers)
        if response.status_code == 200:
            return [model["id"] for model in response.json().get("data", [])]
        else:
            return ["openrouter/gpt-4", "openrouter/gpt-3.5-turbo", "openrouter/mistral"]
    except Exception:
        return ["openrouter/gpt-4", "openrouter/gpt-3.5-turbo", "openrouter/mistral"]


models = get_models(api_key)
model = st.sidebar.selectbox("Select AI Model:", models)

# User input
user_prompt = st.text_area("Enter your initial idea or topic:")

# RISEN Framework Inputs
role = st.text_input("Role: Who are you?")
instruction = st.text_input("Instruction: What do you want AI to do?")
steps = st.text_input("Steps: How should AI structure the response?")
end_goal = st.text_input("End Goal: What should the final output achieve?")
narrow = st.text_input("Narrow: Any specific constraints or preferences?")

# Initialize session state for final_prompt
if "final_prompt" not in st.session_state:
    st.session_state.final_prompt = ""

if st.button("Generate Structured Prompt"):
    # Generate structured prompt using RISEN
    st.session_state.final_prompt = (f"You are {role}. {instruction} Follow these steps: {steps}. "
                                     f"Ensure the result meets this goal: {end_goal}. "
                                     f"Keep in mind these constraints: {narrow}.")

st.subheader("Generated Prompt:")
st.session_state.final_prompt = st.text_area("Edit your prompt before sending:", st.session_state.final_prompt, height=150)

if st.button("Generate AI Response"):
    if not api_key:
        st.error("Please enter your OpenRouter API key in the sidebar.")
    elif not st.session_state.final_prompt.strip():
        st.error("Please generate or enter a prompt before sending it to AI.")
    else:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": st.session_state.final_prompt}
            ]
        }
        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
            if response.status_code == 200:
                result = response.json()["choices"][0]["message"]["content"]
                st.subheader("AI Response:")
                st.write(result)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception:
            st.error("Error generating response. Please check your API key and try again.")
