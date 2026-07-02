import time
import asyncio

async def fetch_data(name):
    print(f"Starting fetch for {name}....")
    await asyncio.sleep(2)
    print(f"Done fetching {name}")
    return f"Data from {name}"

async def main():
    start = time.time()
    results = await asyncio.gather(
        fetch_data("LLM API"),
        fetch_data("Database"),
        fetch_data("Vector Store")
    )
    end = time.time()
    print(f"Results: {results}")
    print(f"Total time: {end - start:.2f} seconds")

asyncio.run(main())