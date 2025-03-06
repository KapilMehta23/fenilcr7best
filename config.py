API_KEY = "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"
IMAGE_PATH = "IMAP1.png"

IMAGE_MODEL = "llama-3.2-90b-vision-preview"
LAYOUT_MODEL = "llama-3.1-8b-instant"

LAYOUT_TEMPERATURE = 0.2 #Creativity of the model
LAYOUT_MAX_TOKENS = 4096  #Maximum tokens to generate
LAYOUT_TOP_P = 0.9 #Top P value for sampling

IMAGE_PROMPT = '''You are an expert chip layout optimizer/Analyzer. Analyze this complex floorplan image meticulously.

Extract the following details with precision:

Core Measurements:
- Total chip dimensions (width * height) in consistent units
- Total chip area
- Establish a coordinate system with (0,0) at the bottom-left corner

For each block:
- Block name/identifier exactly as labeled
- Precise width and height measurements
- Exact coordinates (x,y) of bottom-left corner
- Block area and percentage of total chip area
- Current aspect ratio (width:height)
- Unique color code (HEX value) for visualization

Block Relationships:
- Generate a complete adjacency map listing all pairs of blocks that share an edge
- Identify functional groups of blocks (like FSR_0-3 or HDIOL blocks)
- Note any apparent connectivity requirements (blocks that appear to require proximity)

Output all the details in an structured format 
{
  "chip_dimensions": {"width": X, "height": Y},
  "total_area": Z,
  "blocks": {
    "block_name": {
      "x": position_x,
      "y": position_y,
      "width": width,
      "height": height,
      "area": area,
      "percentage": percentage,
      "aspect_ratio": ratio,
      "color": "#HEXCODE"
    },
    ...
  },
  "adjacency_map": [
    ["block_A", "block_B"],
    ...
  ],
  "functional_groups": {
    "group_name": ["block_1", "block_2", ...],
    ...
  }
}

Analyze every detail methodically and ensure complete coverage with no gaps in the analysis.

'''

Constraints = '''See the Image will be of Consisting of individual blocks (chip floorplan), We can extract the total area and the 
 total area covered by all the individual blocks their dimensions and the total percentage that it covers of the whole Image  which is provided in the image description 
There are some Constraints which will be while generating layouts :
**Hard Constraints (MUST FOLLOW):**


1. Block Area Preservation: The area of each individual block must remain exactly the same as in the original layout.
2.The area of the blocks should remain constant, the aspect ratio can change however according to the adjacent block arrangements.
3. Complete Coverage: All blocks must fit precisely within the chip boundaries with no gaps or overlaps between any blocks.
4. There should be NO OVERLAPS between the blocks in the generated layouts.
5. Maintain the same and Consistent color coding throughout the generated layouts.
6. Aspect Ratio Limits: When modifying block shapes, aspect ratios should not change by more than 2:1 from original.
7. Physical Feasibility: Generated layouts must represent physically realizable chip designs.
8.All the rearrangend blocks should be properly arranged and should be properly separated from each other.
9 ALL the blocks should be fitted properly in the layout and should not be outside the layout.
'''
Sample_code ="""   This is the sample code format of a valid dictionary generated  output generated for model to learn and provide similar layouts with different arrangements  
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

# LAYOUT_PROMPT_TEMPLATE = fLAYOUT_PROMPT_TEMPLATE = f'''You are an expert chip layout optimizer specializing in complex floorplans.  
  
# Based on the provided image description of a chip floorplan with , generate exactly 3 alternative layout designs.  
  
# APPROACH TO COMPLEX LAYOUTS:  
# 1. Analyze functional groups first (APU blocks, FSR blocks, HDIOL blocks, etc.)  
# 2. Preserve critical adjacencies between related blocks  
# 3. Consider hierarchical optimization - first arrange major block groups, then optimize within groups  
# 4. Ensure all constraints are strictly satisfied  
# 5. Verify NO OVERLAPS or gaps exist in the final layout  
  
# Image Description:  
# {IMAGE_PROMPT}  
  
# Constraints:  
# {Constraints}  
  
# OUTPUT REQUIREMENTS:  
# Generate a valid JSON array containing 3 different layout dictionaries. Each dictionary must:  
# - Define position (x,y), dimensions (width,height), and color for every block  
# - Express positions and dimensions as mathematical expressions relative to total_width and total_height  
# - Ensure blocks precisely fill the available space  
# - Represent meaningfully different arrangements (not minor variations)  
  
# Output format (JSON array only, no explanations):  
# [  
#   {{  
#     "block_1": {{  
#       "x": "expression",  
#       "y": "expression",  
#       "width": "expression",  
#       "height": "expression",  
#       "color": "#HEXCODE"  
#     }},  
#     ...  
#   }},  
#   ... additional layout dictionaries ...  
# ]  
# '''  
LAYOUT_PROMPT_TEMPLATE = f'''You are an expert chip layout optimizer specializing in complex floorplans.  
  
Based on the provided image description of a chip floorplan with, generate exactly 3 alternative layout designs.  
  
APPROACH TO COMPLEX LAYOUTS:  
1. Analyze functional groups first (APU blocks, FSR blocks, HDIOL blocks, etc.)  
2. Preserve critical adjacencies between related blocks  
3. Consider hierarchical optimization - first arrange major block groups, then optimize within groups  
4. Ensure all constraints are strictly satisfied  
5. Verify NO OVERLAPS or gaps exist in the final layout  
  
Image Description:  
{IMAGE_PROMPT}  
  
Constraints:  
{Constraints}  
  
OUTPUT REQUIREMENTS:  
Generate a valid JSON array containing 3 different layout dictionaries. Each dictionary must:  
- Define position (x,y), dimensions (width,height), and color for every block  
- Express positions and dimensions as mathematical expressions relative to total_width and total_height  
- Ensure blocks precisely fill the available space  
- Represent meaningfully different arrangements (not minor variations)  
  
Output format (JSON array only, no explanations):  
[  
  {{  
    "block_1": {{  
      "x": "expression",  
      "y": "expression",  
      "width": "expression",  
      "height": "expression",  
      "color": "#HEXCODE"  
    }},  
    ...  
  }},  
  ... additional layout dictionaries ...  
]  
'''  
