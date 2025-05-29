import os
import base64
import io
from dotenv import load_dotenv
from PIL import Image
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set")

# Initialize the Gemini API client
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")  # or gemini-1.5-pro

def image_url(img):
    """Convert an image to a base64 URL."""
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return 'data:image/jpeg;base64,' + base64.b64encode(buffered.getvalue()).decode("utf-8")

def estimate_calories(prompt, img):
    """Estimate calories using the Gemini API."""
    message = HumanMessage(content=[
        {'type': 'text', 'text': prompt},
        {'type': 'image_url', 'image_url': image_url(img)}
    ])
    response = model.stream([message])

    # Collect and return the response
    buffer = []
    for chunk in response:
        buffer.append(chunk.content)
    return ''.join(buffer)

if __name__ == "__main__":
    # Example usage
    prompt = "Estimate the calories in this food item."
    
    # Load an image with PIL
    image_path = "/Users/gurmeher/Documents/development/calorie-counter/image.jpg"  # Replace with your image path
    img = Image.open(image_path)
    
    try:
        calorie_estimate = estimate_calories(prompt, img)
        print("Calorie Estimate:", calorie_estimate)
    except Exception as e:
        print("Error:", e)