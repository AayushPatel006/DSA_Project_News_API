import asyncio
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

# load news data
with open("news.json") as f:
    NEWS = json.load(f)

queue = asyncio.Queue()
index = 0  # track which news to send next
current_news = None  # track the last news item sent


async def news_generator():
    """
    Background task that adds one news item to the queue every 3 seconds.
    Runs forever.
    """
    global index
    global current_news
    while True:
        current_news = NEWS[index % len(NEWS)]  # loop through list
        index += 1
        await asyncio.sleep(3)


@app.on_event("startup")
async def start_background_task():
    """Start news generator when server starts."""
    asyncio.create_task(news_generator())

@app.get("/live")
async def live_feed():
    global current_news
    return current_news
