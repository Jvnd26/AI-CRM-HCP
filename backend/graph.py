from typing import Any, Dict, List
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from sqlalchemy.orm import Session

from tools import (
    edit_interaction,
    generate_follow_up,
    log_interaction,
    search_hcp,
    summarize_interaction,
)


class AgentState(dict):
    action: str
    payload: Dict[str, Any]
    db: Session
    result: Any


def run_agent(state: AgentState) -> AgentState:
    action = state.get("action")
    payload = state.get("payload", {})
    db = state.get("db")

    if action == "log_interaction":
        result = log_interaction(db, payload)
    elif action == "edit_interaction":
        result = edit_interaction(db, int(payload.get("id", 0)), payload.get("changes", {}))
    elif action == "search_hcp":
        result = search_hcp(db, payload.get("query", ""))
    elif action == "generate_follow_up":
        result = generate_follow_up(db, int(payload.get("id", 0)))
    elif action == "summarize_interaction":
        result = summarize_interaction(db, int(payload.get("id", 0)))
    else:
        raise ValueError(f"Unsupported action: {action}")

    state["result"] = result
    return state


def build_graph() -> CompiledStateGraph:
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", run_agent)
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)
    return workflow.compile()


agent_graph = build_graph()
