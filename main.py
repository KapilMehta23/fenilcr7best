# main.py

import json
from config import IMAGE_PATH, IMAGE_PROMPT, LAYOUT_PROMPT_TEMPLATE, Constraints, Sample_code
from utils import encode_image
from chat_client import get_image_description, get_layout_suggestions
from layout_drawer import BlockArrangement

def main():  
    # Step 1: Image Encoding and Analysis  
    encoded_image = encode_image(IMAGE_PATH)  
      
    image_description = get_image_description(encoded_image, IMAGE_PROMPT)  
    print("Image Description:\n", image_description)  
      
    LAYOUT_PROMPT = LAYOUT_PROMPT_TEMPLATE.format(  
        IMAGE_PROMPT=image_description,  
        Constraints=Constraints  
    )  
      
    try:  
        layout_response = get_layout_suggestions(LAYOUT_PROMPT)  
        print("Layout Suggestions Response:\n", layout_response)  
    except Exception as e:  
        print(f"An error occurred while getting layout suggestions: {e}")  
        return  
  
    # Step 3: Parse and Draw Layouts  
    try:  
        # If layout_response is a string, parse it as JSON  
        if isinstance(layout_response, str):  
            layouts = json.loads(layout_response)  
        else:  
            layouts = layout_response  
  
        # Verify that layouts is a list  
        if not isinstance(layouts, list):  
            print("Layout suggestions not in the expected list format.")  
            return  
              
        arranger = BlockArrangement(width=800, height=600)  
        for idx, layout in enumerate(layouts):  
            print(f"Drawing layout {idx + 1}")  
            arranger.draw_layout(layout)  
              
    except json.JSONDecodeError as e:  
        print(f"Failed to parse layout suggestions as JSON: {e}")  
    except Exception as e:  
        print(f"An error occurred while processing layouts: {e}")  
  
if __name__ == "__main__":  
    main()  
