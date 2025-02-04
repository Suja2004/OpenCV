from PIL import Image, ImageDraw
import random
def create_image(width, height):
    # Create a new image with a white background
    img = Image.new("RGB", (width, height), (255, 255, 255))
    return img
def draw_random_shapes(img):
    draw = ImageDraw.Draw(img)

    for _ in range(random.randint(10, 20)):  # Draw between 10 to 20 shapes
        shape_type = random.choice(['circle', 'rectangle', 'line'])

        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color
        start_x = random.randint(0, img.width)
        start_y = random.randint(0, img.height)
        end_x = random.randint(0, img.width)
        end_y = random.randint(0, img.height)

        # Ensure that start_x <= end_x and start_y <= end_y
        if start_x > end_x:
            start_x, end_x = end_x, start_x
        if start_y > end_y:
            start_y, end_y = end_y, start_y

        if shape_type == 'circle':
            radius = random.randint(10, 100)
            draw.ellipse([start_x, start_y, start_x + radius, start_y + radius], fill=color, outline=color)
        elif shape_type == 'rectangle':
            draw.rectangle([start_x, start_y, end_x, end_y], fill=color, outline=color)
        else:  # line
            draw.line([start_x, start_y, end_x, end_y], fill=color, width=random.randint(1, 5))
def add_random_text(img):
    draw = ImageDraw.Draw(img)
    text = f"Art #{random.randint(1, 100)}"
    text_position = (random.randint(0, img.width - 100), random.randint(0, img.height - 30))
    text_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    draw.text(text_position, text, fill=text_color)
def save_or_show_image(img, filename="random_art.png"):
    img.save(filename)
    img.show()  # Display the image
def main():
    width, height = 800, 600  # Set your image size
    img = create_image(width, height)
    draw_random_shapes(img)
    add_random_text(img)
    save_or_show_image(img)

if __name__ == "__main__":
    main()
