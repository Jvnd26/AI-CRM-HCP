import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'

const initialState = {
  items: [],
  loading: false,
  error: '',
  aiSummary: 'Ask the assistant to summarize or search an HCP.',
}

export const fetchInteractions = createAsyncThunk('interactions/fetch', async () => {
  const response = await fetch('http://localhost:8000/interactions')
  if (!response.ok) throw new Error('Failed to fetch interactions')
  return response.json()
})

export const createInteraction = createAsyncThunk('interactions/create', async (payload) => {
  const response = await fetch('http://localhost:8000/interactions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!response.ok) throw new Error('Failed to create interaction')
  return response.json()
})

export const runAgent = createAsyncThunk('interactions/agent', async ({ action, payload }) => {
  const response = await fetch('http://localhost:8000/agent', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action, payload }),
  })
  if (!response.ok) throw new Error('Agent request failed')
  return response.json()
})

const interactionSlice = createSlice({
  name: 'interactions',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchInteractions.pending, (state) => {
        state.loading = true
        state.error = ''
      })
      .addCase(fetchInteractions.fulfilled, (state, action) => {
        state.items = action.payload
        state.loading = false
      })
      .addCase(fetchInteractions.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
      .addCase(createInteraction.fulfilled, (state, action) => {
        state.items.unshift({ id: action.payload.id, ...action.payload })
      })
      .addCase(runAgent.fulfilled, (state, action) => {
        state.aiSummary = action.payload.result?.summary || action.payload.result?.message || JSON.stringify(action.payload.result)
      })
  },
})

export default interactionSlice.reducer
