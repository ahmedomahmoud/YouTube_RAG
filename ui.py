import gradio as gr
from rag import VideoBot

# Initialize the VideoBot
bot = VideoBot()

def handle_youtube_url(url):
    response = bot.add_youtube_video(url)
    return response

def chat_fn(message, history):
    response = bot.query(message)
    return response

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Section A: YouTube Video")
            youtube_url = gr.Textbox(label="YouTube Video URL", placeholder="Paste YouTube link here")
            url_submit = gr.Button("Submit URL")
            url_output = gr.Textbox(label="URL Status", interactive=False)
            url_submit.click(handle_youtube_url, youtube_url, url_output)
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Section B: Chat Interface")
            chat = gr.ChatInterface(
                fn=chat_fn,
                title="Video Chatbot",
                textbox=gr.Textbox(placeholder="Type your message here...", label="Your Message"),
                type="messages",
            )

demo.launch()