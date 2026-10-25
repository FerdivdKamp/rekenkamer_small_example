import { useState, type FormEvent } from 'react'
import { createRoot } from 'react-dom/client'
import './style.css'

type Begroeting = { boodschap: string }
type Problem = { detail?: string }

function App() {
  const [naam, setNaam] = useState('')
  const [boodschap, setBoodschap] = useState('')
  const [fout, setFout] = useState('')
  const [laden, setLaden] = useState(false)

  async function begroet(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const invoer = naam.trim()
    if (!invoer) {
      setBoodschap('')
      setFout('Vul een naam in.')
      return
    }

    setLaden(true)
    setBoodschap('')
    setFout('')

    try {
      const response = await fetch(`/v1/begroetingen/${encodeURIComponent(invoer)}`)
      if (!response.ok) {
        const problem = (await response.json()) as Problem
        throw new Error(problem.detail || `De aanvraag mislukte (${response.status}).`)
      }
      const begroeting = (await response.json()) as Begroeting
      setBoodschap(begroeting.boodschap)
    } catch (error) {
      setFout(error instanceof Error ? error.message : 'De begroeting kon niet worden opgehaald.')
    } finally {
      setLaden(false)
    }
  }

  return (
    <main className="kaart">
      <h1>Begroetingen</h1>
      <p>Vul je naam in voor een persoonlijke begroeting.</p>
      <form onSubmit={begroet}>
        <label htmlFor="naam">Naam</label>
        <div className="invoerregel">
          <input
            id="naam"
            name="naam"
            type="text"
            value={naam}
            onChange={(event) => setNaam(event.target.value)}
            autoComplete="given-name"
          />
          <button type="submit" disabled={laden}>{laden ? 'Ophalen…' : 'Begroet'}</button>
        </div>
      </form>
      <p className="resultaat" role="status" aria-live="polite">
        {fout || boodschap}
      </p>
    </main>
  )
}

createRoot(document.getElementById('root')!).render(<App />)
