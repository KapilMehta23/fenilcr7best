# main.py

import json
from config import IMAGE_PATH, IMAGE_PROMPT, LAYOUT_PROMPT_TEMPLATE, Constraints, Sample_code
from utils import encode_image
from chat_client import get_image_description, get_layout_suggestions
from layout_drawer import BlockArrangement

def main():  
    encoded_image = encode_image(IMAGE_PATH)  
      
    image_description = get_image_description(encoded_image, IMAGE_PROMPT)  
      
    LAYOUT_PROMPT = LAYOUT_PROMPT_TEMPLATE.format(
        image_description=image_description,
        Constraints=Constraints
    )
      
    try:  
        layout_response = get_layout_suggestions(LAYOUT_PROMPT)  
        print("Layout Suggestions Response:\n", layout_response)  
    except Exception as e:  
        print(f"An error occurred while getting layout suggestions: {e}")  
        return  
  
    try:  
        import re
        json_match = re.search(r'\[\s*\{.*\}\s*\]', layout_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            json_str = json_str.replace('```json', '').replace('```', '')
            layouts = json.loads(json_str)
        else:
            layout_matches = re.findall(r'\{\s*"block_[^}]+\}', layout_response, re.DOTALL)
            if layout_matches:
                layouts = []
                for match in layout_matches:
                    try:
                        layout = json.loads(match)
                        layouts.append(layout)
                    except json.JSONDecodeError:
                        print(f"Failed to parse layout: {match[:50]}...")
            else:
                print("No valid JSON layouts found in the response.")
                return
  
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
