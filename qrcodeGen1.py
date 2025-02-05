import qrcode

# Input data for the QR Code
data = input("Enter the text or URL for the QR code: ")

# Create a QR code instance
qr = qrcode.QRCode(
    version=1,  # Controls the size of the QR Code (1 = small, 40 = large)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
    box_size=10,  # Size of each box in the QR code grid
    border=1,  # Thickness of the border
)

# Add data to the QR Code
qr.add_data(data)
qr.make(fit=True)

# Generate the QR Code image
img = qr.make_image(fill_color="black", back_color="white")

# Save the image
filename = "generated_qr_code.png"
img.save(filename)
print(f"QR Code saved as {filename}")

# Show the QR Code
img.show()
