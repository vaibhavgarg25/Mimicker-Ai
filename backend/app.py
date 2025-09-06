import asyncio
from flask import Flask

app = Flask(__name__)

@app.route("/")
async def home():
    await asyncio.sleep(1)  # simulate async I/O
    return {"message": "Hello from async Flask with Uvicorn!"}

@app.route("/sync")
def sync_route():
    return {"message": "This is synchronous."}

if __name__ == "__main__":
    # For dev only (not production)
    app.run(debug=True)

