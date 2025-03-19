import matplotlib.pyplot as plt
import matplotlib.patches as patches

class BlockArrangement:
    def __init__(self, width=800, height=600):
        self.total_width = width
        self.total_height = height

    def evaluate_expression(self, expr):
        """Safely evaluate expressions that might contain total_width or total_height"""
        if not isinstance(expr, str):
            return float(expr)  # Convert numeric types to float for consistency
            
        # Replace both self.total_width and total_width
        expr = expr.replace('self.total_width', str(self.total_width))
        expr = expr.replace('self.total_height', str(self.total_height))
        expr = expr.replace('total_width', str(self.total_width))
        expr = expr.replace('total_height', str(self.total_height))
        
        try:
            return float(eval(expr))  # Convert result to float for consistency
        except Exception as e:
            print(f"Error evaluating expression '{expr}': {e}")
            return 0.0

    def draw_layout(self, layout):
        """
        Draws the layout based on a dictionary of block definitions.
        Each block is defined under the "blocks" key. Additionally, the
        chip's overall dimensions (from "chip_dimensions") are used to draw
        a boundary.
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Check if the layout is a list of layouts or a single layout
        if isinstance(layout, list):
            print(f"Found {len(layout)} layouts, displaying the first one")
            layout = layout[0]
            
        chip_dims = layout.get("chip_dimensions", {"width": self.total_width, "height": self.total_height})
        chip_width = float(chip_dims.get("width", self.total_width))
        chip_height = float(chip_dims.get("height", self.total_height))
        
        boundary_rect = patches.Rectangle(
            (0, 0),
            chip_width,
            chip_height,
            fill=False,
            edgecolor="red",
            linewidth=2,
            linestyle="--"
        )
        ax.add_patch(boundary_rect)
        
        # Handle both formats: direct blocks dict or nested under "blocks"
        if "blocks" in layout and isinstance(layout["blocks"], dict):
            blocks_dict = layout["blocks"]
        else:
            # Assume the layout itself is the blocks dictionary
            blocks_dict = layout
            
        for block_name, block_data in blocks_dict.items():
            try:
                # Skip non-block entries in the dictionary
                if not isinstance(block_data, dict):
                    continue
                    
                x = self.evaluate_expression(block_data.get('x', 0))
                y = self.evaluate_expression(block_data.get('y', 0))
                width = self.evaluate_expression(block_data.get('width', 0))
                height = self.evaluate_expression(block_data.get('height', 0))
                
                rect = patches.Rectangle(
                    (x, y),
                    width,
                    height,
                    facecolor=block_data.get('color', '#CCCCCC'),
                    edgecolor='black',
                    linewidth=1
                )
                ax.add_patch(rect)
                
                # Display just the block name
                ax.text(
                    x + width / 2,
                    y + height / 2,
                    block_name,
                    horizontalalignment='center',
                    verticalalignment='center',
                    fontsize=9,
                    color='black'
                )
            except Exception as e:
                print(f"Error drawing block {block_name}: {e}")
                print(f"Block data: {block_data}")
        
        ax.set_xlim(0, chip_width)
        ax.set_ylim(0, chip_height)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.title('Generated Layout', pad=20)
        plt.show()
