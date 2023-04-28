# Rap Therapy App

The Rap Therapy App is a Python application that uses two OpenAI APIs (whisper and GPT4) to provide a unique therapy experience. The user speaks into the app and receives a response from the app in the form of a rap verse. The app allows the user to select their preferred rapper and provides therapy in the form of a rap verse. The user also has the option to save their session transcript to a PDF file.

## Installation

1. Clone the repository to your local machine.
2. Install the necessary libraries by running the following command:
```
pip install -r requirements.txt
```

## Usage

1. Open a terminal window and navigate to the directory where the repository is cloned.
2. Run the following command to launch the app:
```
python therapist.py
```
3. In the app window, enter your OpenAI API key, the name of your preferred rapper, and speak into the microphone to voice your concerns.
4. If you want the system messages to be read out loud, check the "Text-to-Speech" checkbox.
5. If you want to save the transcript to a PDF file, check the "Save to PDF" checkbox and enter a file name.
6. After your session is complete, the transcript will be displayed in the text box.
7. If you selected the "Save to PDF" checkbox, a PDF file will be created with your transcript.

## Requirements

The following libraries are required to run the Rap Therapy App:
* Gradio
* OpenAI
* FPDF

## Contributing

We welcome contributions to the Rap Therapy App! If you have any ideas or suggestions, feel free to open an issue or submit a pull request.

