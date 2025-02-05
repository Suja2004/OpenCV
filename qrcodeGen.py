import math

# Encode input data into binary
def encode_data(data):
    binary_data = ''.join(format(ord(char), '08b') for char in data)
    return binary_data

# Add error correction by repeating each binary digit
def add_error_correction(binary_data):
    return ''.join(bit * 4 for bit in binary_data)

# Generate a matrix for the QR code
def create_qr_matrix(binary_data, size):
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    index = 0

    for row in range(size):
        for col in range(size):
            if index < len(binary_data):
                matrix[row][col] = int(binary_data[index])
                index += 1
            else:
                break
    return matrix


# Create an image from the QR code matrix
def generate_qr_image(matrix, scale=10):
    from PIL import Image, ImageDraw

    size = len(matrix)
    img_size = size * scale
    img = Image.new("1", (img_size, img_size), "white")  # Black & white image
    draw = ImageDraw.Draw(img)

    for row in range(size):
        for col in range(size):
            if matrix[row][col] == 1:
                x0 = col * scale
                y0 = row * scale
                x1 = x0 + scale
                y1 = y0 + scale
                draw.rectangle([x0, y0, x1, y1], fill="black")

    img.save("qr_code.png")
    img.show()

# Main QR code generation process
def generate_qr_code(data):
    binary_data = encode_data(data)
    print("Binary Data:", binary_data)
    corrected_data = add_error_correction(binary_data)
    print("Error Corrected Data:", corrected_data)

    # Determine size of QR matrix (nearest square size)
    matrix_size = math.ceil(math.sqrt(len(corrected_data)))
    print("QR Code Matrix Size:", matrix_size)
    qr_matrix = create_qr_matrix(corrected_data, matrix_size)

    # Generate and display the QR code
    generate_qr_image(qr_matrix)


# Input for the QR code
data = input("Enter the text to generate QR code: ")
generate_qr_code(data)
