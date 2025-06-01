import os
from pathlib import Path
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
from typing import List
import warnings
warnings.filterwarnings("ignore", message=".*urllib3.*")


# Constants for image handling
BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "images"
SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.gif','.webp')

# Load environment variables
load_dotenv()

# Configure Google API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY in .env file")

# Configure Gemini API with safety settings
genai.configure(api_key=GOOGLE_API_KEY)
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32
}
# Add this after the configuration section and before analyze_image function
def get_image_path(image_name: str) -> Path:
    """
    Get full path of image from images directory
    Args:
        image_name: Name of the image file
    Returns:
        Path object pointing to the image
    Raises:
        ValueError: If image not found or format not supported
    """
    # Try exact name first
    path = IMAGE_DIR / image_name
    if path.exists() and path.suffix.lower() in SUPPORTED_FORMATS:
        return path
        
    # Try adding extensions if no extension provided
    if '.' not in image_name:
        for ext in SUPPORTED_FORMATS:
            path = IMAGE_DIR / f"{image_name}{ext}"
            if path.exists():
                return path
                
    raise ValueError(f"Image '{image_name}' not found in {IMAGE_DIR} or format not supported. "
                    f"Supported formats: {', '.join(SUPPORTED_FORMATS)}")

def analyze_image(image_name: str, prompt: str = "Describe this image in detail.") -> str:
    """Analyze an image using Gemini Pro Vision"""
    try:
        # Get full image path
        image_path = get_image_path(image_name)
        
        # Initialize Gemini Pro Vision model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Load and prepare image
        image = Image.open(image_path)
        
        # Generate response with proper configuration
        response = model.generate_content(
            contents=[
                prompt,
                image
            ],
            generation_config=generation_config,
            stream=False
        )
        
        # Check if response has text
        if response.text:
            return response.text
        else:
            return "No analysis generated for the image."
        
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def compare_images(image1_name: str, image2_name: str) -> str:
    """Compare two images using Gemini-2.0-flash"""
    try:
        # Get image paths
        image1_path = get_image_path(image1_name)
        image2_path = get_image_path(image2_name)
        
        # Initialize model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Load images
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
        
        # Generate comparison
        response = model.generate_content(
            contents=[
                "Compare these two images and describe their differences.",
                image1,
                image2
            ],
            generation_config=generation_config
        )
        
        return response.text
        
    except Exception as e:
        return f"Error comparing images: {str(e)}"

def main():
    # Ensure images directory exists
    IMAGE_DIR.mkdir(exist_ok=True)
    
    print("Gemini Vision System (Type 'quit' to exit)")
    print("\nAvailable commands:")
    print("1. analyze <image> [prompt] - Analyze an image with optional prompt")
    print("2. compare <image1> <image2> - Compare two images")
    print("3. list - Show available images")
    print("4. quit - Exit program")
    
    while True:
        command = input("\nEnter command: ").strip().split()
        
        if not command:
            continue
            
        if command[0].lower() == 'quit':
            break
            
        elif command[0].lower() == 'list':
            images = list_available_images()
            if images:
                print("\nAvailable images:")
                for img in images:
                    print(f"- {img}")
            else:
                print("\nNo images found. Add images to the 'images' directory.")
                
        elif command[0].lower() == 'analyze':
            if len(command) < 2:
                print("Please specify an image name.")
                continue
                
            try:
                image_name = command[1]
                prompt = " ".join(command[2:]) if len(command) > 2 else "Describe this image in detail."
                
                print("\nAnalyzing image...")
                result = analyze_image(image_name, prompt)
                print("\nAnalysis Result:")
                print(result)
            except ValueError as e:
                print(f"\nError: {e}")
                
        elif command[0].lower() == 'compare':
            if len(command) != 3:
                print("Please specify two images to compare.")
                continue
                
            try:
                result = compare_images(command[1], command[2])
                print("\nComparison Result:")
                print(result)
            except ValueError as e:
                print(f"\nError: {e}")
                
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()