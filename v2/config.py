API_KEY = ""
IMAGE_PATH = "baseimage.png"

IMAGE_MODEL = "llama-3.2-90b-vision-preview"
LAYOUT_MODEL = "llama-3.1-8b-instant"

LAYOUT_TEMPERATURE = 0.5
LAYOUT_MAX_TOKENS = 4096
LAYOUT_TOP_P = 1

IMAGE_PROMOT = """You are an expert chip layout optimizer. Analyze this layout image with the goal of generating alternative arrangements.
                Analyze the provided chip floorplan image and extract the following key details:
                Core Measurements
                Provide specific numerical values for:

                Total chip dimensions (width * height)
                Total chip area
                Individual block measurements:

                Width and height of each block
                Area of each block
                Exact coordinates/position of each block
                Percentage of total chip area occupied by each block


                Block Identification and Properties
                For each block in the image:

                Block name/identifier
                Exact dimensions
                Location within the layout
                Current aspect ratio

                Ensure that all blocks cover the whole area of the image 

                Mention
                Which blocks are adjacent to each other


                Output Requirements
                Present all measurements in:

                Consistent units
                Numerical format with appropriate precision
                Percentages rounded to two decimal places
                Coordinates relative to a clearly defined origin point


                Output all this in strictly JSON format for easeness in the next step
                Analyze it fully and follow the chain of thought prompting and get to the final output description."""


Constraints = """See the Image will be of Consisting of individual blocks (chip floorplan), We can extract the total area and the 
 total area covered by all the individual blocks their dimensions and the total percentage that it covers of the whole Image  which is provided in the image description 
There are some Constraints which will be while generating layouts :
1 .The Area of all the individual blocks should remain conserved ,the aspect ratio can change however according to the arrangements 
2. All the rearranged blocks should be fitted inside the whole chip layout and there should be no gaps/blank spaces within the generated layouts (blocks should be arranged that way)
3. All the F blocks and their subdivisions should be connected to the E block , 
therefore the area of the E block can be expanded if needed and the aspect ratio can be modified (also mentioned in the above constraint) ,  here keep in mind that it is not necessary that F blocks have to be connected sequentially or to each other they just need to be connected to have sharing one of the Edges with the E block(like network block) 

"""
Sample_code ="""   This is the sample  code format of a valid dictionary generated  output generated for model to learn and provide similar layouts with different arrangements  
{  
    "E":
{
    {
        "x": "0.45 * self.total_width",  
        "y": 0,  
        "width": "0.1 * self.total_width",  
        "height": "self.total_height",  
        "color": "#40E0D0"  
    },  
    "F1": {  
        "x": 0,  
        "y": "0.9 * self.total_height",  
        "width": "0.45 * self.total_width",  
        "height": "0.1 * self.total_height",  
        "color": "#D3D3D3"  
    },  
    "F2": {  
        "x": "0.55 * self.total_width",  
        "y": "0.9 * self.total_height",  
        "width": "0.45 * self.total_width",  
        "height": "0.1 * self.total_height",  
        "color": "#D3D3D3"  
    },  
    "F3": {  
        "x": 0,  
        "y": 0,  
        "width": "0.45 * self.total_width",  
        "height": "0.1 * self.total_height",  
        "color": "#D3D3D3"  
    },  
    "F4": {  
        "x": "0.55 * self.total_width",  
        "y": 0,  
        "width": "0.45 * self.total_width",  
        "height": "0.1 * self.total_height",  
        "color": "#D3D3D3"  
    },  
    "A": {  
        "x": 0,  
        "y": "0.1 * self.total_height",  
        "width": "0.45 * self.total_width",  
        "height": "0.5 * self.total_height",  
        "color": "#F0F0F0"  
    },  
    "B": {  
        "x": "0.55 * self.total_width",  
        "y": "0.5 * self.total_height",  
        "width": "0.45 * self.total_width",  
        "height": "0.40 * self.total_height",  
        "color": "#DAA520"  
    },  
    "C": {  
        "x": "0.55 * self.total_width",  
        "y": "0.1 * self.total_height",  
        "width": "0.45 * self.total_width",  
        "height": "0.43 * self.total_height",  
        "color": "#4169E1"  
    },  
    "D": {  
        "x": 0,  
        "y": "0.6 * self.total_height",  
        "width": "0.45 * self.total_width",  
        "height": "0.3 * self.total_height",  
        "color": "#9370DB"  
    },  
    "Gray": {  
        "x": "0.99 * self.total_width",  
        "y": "0.00001 * self.total_height",  
        "width": "0.03 * self.total_width",  
        "height": "0.1 * self.total_height",  
        "color": "#808080"  
    }  
}  

"""

LAYOUT_PROMPT_TEMPLATE = """You are an expert chip layout optimizer.
I will provide an image description containing block details.
Using the following constraints and sample code, generate exactly 3 different layout dictionaries.
**IMPORTANT:** Output only valid JSON in the following format:
[
   {{ <layout dictionary 1> }},
   {{ <layout dictionary 2> }},
   {{ <layout dictionary 3> }}
]
Do not include any markdown formatting, introductions, or commentary—output only the JSON.

Image Description:
{image_description}

Constraints:
{Constraints}

Sample Code:
{Sample_code}
"""
