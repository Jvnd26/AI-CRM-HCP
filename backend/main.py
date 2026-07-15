from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

from database import engine, get_db
from models import Base, Interaction
from graph import agent_graph

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-First CRM HCP Module", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InteractionCreate(BaseModel):
    hcp_name: str
    interaction_type: str
    interaction_date: str
    interaction_time: str
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    outcome: Optional[str] = None
    follow_up_actions: Optional[str] = None


class InteractionUpdate(BaseModel):
    hcp_name: Optional[str] = None
    interaction_type: Optional[str] = None
    interaction_date: Optional[str] = None
    interaction_time: Optional[str] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    outcome: Optional[str] = None
    follow_up_actions: Optional[str] = None


class AgentRequest(BaseModel):
    action: str = Field(..., description="One of: log_interaction, edit_interaction, search_hcp, generate_follow_up, summarize_interaction")
    payload: Dict[str, Any] = {}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/interactions", response_model=List[Dict[str, Any]])
def list_interactions(db: Session = Depends(get_db)):
    interactions = db.query(Interaction).order_by(Interaction.created_at.desc()).all()
    return [
        {
            "id": item.id,
            "hcp_name": item.hcp_name,
            "interaction_type": item.interaction_type,
            "interaction_date": str(item.interaction_date),
            "interaction_time": item.interaction_time,
            "attendees": item.attendees,
            "topics_discussed": item.topics_discussed,
            "materials_shared": item.materials_shared,
            "outcome": item.outcome,
            "follow_up_actions": item.follow_up_actions,
            "summary": item.summary,
        }
        for item in interactions
    ]


@app.post("/interactions", response_model=Dict[str, Any])
def create_interaction(payload: InteractionCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    data["interaction_date"] = data["interaction_date"]
    result = agent_graph.invoke({"action": "log_interaction", "payload": data, "db": db})
    return result["result"]


@app.put("/interactions/{interaction_id}", response_model=Dict[str, Any])
def update_interaction(interaction_id: int, payload: InteractionUpdate, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude_unset=True)
    result = agent_graph.invoke({"action": "edit_interaction", "payload": {"id": interaction_id, "changes": data}, "db": db})
    return result["result"]


@app.post("/agent", response_model=Dict[str, Any])
def run_agent(request: AgentRequest, db: Session = Depends(get_db)):
    result = agent_graph.invoke({"action": request.action, "payload": request.payload, "db": db})
    return {"action": request.action, "result": result["result"]}
