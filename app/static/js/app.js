class VirtualNursingAssistant {
    constructor() {
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.messageContainer = document.querySelector('.message-container');
        this.startButton = document.getElementById('startButton');
        this.statusText = document.getElementById('status');
        
        this.initializeSpeechRecognition();
        this.setupEventListeners();
    }

    initializeSpeechRecognition() {
        try {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';

            this.recognition.onresult = (event) => this.handleSpeechResult(event);
            this.recognition.onerror = (event) => this.handleSpeechError(event);
            this.recognition.onend = () => this.handleSpeechEnd();
            this.recognition.onstart = () => this.handleSpeechStart();
        } catch (error) {
            console.error('Speech recognition not supported:', error);
            this.showError('Speech recognition is not supported in this browser. Please use Google Chrome.');
            this.startButton.disabled = true;
        }
    }

    setupEventListeners() {
        this.startButton.addEventListener('click', () => this.toggleListening());
    }

    toggleListening() {
        if (!this.recognition) {
            this.showError('Speech recognition is not supported in this browser. Please use Google Chrome.');
            return;
        }

        if (this.isListening) {
            this.stopListening();
        } else {
            this.startListening();
        }
    }

    startListening() {
        try {
            this.recognition.start();
            this.isListening = true;
            this.startButton.textContent = 'Stop Speaking';
            this.startButton.classList.add('listening');
            this.updateStatus('Listening...');
        } catch (error) {
            console.error('Error starting recognition:', error);
            this.showError('Error starting speech recognition. Please try again.');
            this.stopListening();
        }
    }

    stopListening() {
        try {
            this.recognition.stop();
            this.isListening = false;
            this.startButton.textContent = 'Start Speaking';
            this.startButton.classList.remove('listening');
            this.updateStatus('Click to start speaking');
        } catch (error) {
            console.error('Error stopping recognition:', error);
        }
    }

    handleSpeechStart() {
        this.updateStatus('Listening...');
    }

    async handleSpeechResult(event) {
        const message = event.results[0][0].transcript;
        this.addMessage(message, 'user');
        this.updateStatus('Processing...');
        await this.processMessage(message);
    }

    handleSpeechError(event) {
        console.error('Speech recognition error:', event.error);
        this.showError('Error with speech recognition. Please try again.');
        this.stopListening();
    }

    handleSpeechEnd() {
        if (this.isListening) {
            this.stopListening();
        }
    }

    async processMessage(message) {
        try {
            const response = await fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.error) {
                this.showError(data.error);
                return;
            }

            this.addMessage(data.response, 'assistant');
            this.speakResponse(data.response);
            this.updateStatus('Click to start speaking');
        } catch (error) {
            console.error('Error processing message:', error);
            this.showError('Error processing your message. Please try again.');
            this.updateStatus('Error occurred');
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        
        // Format message with bullet points
        const formattedText = text.split('\n').map(line => {
            if (line.trim().startsWith('•')) {
                return `<li>${line.substring(1).trim()}</li>`;
            }
            return `<p>${line}</p>`;
        }).join('');
        
        messageDiv.innerHTML = formattedText;
        this.messageContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.classList.add('message', 'error');
        errorDiv.textContent = message;
        this.messageContainer.appendChild(errorDiv);
        this.scrollToBottom();
    }

    updateStatus(message) {
        if (this.statusText) {
            this.statusText.textContent = message;
        }
    }

    scrollToBottom() {
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }

    speakResponse(text) {
        try {
            if (this.synthesis.speaking) {
                this.synthesis.cancel();
            }

            // Clean up text for better speech synthesis
            const cleanText = text.replace(/[•\-\*]/g, '').replace(/\n/g, '. ');
            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.lang = 'en-US';
            utterance.rate = 1;
            utterance.pitch = 1;
            
            utterance.onend = () => {
                this.updateStatus('Click to start speaking');
            };
            
            utterance.onerror = (event) => {
                console.error('Speech synthesis error:', event);
                this.updateStatus('Error in speech synthesis');
            };

            this.synthesis.speak(utterance);
            this.updateStatus('Speaking...');
        } catch (error) {
            console.error('Error with speech synthesis:', error);
            this.updateStatus('Error in speech synthesis');
        }
    }
}

// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VirtualNursingAssistant();
});
