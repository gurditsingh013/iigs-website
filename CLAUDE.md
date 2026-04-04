# IIGS — Claude Code Instructions

## Project
IIGS — IIGS project

Project directory: `C:/Users/G Singh/Desktop/Claude Ai Projects/IIGS`

---

## Message Routing

Messages from the ARCHON dashboard arrive prefixed: `[RELAY:IIGS] your message`
Strip the prefix and respond normally — Relay handles routing back.

---

## Inter-Agent Communication

To send a message to another agent: POST to `http://localhost:57821/agent/message`
```json
{"from_agent": "claude", "to_agent": "sahiba", "message_type": "info", "content": "..."}
```
