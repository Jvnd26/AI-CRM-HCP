import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import InteractionForm from '../components/InteractionForm'
import AIChatPanel from '../components/AIChatPanel'
import { fetchInteractions } from '../store/interactionSlice'

export default function Dashboard() {
  const dispatch = useDispatch()
  const items = useSelector((state) => state.interactions.items)

  useEffect(() => {
    dispatch(fetchInteractions())
  }, [dispatch])

  return (
    <main className="dashboard">
      <header>
        <div>
          <p className="eyebrow">AI-First CRM</p>
          <h1>HCP Interaction Module</h1>
        </div>
        <div className="badge">Live insights • Fast follow-up</div>
      </header>

      <section className="grid-layout">
        <InteractionForm />
        <AIChatPanel />
      </section>

      <section className="panel history">
        <h2>Recent Interactions</h2>
        {items.map((item) => (
          <article key={item.id} className="history-card">
            <strong>{item.hcp_name}</strong>
            <span>{item.interaction_type} • {item.interaction_date}</span>
            <p>{item.summary || 'No summary yet.'}</p>
          </article>
        ))}
      </section>
    </main>
  )
}
