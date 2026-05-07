# River Crossing: AI Agent Chatbot

**Tier**: Intermediate | **Learning Path**: AI Agents & LLMs  
**Difficulty**: ⭐⭐⭐ (Intermediate) | **Estimated Time**: 3-4 hours

## Overview

Build an intelligent conversational AI agent that can:
- Maintain multi-turn conversation history
- Use external tools (calculator, web search, etc.)
- Reason about user queries and provide helpful responses
- Handle errors gracefully with fallback behavior

This project demonstrates practical patterns for integrating Claude API with tool use and memory management.

## Learning Objectives

By completing this project, you'll understand:
- ✅ How large language models work and how to call them via APIs
- ✅ Prompt engineering and conversation history management
- ✅ Tool/function calling patterns (agent patterns)
- ✅ Error handling and fallback mechanisms
- ✅ Streaming responses and token management
- ✅ Building stateful applications with LLMs

## Prerequisites

- Completed: `projects/guess_the_number/` (Python basics)
- Completed: `projects/data_pipeline_etl/` (Data handling) - recommended but optional
- Understanding of: classes, JSON, HTTP APIs
- API Key: Anthropic Claude API key (get at https://console.anthropic.com)

## Quick Start

### 1. Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set API key (create .env file)
cat > .env << EOF
ANTHROPIC_API_KEY=sk-ant-your-key-here
EOF
```

### 2. Run the Chatbot

```bash
# Interactive CLI mode
python main.py

# Run tests
pytest tests/ -v

# Run with verbose logging
DEBUG=1 python main.py
```

### 3. Example Interaction

```
$ python main.py

AI Agent Chatbot
Type 'exit' to quit, 'clear' to reset conversation

User: What's 15 * 27 + 42?
Agent: I'll calculate that for you.
[Using tool: calculator]
15 * 27 + 42 = 447

User: How far is the Moon from Earth?
Agent: The Moon is approximately 384,400 kilometers (238,855 miles) from Earth...
[Using tool: web_search]

User: exit
Goodbye!
```

## Project Structure

```
projects/ai_agent_chatbot/
├── README.md                    # This file
├── requirements.txt             # Project dependencies
├── .env.example                 # Environment variables template
├── main.py                      # CLI entry point
├── agent.py                     # Core agent implementation
├── tools.py                     # Tool definitions (calculator, search, etc.)
├── config.py                    # Configuration management
├── utils.py                     # Helper functions
├── tests/
│   ├── test_agent.py           # Agent unit tests
│   ├── test_tools.py           # Tool integration tests
│   └── test_main.py            # CLI tests
└── notebooks/
    └── chatbot_demo.ipynb      # Interactive Jupyter demo
```

## Key Concepts

### 1. **LLM Integration**
Connect to Claude API and manage conversations:
```python
from anthropic import Anthropic

client = Anthropic(api_key="your-key")
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=conversation_history
)
```

### 2. **Tool Use Pattern**
Enable the agent to use external tools:
```python
tools = [
    {
        "name": "calculator",
        "description": "Perform math calculations",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string"}
            }
        }
    }
]

response = client.messages.create(
    model="claude-opus-4-7",
    tools=tools,
    messages=conversation_history
)
```

### 3. **Conversation Memory**
Maintain conversation state across multiple turns:
```python
conversation_history = []
conversation_history.append({"role": "user", "content": user_input})
# ... get response ...
conversation_history.append({"role": "assistant", "content": response})
```

### 4. **Error Handling**
Gracefully handle API errors and invalid tool calls:
```python
try:
    response = client.messages.create(...)
except RateLimitError:
    print("Rate limited. Please try again later.")
except InvalidRequestError as e:
    print(f"Invalid request: {e}")
```

## Extended Features (Bonus)

- ✨ **Streaming Responses**: Stream tokens as they're generated
- ✨ **Conversation Persistence**: Save/load conversation history to file
- ✨ **System Prompts**: Customize agent personality and behavior
- ✨ **Tool Chains**: Combine multiple tools for complex tasks
- ✨ **Web Interface**: Build Flask/FastAPI interface
- ✨ **Cost Tracking**: Monitor API token usage and costs

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test
pytest tests/test_agent.py::TestAgent::test_basic_conversation -v
```

## Troubleshooting

**Issue**: "Invalid API key"
- Solution: Check `.env` file and API key is valid at https://console.anthropic.com

**Issue**: "Module 'anthropic' not found"
- Solution: Install dependencies: `pip install -r requirements.txt`

**Issue**: "Tool not found" error
- Solution: Ensure tool is defined in `tools.py` and registered in agent

## Resources

- 📖 [Anthropic Claude API Documentation](https://docs.anthropic.com)
- 📖 [Tool Use Guide](https://docs.anthropic.com/messages/tool-use)
- 📖 [Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-a-bot/tool-use)
- 🎥 [Building Agents with Claude](https://www.youtube.com/@AnthropicAI)

## Learning Path

1. **Complete**: `projects/guess_the_number/` - Python basics
2. **Next**: This project (AI Agent Chatbot)
3. **Then**: `projects/data_pipeline_etl/` - Data processing
4. **Advanced**: `projects/ml_recommendation/` - Machine learning
5. **Expert**: `projects/web_api_service/` - Full-stack application

## Next Steps

After completing this project:
- Build a specialized agent (customer support, code reviewer, etc.)
- Integrate with web framework (Flask/FastAPI)
- Deploy to production (Vercel, Heroku, AWS)
- Optimize prompts and tool definitions
- Explore multi-agent systems

## Contributing

Have improvements? Submit a PR with:
- Feature or bug fix
- Tests for new functionality
- Updated documentation

See `CONTRIBUTING.md` for guidelines.
