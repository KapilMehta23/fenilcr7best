import matplotlib.pyplot as plt
import matplotlib.patches as patches

class BlockArrangement:
    def __init__(self, width=800, height=600):
        self.total_width = width
        self.total_height = height

    def draw_layout(self, layout):
        """
        Draws the layout based on a dictionary of block definitions.
        Each block is defined under the "blocks" key. Additionally, the
        chip's overall dimensions (from "chip_dimensions") are used to draw
        a boundary.
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        
        chip_dims = layout.get("chip_dimensions", {"width": self.total_width, "height": self.total_height})
        chip_width = chip_dims.get("width", self.total_width)
        chip_height = chip_dims.get("height", self.total_height)
        
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
        
        blocks = layout.get("blocks", {})
        for block_name, block_data in blocks.items():
            x = block_data['x']
            if isinstance(x, str):
                x = eval(x.replace('self.total_width', str(self.total_width))
                            .replace('self.total_height', str(self.total_height)))
            
            y = block_data['y']
            if isinstance(y, str):
                y = eval(y.replace('self.total_width', str(self.total_width))
                            .replace('self.total_height', str(self.total_height)))
            
            width = block_data['width']
            if isinstance(width, str):
                width = eval(width.replace('self.total_width', str(self.total_width))
                                .replace('self.total_height', str(self.total_height)))
            
            height = block_data['height']
            if isinstance(height, str):
                height = eval(height.replace('self.total_width', str(self.total_width))
                                 .replace('self.total_height', str(self.total_height)))
            
            rect = patches.Rectangle(
                (x, y),
                width,
                height,
                facecolor=block_data.get('color', '#CCCCCC'),
                edgecolor='black',
                linewidth=1
            )
            ax.add_patch(rect)
            ax.text(
                x + width / 2,
                y + height / 2,
                f'Block {block_name}',
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=9,
                color='black'
            )
        
        ax.set_xlim(0, chip_width)
        ax.set_ylim(0, chip_height)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.title('Generated Layout', pad=20)
        plt.show()
