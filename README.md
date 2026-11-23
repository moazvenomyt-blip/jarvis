# JARVIS AI

A Python Flask application with a responsive futuristic web interface, Groq chat integration, and ElevenLabs speech endpoint.

## Important hosting note
GitHub stores the source code but GitHub Pages cannot run Python or keep API keys secret. Deploy this Flask app to a Python host (for example, Render) and keep the repository on GitHub.

## Environment variables
Set these in your hosting provider's private environment settings:
- `GROQ_API_KEY` — a newly rotated Groq key
- `ELEVENLABS_API_KEY` — a newly rotated ElevenLabs key
- `ELEVENLABS_VOICE_ID` — your selected voice ID
- `GROQ_MODEL` — optional; defaults to `llama-3.3-70b-versatile`

Never commit API keys to GitHub.

## Run command
`gunicorn app:app`

## Local run (optional)
`pip install -r requirements.txt`
`python app.py`

## Current functionality
- Responsive dashboard and chat interface
- Server-side Groq chat endpoint
- Server-side ElevenLabs speech endpoint
- Browser speech recognition when supported
- YouTube, GitHub and browser shortcuts
- Browser reminder (page must remain open)

This is a foundation, not a claim that every requested feature is already implemented. Device controls, persistent alarms, full OSINT workflows, file operations, and integrations require separate permission-aware modules.
