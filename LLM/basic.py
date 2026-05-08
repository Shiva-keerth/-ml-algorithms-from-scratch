from groq import Groq
import os

# Initialize the client
import os
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "your-api-key-here"))

# Define the model ID as a string to use in the loop
model_id = "llama-3.3-70b-versatile"

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    # The correct method call for Groq
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            }
        ],
        model=model_id,
    )

    # Correct way to extract the text response
    print("AI:", chat_completion.choices[0].message.content)