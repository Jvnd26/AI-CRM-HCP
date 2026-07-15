import { useState } from 'react'
import { useDispatch } from 'react-redux'
import { createInteraction, runAgent } from '../store/interactionSlice'

const initialState = {
  hcp_name: '',
  interaction_type: 'Call',
  interaction_date: '',
  interaction_time: '',
  attendees: '',
  topics_discussed: '',
  materials_shared: '',
  outcome: '',
  follow_up_actions: '',
}

export default function InteractionForm() {
  const dispatch = useDispatch()
  const [form, setForm] = useState(initialState)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    await dispatch(createInteraction(form))
    await dispatch(runAgent({ action: 'summarize_interaction', payload: { id: form.id } }))
    setForm(initialState)
  }

  return (
    <form className="panel" onSubmit={handleSubmit}>
      <h2>Log Interaction</h2>
      <div className="grid">
        <label>
          HCP Name
          <input name="hcp_name" value={form.hcp_name} onChange={handleChange} required />
        </label>
        <label>
          Interaction Type
          <select name="interaction_type" value={form.interaction_type} onChange={handleChange}>
            <option>Call</option>
            <option>Meeting</option>
            <option>Email</option>
            <option>Event</option>
          </select>
        </label>
        <label>
          Date
          <input type="date" name="interaction_date" value={form.interaction_date} onChange={handleChange} required />
        </label>
        <label>
          Time
          <input type="time" name="interaction_time" value={form.interaction_time} onChange={handleChange} required />
        </label>
        <label>
          Attendees
          <input name="attendees" value={form.attendees} onChange={handleChange} />
        </label>
        <label>
          Topics Discussed
          <input name="topics_discussed" value={form.topics_discussed} onChange={handleChange} />
        </label>
        <label>
          Materials Shared
          <input name="materials_shared" value={form.materials_shared} onChange={handleChange} />
        </label>
        <label>
          Outcome
          <input name="outcome" value={form.outcome} onChange={handleChange} />
        </label>
        <label className="full">
          Follow-up Actions
          <textarea name="follow_up_actions" value={form.follow_up_actions} onChange={handleChange} />
        </label>
      </div>
      <button type="submit">Save Interaction</button>
    </form>
  )
}
