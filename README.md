# Virtual Nursing Assistant

An AI-powered medical consultation system with voice interaction capabilities.

## Features

- 🎤 Voice-to-voice interaction
- 🏥 Real-time symptom analysis
- 🚨 Emergency condition detection
- 💊 Medical recommendations
- 🗣️ Natural language processing
- 📱 Responsive web interface

## Tech Stack

- **Backend:**
  - Python 3.8+
  - FastAPI
  - NLTK for natural language processing
  - scikit-learn for analysis

- **Frontend:**
  - HTML5
  - CSS3
  - JavaScript (ES6+)
  - Web Speech API

## Prerequisites

- Python 3.8 or higher
- Google Chrome browser (recommended for best speech recognition support)
- Internet connection
- Microphone

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd saif
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Open in browser:
   - Navigate to http://127.0.0.1:8000
   - Use Google Chrome for best experience

## Usage Guide

1. **Starting a Consultation:**
   - Click the "Start Speaking" button
   - Allow microphone access when prompted
   - Speak your symptoms clearly

2. **Understanding Responses:**
   - The assistant will analyze your symptoms
   - You'll receive voice and text responses
   - Recommendations will be provided
   - Emergency warnings if applicable

3. **Example Queries:**
   - "I have a headache and fever"
   - "I'm experiencing a cough"
   - "My throat is sore"

4. **Emergency Detection:**
   - The system recognizes emergency conditions
   - Provides immediate warnings
   - Recommends seeking urgent care when necessary

## Project Structure

```
saif/
├── app/
│   ├── models/
│   │   └── medical_kb.py     # Medical knowledge base
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css     # Application styling
│   │   └── js/
│   │       └── app.js        # Frontend logic
│   ├── templates/
│   │   └── index.html        # Main application template
│   └── main.py               # FastAPI application
├── requirements.txt          # Project dependencies
└── README.md                # Documentation
```

## Key Features

1. **Voice Interaction:**
   - Real-time speech recognition
   - Natural text-to-speech responses
   - Clear audio feedback

2. **Medical Analysis:**
   - Symptom recognition
   - Condition assessment
   - Emergency detection
   - Evidence-based recommendations

3. **User Interface:**
   - Modern, clean design
   - Responsive layout
   - Real-time status updates
   - Error handling

4. **Security:**
   - No personal data storage
   - Local processing
   - Clear medical disclaimers

## Browser Compatibility

- **Recommended:** Google Chrome
- **Required Features:**
  - Web Speech API
  - ES6+ JavaScript
  - Modern CSS support

## Development

- **Code Style:** PEP 8 (Python), Modern JS
- **Architecture:** MVC pattern
- **API:** RESTful endpoints
- **Testing:** Manual testing implemented

## Disclaimer

This application is for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers.

## Version

1.0.0 - Initial Release

## License

MIT License - Feel free to use and modify as needed.
