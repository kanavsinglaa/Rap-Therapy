import gradio as gr
import openai
import subprocess
from fpdf import FPDF
import datetime

messages = [
    {
        "role": "system",
        "content": "You are a therapist. Respond as if you were a rapper Baby Keem.",
    }
]

chat_transcript = ""


def transcribe(openai_key, audio, rapper_name, tts_enabled, save_to_pdf):
    global messages, chat_transcript

    openai.api_key = openai_key
    new_prompt = (
        "You are a therapist. Respond in 1-2 rap verses in less than 20 words that rhyme super well as if you were the rapper "
        + rapper_name
    )
    if messages[0]["content"] != new_prompt:
        messages[0]["content"] = new_prompt

    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    messages.append({"role": "user", "content": transcript["text"]})
    chat_transcript += "You: " + transcript["text"] + "\n\n"

    response = openai.ChatCompletion.create(model="gpt-4", messages=messages)
    system_message = response["choices"][0]["message"]["content"]

    if tts_enabled:
        subprocess.call(["say", system_message])
    messages.append({"role": "assistant", "content": system_message})
    chat_transcript += rapper_name + ": " + system_message + "\n\n"

    pdf_file_path = generate_pdf(chat_transcript, save_to_pdf)

    return chat_transcript, pdf_file_path


def generate_pdf(chat_transcript, save_to_pdf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    if save_to_pdf:
        pdf.cell(200, 10, txt="Rap Therapy Session Transcript", ln=1, align="C")
        pdf.cell(
            200,
            10,
            txt=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ln=1,
            align="C",
        )
        pdf.cell(0, 10, "", ln=1)
        lines = chat_transcript.split("\n\n")
        for line in lines:
            if line.startswith("You: "):
                pdf.set_text_color(100, 0, 0)  # red
                response = line
                while len(response) > 0:
                    # Split therapist's response into multiple lines
                    max_len = 100  # Maximum characters per line
                    if len(response) <= max_len:
                        pdf.cell(0, 10, txt=response, ln=1)
                        response = ""
                    else:
                        space_idx = response.rfind(" ", 0, max_len)
                        if space_idx == -1:
                            space_idx = max_len
                        pdf.cell(0, 10, txt=response[:space_idx], ln=1)
                        response = response[space_idx + 1 :]
            else:
                response_lines = line.split("\n")
                for line in response_lines:
                    pdf.set_text_color(0, 100, 0)  # green for therapist response
                    pdf.cell(0, 10, txt=line, ln=1)

        file_name = f"rap_therapy_transcript_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
        file_path = f"./{file_name}"
    else:
        file_path = f"./empty_transcript"

    pdf.output(file_path)
    return file_path


def launch_app():
    openai_key_input = gr.inputs.Textbox(
        label="OpenAI API Key",
        placeholder="Enter your OpenAI API Key here...",
    )
    rapper_name_input = gr.inputs.Textbox(
        label="Therapist",
        placeholder="Who do you want therapy from? (ex- Jay-Z, Baby Keem)",
    )
    audio_input = gr.inputs.Audio(
        label="Voice your concerns... (for eg. say I have been really sad lately, what should I do to feel better?)",
        source="microphone",
        type="filepath",
    )
    save_to_pdf_input = gr.inputs.Checkbox(
        label="Save chat transcript to PDF file",
        default=True,
    )

    tts_checkbox = gr.inputs.Checkbox(
        label="Enable text-to-speech for your therapist rapper",
        default=False,
    )

    output_text = gr.outputs.Textbox(label="Transcripts from your session")
    output_file = gr.outputs.File(label="Download chat transcript as PDF")

    gr.Interface(
        fn=transcribe,
        inputs=[
            openai_key_input,
            audio_input,
            rapper_name_input,
            tts_checkbox,
            save_to_pdf_input,
        ],
        outputs=[output_text, output_file],
        title="RapTherapy",
        description="### Welcome to Rap Therapy!\n\n"
        "In this app, you can vent to a virtual therapist who responds to you like your favorite rapper.\n\n"
        "#### Here's how to use the app:\n\n"
        "1. Enter your OpenAI API key.\n"
        "2. Type the name of the rapper you want therapy from.\n"
        "3. Click on the 'Voice your concerns...' button to start recording your message. "
        "You will have 60 seconds to record your message.\n"
        "4. Repeat steps 2 and 3 as many times as you want.\n"
        "5. If you want to read the system messages instead of hearing them out loud, uncheck the 'Enable text-to-speech' option.\n"
        "6. Click on the 'Save transcript to PDF' button to save the transcripts of your session for future reference.\n"
        "7. Click the 'Submit' button to start the session.\n\n"
        "Enjoy your therapy session!",
        article="This is just a MVP demo. A lot can be added on top of this for better UI & functionality.",
    ).launch()


if __name__ == "__main__":
    launch_app()
