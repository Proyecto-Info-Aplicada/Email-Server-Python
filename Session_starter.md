AI Session Starter: Email-Server-Python

Project memory file for AI assistant session continuity. Auto-referenced by custom instructions.
This file should be added to .gitignore to avoid committing session-specific data.

---

Project Context

Project: Email-Server-Python
Type: Python Application
Purpose: [Describe the project purpose and goals]
Status: New project setup
Core Technologies:
- Python
- pip/poetry
- Virtual Environment
- pytest

Available AI Capabilities:
- MCP Servers: [Check and list available MCP servers at session start]
- Documentation: Microsoft docs MCP available for Azure and Microsoft products
- Tools: [Document any specialized MCP tools available for this project]

---

Current State

Build Status: In development
Key Achievement: Project initialized with session continuity
Active Issue: None, ready for development
AI Enhancement: Session configured with MCP server awareness

Architecture Highlights:
- Clean layered architecture: config, connection, controller, dto, interfaces, services, middleware
- Gmail API integration for email sending
- Storage Server integration for PDF retrieval
- Apache Kafka integration (optional) for distributed logging and traceability
- Correlation ID pattern for end-to-end request tracking
- Resilient design: works with or without Kafka (automatic fallback)
- Structured logging with execution time tracking
- Flask middleware for automatic request/response handling

---

Technical Memory

Critical Discoveries:
- Project created with Chat Catalyst session continuity setup
- Custom instructions configured for consistent AI interactions
- Session starter template customized for Python Application development
- MCP server integration enabled for enhanced AI capabilities
- Session file located in .chatcatalyst folder and added to gitignore
- Kafka integration adapted from Node.js Message Server pattern to Python/Flask
- kafka-python-ng chosen for Kafka client (modern fork of kafka-python)
- Asyncio used for Kafka async operations in Flask synchronous context
- Flask 'g' context used for storing correlation_id across request lifecycle

Performance Insights:
- Kafka producer uses acks='all' for guaranteed delivery
- Automatic retry logic (3 retries) for transient failures
- Connection timeout of 3 seconds prevents blocking on Kafka unavailability
- Fallback to console/file logging when Kafka is down (zero downtime)
- Execution time tracking helps identify bottlenecks

Known Constraints:
- Requires Gmail API credentials (credentials.json)
- Depends on external Storage Server for PDF retrieval
- Kafka is optional but recommended for production environments
- Python 3.12+ required for latest features
- Async operations use asyncio.run() due to Flask sync nature

---

Recent Achievements

Date | Achievement
-----|------------
2025-10-22 | Project initialized with session continuity infrastructure
2025-10-22 | Python Application development environment configured
2025-10-22 | MCP server awareness integrated for enhanced AI capabilities
2025-10-22 | Session file configured in .chatcatalyst folder with gitignore protection
2025-10-22 | Session file reviewed by assistant; todo list created and next steps planned
2025-10-22 | Recreated virtual environment (.venv) with Python 3.12
2025-10-22 | Created requirements.txt with Flask, Google API, and other dependencies
2025-10-22 | Successfully installed all dependencies and launched Email Server on port 5001
2025-10-22 | Completed full project refactoring to simplified src/ structure
2025-10-22 | Organized code into: config, connection, controller, dto, interfaces, services
2025-10-22 | Removed old directories (Application, Domain, Infrastructure, Presentation)
2025-10-22 | Updated all imports and verified server runs successfully with new structure
2025-10-22 | Created comprehensive ARCHITECTURE.md with diagrams and technical documentation
2025-10-22 | Generated Postman Collection JSON with all endpoints and examples ready to import
2025-11-19 | ✅ Integrated Apache Kafka for distributed logging and request traceability
2025-11-19 | Created kafka_service.py with optional connection and automatic fallback
2025-11-19 | Implemented request_logger.py for structured logging to Kafka
2025-11-19 | Added correlation_middleware.py for automatic Correlation ID handling
2025-11-19 | Updated controller and service with Kafka logging integration
2025-11-19 | Added execution time tracking and detailed validation flow logging
2025-11-19 | Created comprehensive Kafka documentation (KAFKA_INTEGRATION.md)
2025-11-19 | Server now works with or without Kafka - fully resilient implementation

---

Active Priorities

- [ ] Complete initial project setup
- [ ] Configure build pipeline
- [ ] Set up testing framework
- [ ] Document core architecture decisions
- [ ] Implement first features
- [ ] Identify and utilize relevant MCP servers for this project
- [ ] Verify .chatcatalyst folder is in gitignore

---

Development Environment

Common Commands:
- `python main.py`
- `pip install -r requirements.txt`
- `pytest`
- `python -m venv venv`

Key Files: [Document important project files]
Setup Requirements: [List setup steps for new team members]
AI Tools: [Document useful MCP servers and their capabilities for this project]

---

Gitignore Configuration:
Ensure .chatcatalyst/ is added to .gitignore to keep session data local.
If .gitignore does not exist, create it with: .chatcatalyst/

---

This file serves as persistent project memory for enhanced AI assistant session continuity with MCP server integration.
```

**Entrada sugerida para .gitignore:**
```
# Chat Catalyst session files
.chatcatalyst/