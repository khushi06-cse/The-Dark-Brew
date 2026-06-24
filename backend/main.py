import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
from database import init_db, get_db_connection

# Load .env variables
load_dotenv()

app = FastAPI(title="The Dark Brew - Backend Engine")

# CORS Handle karein taaki HTML file bina dikkat connect ho sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Local HTML testing ke liye full open
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database structure on startup
init_db()

# Check Groq Key
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    print("WARNING: GROQ_API_KEY nahi mili! .env check karein.")

client = Groq(api_key=GROQ_KEY)

# Request schema for frontend chat
class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    # 1. SQLite Database se menu fetch karein taaki AI ko dynamic context mile
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT item_name, category, price, description FROM menu")
    menu_rows = cursor.fetchall()
    conn.close()
    
    menu_context = "\n".join([
        f"- {m['item_name']} [{m['category']}]: ₹{m['price']} - {m['description']}" 
        for m in menu_rows
    ])
    
    # 2. GenZ Bilingual System Prompt Configuration
    system_prompt = f"""
    You are BrewAI Assistant, the elite host of 'The Dark Brew | Cyber Cafe & AI Lounge'.
    The user can talk in English, Hindi, or Hinglish. Always talk in an energetic, premium dark cyber aesthetic vibe. Use cool emojis.
    
    CRITICAL RULE: If the user asks or demands for something sweet, cold, or meetha/thanda (e.g., 'kuch thanda chahiye', 'suggest me something sweet', 'meetha dikhao'), 
    you MUST look at the cafe menu provided below and suggest exactly 2-3 matching drinks or desserts with their exact prices.
    
    THE DARK BREW MENU:
    {menu_context}
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
            ],
            temperature=0.7
        )
        # Frontend expect kar raha hai: data.reply
        return {"reply": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq AI Error: {str(e)}")

@app.post("/api/order")
async def order_endpoint(item_name: str = Query(...), quantity: int = Query(...)):
    # Aapka frontend parameters query me bhej raha hai: /api/order?item_name=...&quantity=...
    if not item_name or quantity <= 0:
        raise HTTPException(status_code=400, detail="Invalid order details")
        
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (item_name, quantity) VALUES (?, ?)", 
            (item_name, quantity)
        )
        conn.commit()
        conn.close()
        
        # Frontend expect kar raha hai ek success alert message
        return {"message": f"Order Received! Your code/fudge session is active for {quantity}x {item_name}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")