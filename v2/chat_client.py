from groq import Groq
import requests
from config import AMD_API_KEY, API_URL, IMAGE_MAX_COMPLETION_TOKENS, API_KEY, IMAGE_MODEL, LAYOUT_MODEL, LAYOUT_TEMPERATURE, LAYOUT_MAX_TOKENS, LAYOUT_TOP_P

client = Groq(api_key=API_KEY)

headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": AMD_API_KEY,
    "Cache-Control": "no-cache"
}

def get_image_description(encoded_image, prompt):
    """
    Sends an image (as a base64 string) and a text prompt to extract the chip layout description.
    """
    # We keep the same message format (with text and image_url)
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{encoded_image}"}
                },
            ],
        }
    ]
    
    payload = {
        "messages": messages,
        "temperature": LAYOUT_TEMPERATURE, 
        "n": 1,
        "seed": 0,
        "stream": False,
        "stop": None,
        "max_Tokens": None,
        "max_Completion_Tokens": IMAGE_MAX_COMPLETION_TOKENS,
        "presence_Penalty": 0,
        "frequency_Penalty": 0,
        "logit_Bias": None,
        "user": None,
        "reasoning_Effort": "string",
        "response_Format": None,
        "tools": None,
        "tool_Choice": None,
    }
    
    url = API_URL
    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()
    
    # Return the content of the first choice
    return response_data["choices"][0]["message"]["content"]

def get_layout_suggestions(prompt):
    """
    Sends a prompt (which includes the image description and additional constraints)
    to generate layout suggestions.
    """
    messages = [{"role": "user", "content": prompt}]
    
    payload = {
        "messages": messages,
        "temperature": LAYOUT_TEMPERATURE,
        "n": 1,
        "seed": 0,
        "stream": False,  
        "stop": None,
        "max_Tokens": None,
        "max_Completion_Tokens": LAYOUT_MAX_TOKENS,
        "presence_Penalty": 0,
        "frequency_Penalty": 0,
        "logit_Bias": None,
        "user": None,
        "reasoning_Effort": "string",
        "response_Format": None,
        "tools": None,
        "tool_Choice": None,
        "top_p": LAYOUT_TOP_P,
    }
    
    url = API_URL
    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()
    
    return response_data["choices"][0]["message"]["content"]

def get_image_description_groq(encoded_image, prompt):
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

def get_layout_suggestions_groq(prompt):
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
