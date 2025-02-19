import base64

def encode_image(image_path):
    """
    Encode the given image file as a base64 string.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')