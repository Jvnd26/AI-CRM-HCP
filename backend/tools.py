import os
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from groq import Groq
from dotenv import load_dotenv

from models import Interaction

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))


def log_interaction(db: Session, payload: Dict[str, Any]) -> Dict[str, Any]:
    interaction = Interaction(**payload)
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return {"id": interaction.id, "message": "Interaction logged successfully"}


def edit_interaction(db: Session, interaction_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise ValueError("Interaction not found")
    for key, value in payload.items():
        setattr(interaction, key, value)
    db.commit()
    db.refresh(interaction)
    return {"id": interaction.id, "message": "Interaction updated successfully"}


def search_hcp(db: Session, query: str) -> List[Dict[str, Any]]:
    results = db.query(Interaction).filter(Interaction.hcp_name.contains(query)).all()
    return [
        {
            "id": item.id,
            "hcp_name": item.hcp_name,
            "interaction_type": item.interaction_type,
            "interaction_date": str(item.interaction_date),
            "summary": item.summary,
        }
        for item in results
    ]


def generate_follow_up(db: Session, interaction_id: int) -> Dict[str, Any]:
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise ValueError("Interaction not found")
    draft = (
        f"Follow-up for {interaction.hcp_name}: "
        f"Please share the {interaction.topics_discussed or 'latest update'} and confirm the next meeting."
    )
    return {"message": draft}


def summarize_interaction(db: Session, interaction_id: int) -> Dict[str, Any]:
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise ValueError("Interaction not found")

    if interaction.summary:
        return {"summary": interaction.summary}

    if client.api_key:
        try:
            response = client.chat.completions.create(
                model="gemma2-9b-it",
                messages=[
                    {
                        "role": "system",
                        "content": "Summarize the interaction as a concise CRM note.",
                    },
                    {
                        "role": "user",
                        "content": f"HCP: {interaction.hcp_name}\nType: {interaction.interaction_type}\nOutcome: {interaction.outcome}\nTopics: {interaction.topics_discussed}",
                    },
                ],
                temperature=0.2,
            )
            summary = response.choices[0].message.content
        except Exception:
            summary = "AI summary unavailable; stored interaction details are available."
    else:
        summary = "AI summary unavailable; stored interaction details are available."

    interaction.summary = summary
    db.commit()
    return {"summary": summary}
