from fastapi import FastAPI, Request
from agent import interpret_prompt
from executor import execute_steps
from dotenv import load_dotenv
import asyncio
import sys

# if sys.platform.startswith("win"):
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv(".env")

app = FastAPI()


@app.post("/execute")
async def execute(request: Request):
    body = await request.json()
    prompt = body["prompt"]

    steps = interpret_prompt(prompt)
    result = await execute_steps(steps)

    return {"status": "ok", "result": result}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
