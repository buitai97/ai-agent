import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import argparse
load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
def main():
    parser = argparse.ArgumentParser(description="Chatbox")
    parser.add_argument("user_prompt", type=str, help="The prompt to send to the model")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages
    )
    if response.usage_metadata:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(f"Response: {response.text}")
    else:
        raise RuntimeError("Usage metadata is not available in the response.")
if __name__ == "__main__":
    main()
