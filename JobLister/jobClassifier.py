import os
import google.generativeai as genai

os.environ["GEMINI_API_KEY"] = ""

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="Please provide the response in the following JSON format:\n\n{\n  \"job\": \"<describe the task>\",\n  \"price\": \"<price in Indian rupees>\",\n  \"time\": \"<time in minutes>\"\n}\n\nMake sure the response follows this format strictly, with the \"job\" being a string that describes the task, \"price\" as an integer representing the cost in Indian rupees, and \"time\" as an integer representing the estimated time in minutes. Do not include any additional information or text outside of the JSON structure.\n\nExample task: \"build a calculator in real life\"\n",
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "make a simple login form\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "{\n    \"job\": \"create a simple login form\",\n    \"price\": 10,\n    \"time\": 30\n}",
      ],
    },
    {
      "role": "user",
      "parts": [
        "wash dishes",
      ],
    },
    {
      "role": "model",
      "parts": [
        "{\n\"job\": \"wash dishes\",\n\"price\": 5,\n\"time\": 15\n} \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "wash dishes\n\n\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "{\n\"job\": \"wash dishes\",\n\"price\": 5,\n\"time\": 15\n} \n",
      ],
    },
  ]
)

# Function to send a message to the AI model and get a response
def send_message_to_model(input_text):
    response = chat_session.send_message(input_text)
    return response.text
