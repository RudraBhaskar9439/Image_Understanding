
# Gemini Vision System
A powerful image analysis tool built with Google's Gemini AI that enables detailed image understanding, comparison, and natural language interaction with visual content.

# 🎯 Features
🖼️ Single image analysis with custom prompts

🔄 Image comparison capabilities

📁 Support for multiple image formats

🤖 Powered by Gemini-2.0-flash model

🔍 Natural language image understanding

💾 Local image management


# 📋 Prerequisites

Python 3.8+

Google Gemini API key

Supported image formats: .jpg, .jpeg, .png, .gif, .webp


# 🛠️ Installation
## 1. Clone the repository
```python
git clone <your-repo-url>
cd <your-repo-directory>
```
## 2. Install required packages
```python
pip3 install google-generativeai pillow python-dotenv
```
## 3. Create environment file:
```python
echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env
```


# 📁 Project Structure
```python
.
├── imageUnderstanding.py    # Main application file
├── images/                  # Directory for image files
├── .env                    # Environment variables
└── README.md               # Documentation
```

# 💻 Usage
1. Run the script:
```python
python3 imageUnderstanding.py
```


2. Available commands:

```python
1. analyze <image> [prompt] - Analyze an image with optional prompt
2. compare <image1> <image2> - Compare two images
3. list - Show available images
4. quit - Exit program
```

⚙️ Core Components

Weather Data Retrieval

```python
get_weather(location: str, unit: Literal["celsius", "fahrenheit"])
```
Fetches real-time weather data

Supports temperature unit conversion

Returns comprehensive weather information

## Example Usage:
```python
Enter command: analyze cat.jpg Describe the cat's behavior
Enter command: compare old.jpg new.jpg
Enter command: list
```



# ⚙️ Configuration

Customize these parameters in the code:
```python
SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32
}
```

# 🔒 Security

API key management through environment variables

Input validation for file access

Error handling for API operations


# 🤝 Contributing

Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

# MIT License

Copyright (c) 2024 [Rudra Bhaskar]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Security Note
⚠️ Never commit your .env file or expose your API keys.

Author
[Rudra Bhaskar]