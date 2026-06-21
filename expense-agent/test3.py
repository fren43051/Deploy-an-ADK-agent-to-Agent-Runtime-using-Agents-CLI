import asyncio
from google.adk.runners import InMemoryRunner
from google.genai import types
from app.agent import app

async def main():
    runner = InMemoryRunner(app=app)
    session = await runner.session_service.create_session(app_name="app", user_id="test")
    
    async for event in runner.run_async(
        user_id="test",
        session_id=session.id,
        new_message=types.Content(role="user", parts=[types.Part.from_text(text="I bought a flight to NY for $850")])
    ):
        print("EVENT DUMP:", vars(event))
        
if __name__ == "__main__":
    asyncio.run(main())
