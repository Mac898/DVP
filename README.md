# Discord-based voice chat for minecraft
- Global voice
- Local proximity voice including volume changes.
- Uses local discord api via IPC: GameSDK
- Very early, currently broken
- Built in Python 3.10

## Built into 3 pieces
- Backend: Web & WS host that communicates with:
- Frontend: GUI application that simply runs in the system tray to allow remote communication over HTTPS websockets to the Discord IPC API (GameSDK) in a secure way. Is active only when joining a server with the system enabled.
- Serverend: Java/Kotlin implementation of code that allows communication of player position, server status to the backend. Handles chat messaging for setup & joining VC. Communicates securely via HTTPS websockets to Backend.