from groq import Groq
from config import API_KEY, IMAGE_MODEL, LAYOUT_MODEL, LAYOUT_TEMPERATURE, LAYOUT_MAX_TOKENS, LAYOUT_TOP_P

client = Groq(api_key=API_KEY)

def get_image_description(encoded_image, prompt):
    """
    Sends an image (as base64) and a text prompt to extract the chip layout description.
    """
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded_image}"}}
            ],
        }
    ]
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=IMAGE_MODEL,
    )
    return chat_completion.choices[0].message.content

def get_layout_suggestions(prompt):
    """
    Sends a prompt (which includes the image description and additional constraints)
    to generate layout suggestions.
    """
    messages = [{"role": "user", "content": prompt}]
    completion = client.chat.completions.create(
        model=LAYOUT_MODEL,
        messages=messages,
        temperature=LAYOUT_TEMPERATURE,
        max_completion_tokens=LAYOUT_MAX_TOKENS,
        top_p=LAYOUT_TOP_P,
        stream=True,
        stop=None,
    )
    
    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
    return response
