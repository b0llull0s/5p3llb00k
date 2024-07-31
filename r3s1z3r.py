from PIL import Image

def calculate_new_dimensions(original_width, original_height, target_width=None, target_height=None):
    if target_width is None and target_height is None:
        raise ValueError("Specify at least one of target_width or target_height")

    if target_width and target_height:
        # Calculate the aspect ratios for both dimensions
        width_ratio = target_width / original_width
        height_ratio = target_height / original_height

        # Choose the smaller ratio to ensure the image fits within the target dimensions
        if width_ratio < height_ratio:
            new_width = target_width
            new_height = int(original_height * width_ratio)
        else:
            new_height = target_height
            new_width = int(original_width * height_ratio)
    elif target_width:
        # Calculate based on target width only
        new_width = target_width
        new_height = int(original_height * (target_width / original_width))
    elif target_height:
        # Calculate based on target height only
        new_height = target_height
        new_width = int(original_width * (target_height / original_height))

    return new_width, new_height

# Example usage
original_width = 4000  # Replace with the width of your image
original_height = 3000  # Replace with the height of your image

# Specify either the target width or target height
target_width = 400  # You can set this to your desired width
target_height = None  # Only one of these should be None, or both should be set for bounding box scaling

new_width, new_height = calculate_new_dimensions(original_width, original_height, target_width, target_height)

print(f"New dimensions: {new_width}x{new_height}")
