import cv2
import numpy as np
import pyautogui
from PIL import Image


def overlay_images(background_image_path, overlay_image_path):
    background = Image.open(background_image_path).convert('RGBA')
    overlay = Image.open(overlay_image_path).convert('RGBA')

    combined = Image.new('RGBA', background.size)
    combined.paste(overlay, (0, 0), overlay)
    combined.paste(background, (0, 0), background)

    opencv_combined = cv2.cvtColor(np.array(combined), cv2.COLOR_RGBA2BGR)

    return opencv_combined


def find_image_centers(template_path, threshold=0):
    # Take a screenshot of the entire screen
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Read the template image
    # template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    # r, g, b, a = cv2.split(template)
    # a = cv2.cvtColor(a, cv2.COLOR_GRAY2BGR)
    # background = cv2.imread(r'.\testfiles\RareItem.png', cv2.IMREAD_UNCHANGED)
    # # r, g, b = cv2.split(background)[:3]
    # template = cv2.merge((background, a))
    template = overlay_images(template_path, r'.\testfiles\RareItem.png')

    cv2.imshow('template', template)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    template = cv2.cvtColor(template, cv2.COLOR_RGBA2GRAY)

    # Convert the screenshot to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Initialize ORB detector
    orb = cv2.ORB.create()

    # Find keypoints and descriptors with ORB
    keypoints_template, descriptors_template = orb.detectAndCompute(template, None)
    keypoints_screenshot, descriptors_screenshot = orb.detectAndCompute(screenshot_gray, None)

    # Create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors
    matches = bf.match(descriptors_template, descriptors_screenshot)
    matches = sorted(matches, key=lambda x: x.distance)

    # Filter matches based on the distance threshold
    good_matches = [m for m in matches if m.distance < threshold * matches[-1].distance]

    centers = []
    for match in good_matches:
        # Get the matching keypoints in the screenshot
        keypoint = keypoints_screenshot[match.trainIdx]
        center = (int(keypoint.pt[0]), int(keypoint.pt[1]))
        centers.append(center)

    return centers


# Example usage
template_path = r'.\testfiles\template.png'  # Path to the template image
centers = find_image_centers(template_path, threshold=0.75)

for center in centers:
    print("Center found at:", center)

# Optional: Visualize the results
screenshot = pyautogui.screenshot()
screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
for center in centers:
    cv2.circle(screenshot, center, 10, (0, 255, 0), 2)

cv2.imshow("Matches", screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()
