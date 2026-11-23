import hashlib
from datetime import date
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr, Field
from google import genai

app = FastAPI(title="Smart Ingredient Meal Planner")
client = genai.Client()

# --- Data Models ---
class UserAuth(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class Ingredient(BaseModel):
    id: int
    name: str
    quantity: str
    expiration_date: Optional[date] = None

class BudgetUpdate(BaseModel):
    weekly_limit: float
    spent_so_far: float

class MealPlanRequest(BaseModel):
    days: int = 3
    dietary_preferences: Optional[str] = "None"

# --- In-Memory MVP Store ---
users_db = {}
pantry_db: List[Ingredient] = [
    Ingredient(id=1, name="Chicken Breast", quantity="2 lbs", expiration_date=date(2026, 11, 24)),
    Ingredient(id=2, name="Spinach", quantity="1 bag", expiration_date=date(2026, 11, 23)),
    Ingredient(id=3, name="Rice", quantity="2 cups", expiration_date=None),
]
budget_db = {"weekly_limit": 50.00, "spent_so_far": 13.00}

# --- Serve Frontend UI ---
@app.get("/")
def serve_ui():
    return FileResponse("index.html")

# --- 1. Auth Endpoints ---
@app.post("/api/auth/register")
def register(user: UserAuth):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    pw_hash = hashlib.sha256(user.password.encode()).hexdigest()
    users_db[user.email] = pw_hash
    return {"message": "Registration successful!", "email": user.email}

@app.post("/api/auth/login")
def login(user: UserAuth):
    pw_hash = hashlib.sha256(user.password.encode()).hexdigest()
    if users_db.get(user.email) != pw_hash:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful!", "email": user.email}

# --- 2. Pantry Endpoints ---
@app.get("/api/pantry", response_model=List[Ingredient])
def get_pantry():
    return sorted(pantry_db, key=lambda x: x.expiration_date or date.max)

@app.post("/api/pantry", response_model=Ingredient)
def add_ingredient(item: Ingredient):
    pantry_db.append(item)
    return item

@app.delete("/api/pantry/{item_id}")
def delete_ingredient(item_id: int):
    global pantry_db
    pantry_db = [i for i in pantry_db if i.id != item_id]
    return {"message": "Deleted"}

# --- 3. Budget Endpoints ---
@app.get("/api/budget")
def get_budget():
    remaining = round(budget_db["weekly_limit"] - budget_db["spent_so_far"], 2)
    return {**budget_db, "remaining": remaining}

@app.post("/api/budget")
def update_budget(data: BudgetUpdate):
    budget_db["weekly_limit"] = data.weekly_limit
    budget_db["spent_so_far"] = data.spent_so_far
    return get_budget()

# --- 4. Meal Plan Generator ---
@app.post("/api/meal-plan")
def create_meal_plan(req: MealPlanRequest):
    if not pantry_db:
        raise HTTPException(status_code=400, detail="Add ingredients to your pantry first.")

    remaining_budget = round(budget_db["weekly_limit"] - budget_db["spent_so_far"], 2)
    items_str = "\n".join(
        [f"- {i.name} ({i.quantity}), expires: {i.expiration_date or 'N/A'}" for i in pantry_db]
    )

    prompt = f"""
    You are a college meal-planning assistant. Create a {req.days}-day meal plan using these listed pantry ingredients (prioritize soonest expiration dates):
    {items_str}

    Remaining weekly grocery budget: ${remaining_budget}
    Dietary preferences: {req.dietary_preferences}

    Keep extra purchases minimal so the student stays under their remaining budget. Format clearly by Day 1, Day 2, etc., and list any cheap missing staples needed.
    """
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return {"plan": response.text}

