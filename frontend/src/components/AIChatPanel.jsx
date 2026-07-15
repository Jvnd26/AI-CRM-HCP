import { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { runAgent } from '../store/interactionSlice'

export default function AIChatPanel() {
  const dispatch = useDispatch()
  const [query, setQuery] = useState('')
  const aiSummary = useSelector((state) => state.interactions.aiSummary)

  const handleSubmit = async (e) => {
    e.preventDefault()
    await dispatch(runAgent({ action: 'search_hcp', payload: { query } }))
    await dispatch(runAgent({ action: 'generate_follow_up', payload: { id: 1 } }))
  }

  return (
    <div className="panel chat-panel">
      <h2>AI Assistant</h2>
      <p className="muted">Summaries, search, and follow-up drafting for HCP conversations.</p>
      <form onSubmit={handleSubmit}>
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search HCP name" />
        <button type="submit">Ask AI</button>
      </form>
      <div className="assistant-output">{aiSummary}</div>
    </div>
  )
}
