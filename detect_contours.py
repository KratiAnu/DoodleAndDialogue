import cv2
import numpy as np

# Load the image
image = cv2.imread('image3.png')
# Edge detection
edges = cv2.Canny(image, 100, 200)
# Contour detection
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Filter contours by size and aspect ratio
thought_bubbles = []
for contour in contours:
    area = cv2.contourArea(contour)
    area = area / (image.shape[0] * image.shape[1])
    if area > 1e-2 and area < 0.5 :
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        if aspect_ratio > 1.2 :
            thought_bubbles.append(contour)

img2 = image.copy()

text_lines = ['I just got a promotion at work!', "That's great! What's your new job?", "I'm now in charge of the company's vending machines.", "Oh wow, you've really hit the big time now."]


center_coords = []

for i, contour in enumerate(thought_bubbles):
    mask = np.zeros_like(image)

    # Draw filled contours on the mask
    cv2.drawContours(mask, [thought_bubbles[i]], -1, (255, 255, 255), thickness=cv2.FILLED)

    # create a binary image of the mask
    mask2 = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    # Calculate the center of mass (centroid) of the white regions in the mask
    M = cv2.moments(mask2, binaryImage=True)
    center_x = int(M['m10'] / M['m00'])
    center_y = int(M['m01'] / M['m00'])
    center_coords.append((center_x, center_y))

x_coords = [x for x, y in center_coords]
y_coords = [y for x, y in center_coords]

sorted_x_coords = np.argsort(x_coords)

i1 = sorted_x_coords[0]
i2 = sorted_x_coords[1]

y1 = y_coords[i1]
y2 = y_coords[i2]

if y1 < y2:
    top_left = i1
    bottom_left = i2
else:
    top_left = i2
    bottom_left = i1

i3 = sorted_x_coords[2]
i4 = sorted_x_coords[3]

if y_coords[i3] < y_coords[i4]:
    top_right = i3
    bottom_right = i4
else:
    top_right = i4
    bottom_right = i3

thought_bubbles = [thought_bubbles[top_left], thought_bubbles[top_right], thought_bubbles[bottom_left], thought_bubbles[bottom_right]]


for i, contour in enumerate(thought_bubbles):
    text = text_lines[i]
    mask = np.zeros_like(image)

    # Draw filled contours on the mask
    cv2.drawContours(mask, [thought_bubbles[i]], -1, (255, 255, 255), thickness=cv2.FILLED)

    # create a binary image of the mask
    mask2 = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    # Calculate the center of mass (centroid) of the white regions in the mask
    M = cv2.moments(mask2, binaryImage=True)
    center_x = int(M['m10'] / M['m00'])
    center_y = int(M['m01'] / M['m00'])

    # Define multiple lines of text
    # split the text after every 4 spaces
    lines_of_text =   text.split(' ')
    lines_of_text = [' '.join(lines_of_text[i:i+4]) for i in range(0, len(lines_of_text), 4)]
    # lines_of_text = ['']
    # Calculate the font scale based on the mask size
    font_scale = min(mask.shape[0], mask.shape[1]) / 2000  # Adjust the divisor as needed

    font_color = (255, 0, 0)  # Blue color in BGR
    font_thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Calculate the total height of all lines of text
    total_text_height = len(lines_of_text) * cv2.getTextSize(lines_of_text[0], font, font_scale, font_thickness)[0][1]

    # Calculate the starting y-coordinate to center the text vertically
    start_y = center_y - total_text_height // 2

    # Add each line of text to the mask
    for line in lines_of_text:
        # Calculate the size of the current line of text
        text_size = cv2.getTextSize(line, font, font_scale, font_thickness)[0]
        
        # Calculate the x-coordinate to center the text horizontally
        text_x = center_x - text_size[0] // 2
        
        # Add the text to the mask
        cv2.putText(image, line, (text_x, start_y), font, font_scale, font_color, font_thickness)
        
        # Move the starting y-coordinate down for the next line
        start_y += text_size[1]

# Display or save the mask
cv2.imshow('Contour Mask', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
