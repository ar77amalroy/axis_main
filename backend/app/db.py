from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client.axis_ai

# Collections
users_col = db.users
tasks_col = db.tasks
workflow_steps_col = db.workflow_steps
outputs_col = db.outputs
