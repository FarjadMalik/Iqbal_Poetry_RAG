"""Gradio interface for the Iqbal Poetry RAG application."""

import gradio as gr
from app.config import APP_NAME, GRADIO_THEME, GRADIO_SERVER_PORT

def process_query(question, history):
    """Process user query through the RAG system."""
    try:
        response, _ = rag_system.query_rag(question)
        return response, _
    except Exception as e:
        error_message = f"Error processing query: {str(e)}"
        print(f"Error in process_query: {error_message}")  # Log error for debugging
        return error_message

def handle_feedback(question, response, feedback, comment):
    """Handle user feedback submission."""
    if not question or not response:
        return "Feedback not logged - missing data"
    
    # Since feedback logging is commented out in IqbalRAGSystem, just return success
    return "Feedback logging is currently disabled"

def create_gradio_interface():
    """Create and configure the Gradio interface."""
    with gr.Blocks(theme=GRADIO_THEME, title=APP_NAME) as app:
        gr.Markdown(f"# {APP_NAME}")
        gr.Markdown("""
        Welcome to the Iqbal Poetry RAG system! Ask questions about Iqbal's philosophical poetry.
        The system will search through Iqbal's poems and provide relevant answers based on the content.
        """)
        
        chatbot = gr.Chatbot(
            label="Conversation",
            height=500,
            type="messages",  # Explicitly set type to 'messages'
            show_label=True,
            container=True
        )
        
        with gr.Row():
            with gr.Column(scale=4):
                input_question = gr.Textbox(
                    label="Your Question",
                    placeholder="Ask about philosophical concepts in Iqbal's poetry...",
                    lines=3,
                    show_label=True
                )
            
            with gr.Column(scale=1):
                submit_btn = gr.Button("Submit", variant="primary")
        
        with gr.Accordion("Provide Feedback", open=False):
            feedback_rating = gr.Radio(
                ["Helpful", "Partially Helpful", "Incorrect"],
                label="Feedback Rating",
                value="Helpful"
            )
            
            feedback_comment = gr.Textbox(
                label="Additional Comments",
                placeholder="Provide detailed feedback...",
                lines=3
            )
            
            feedback_btn = gr.Button("Submit Feedback")
            feedback_status = gr.Markdown()
        
        gr.Examples(
            examples=[
                "Explain Iqbal's concept of Khudi",
                "Analyze the symbolism in 'The Himalayas' poem",
                "Compare Iqbal's view of nature with Romantic poets",
                "What is Iqbal's view on Western materialism?",
                "Discuss the influence of Rumi on Iqbal's philosophy",
                "What are the main themes in 'The Secrets of the Self'?",
                "How does Iqbal view the relationship between God and man?"
            ],
            inputs=input_question
        )
        
        def user_input(user_message, history):
            if not user_message.strip():
                return "", history
            # Convert to new message format
            history = history + [{"role": "user", "content": user_message}]
            return "", history
        
        def bot_response(history):
            user_message = history[-1]["content"]
            bot_message, _ = process_query(user_message, history)
            # Convert to new message format
            history = history + [{"role": "assistant", "content": bot_message}]
            return history
        
        submit_btn.click(
            user_input,
            [input_question, chatbot],
            [input_question, chatbot],
            queue=False
        ).then(
            bot_response,
            chatbot,
            chatbot
        )
        
        input_question.submit(
            user_input,
            [input_question, chatbot],
            [input_question, chatbot],
            queue=False
        ).then(
            bot_response,
            chatbot,
            chatbot
        )
        
        feedback_btn.click(
            fn=handle_feedback,
            inputs=[input_question, chatbot, feedback_rating, feedback_comment],
            outputs=feedback_status
        )
        
        return app

def launch_gradio_app(system=None):
    """Launch the Gradio application."""
    global rag_system
    if system is not None:
        globals()['rag_system'] = system
    
    app = create_gradio_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=GRADIO_SERVER_PORT,
        share=False,
        show_error=True  # Show detailed error messages in the UI
    )
