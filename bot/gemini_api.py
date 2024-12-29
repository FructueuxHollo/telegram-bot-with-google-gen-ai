from google import genai
import asyncio
from config import GEMINI_API_KEY

# Initialize the Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

async def process_with_gemini(input_text: str):
    """
    Process a prompt with Gemini AI asynchronously
    
    Args:
        input_text (str): The user's input text to process
        
    Returns:
        str: The generated response text
    """
    try:
        # Run the Gemini API call in a thread pool to avoid blocking
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=input_text
            )
        )
        
        # Extract the text from the response
        # Access the first candidate's text content
        return response.candidates[0].content.parts[0].text

    except Exception as e:
        print(f"Error in Gemini API call: {str(e)}")
        raise