import asyncio
import websockets
import json
import os
from dotenv import load_dotenv
import aiohttp

load_dotenv()

GEMINI_API_KEY = 'AIzaSyCR1XaDcTAYZ3_Em_WVOkUt5LnYuXJTVtk'

async def get_faq_answer(question):
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
            
            prompt = f"""
            You are RABIc's AI assistant. RABIc is an AI-powered data analysis platform.
            Please provide a clear, helpful response to this question about RABIc's services:
            
            Question: {question}
            
            Provide a response that is:
            1. Informative but concise (2-3 sentences)
            2. Focused on RABIc's capabilities
            3. Professional and helpful in tone
            """
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }
            
            async with session.post(url, json=payload) as response:
                data = await response.json()
                if response.status != 200:
                    return "Sorry, there was an error with the API request."
                
                if 'candidates' in data and data['candidates'][0]['content']['parts'][0]['text']:
                    return data['candidates'][0]['content']['parts'][0]['text'].strip()
                return "Sorry, couldn't generate an answer."
    except Exception as e:
        return f"Error: {str(e)}"

async def handle_websocket(websocket):
    print("\n=== FAQ WebSocket Server Running ===")
    try:
        async for message in websocket:
            data = json.loads(message)
            question = data.get('question')
            
            if question:
                print("\n📝 Question:", question)
                answer = await get_faq_answer(question)
                print("🤖 Answer:", answer)
                print("-" * 50)
                
                await websocket.send(json.dumps({
                    'answer': answer,
                    'questionId': data.get('questionId')
                }))
    except websockets.exceptions.ConnectionClosed:
        print("\n❌ WebSocket connection closed")
    except Exception as e:
        print(f"\n❌ Error: {e}")

async def main():
    async with websockets.serve(handle_websocket, "localhost", 8765):
        print("\n🚀 FAQ Server started on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main()) 