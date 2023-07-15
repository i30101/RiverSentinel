import RPi.GPIO as GPIO

# Set up GPIO mode and pin number
GPIO.setmode(GPIO.BOARD)
pin_number = 4  # Replace with your GPIO pin number

# Set up GPIO pin as input
GPIO.setup(pin_number, GPIO.IN)

# Read the GPIO value

while True:
    gpio_value = GPIO.input(pin_number)
    print(gpio_value)

# Generate HTML content
# html_content = f"""
# <html>
#   <head>
#     <title>GPIO Reading</title>
#   </head>
#   <body>
#     <h1>GPIO Reading</h1>
#     <p>GPIO Value: {gpio_value}</p>
#   </body>
# </html>
# """

# Write HTML content to the file
# with open('/var/www/html/index.html', 'w') as html_file:
#     html_file.write(html_content)
