
from ollama import chat
from datetime import datetime
import json
from voice_tools import listen, speak

from system_tools import (
    get_battery_status,
    get_system_performance,
    get_system_info
)

from memory_tools import (
    initialize_memory,
    save_memory,
    recall_memory,
    list_memories,
    delete_memory
)
from weather_tools import get_weather
from mac_tools import open_application

MODEL = "qwen3:4b-instruct"

SYSTEM_PROMPT = """
You are JARVIS, an intelligent personal AI assistant.

Personality:
- Calm, professional, witty, and concise.
- Respond naturally, like a sophisticated personal assistant.
- Avoid unnecessarily long responses.

Memory:
- Use save_memory when the user explicitly asks you to remember something.
- Use recall_memory to retrieve a specific saved fact.
- Use list_memories when the user asks what you remember or when the correct memory key is uncertain.
- Use delete_memory only when the user explicitly asks to forget a saved fact.
- Never claim to remember something permanently unless save_memory succeeded.
- Never invent a saved memory.
- Use short, consistent keys such as favorite_color or preferred_editor.

LONG-TERM MEMORY RULES:

1. When the user explicitly asks you to remember something,
   you MUST call save_memory.

2. If the user shares an important lasting personal fact,
   such as their name, age, preferences, or favorite places,
   use save_memory when appropriate.

3. Never claim that you saved a memory unless
   save_memory returned success=True.

4. When the user asks about previously saved information,
   consult the saved long-term memories.

5. If the information is not saved and is not available
   in the current conversation, admit that you don't know.

6. When the user corrects a previously saved fact,
   update it using save_memory.

7. If the user asks you to forget something,
   use delete_memory.

Weather:
- Use get_weather whenever asked for current weather or a supported forecast.
- Never invent weather conditions or temperatures.
- If no city is specified, use Ahmedabad as the default city.
- If a city is specified, use weather tool for that city.
- If the weather service fails, explain that live data is unavailable.

Rules:
- You are running locally on a MacBook.
- Never invent information about the computer.
- Never claim to have executed an action unless a tool did it.
- Respond with only your final answer.
- Do not narrate your reasoning or internal thought process.
"""
TOOLS = [
    get_battery_status,
    get_system_performance,
    get_system_info,
    open_application,
    get_weather,
    save_memory,
    recall_memory,
    list_memories,
    delete_memory
]

TOOL_FUNCTIONS = {
    tool.__name__: tool
    for tool in TOOLS
}

# Store the conversation in memory
conversation = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]





def ask_jarvis(user_message):
    current_time = datetime.now().astimezone()

    saved_memories = list_memories()["memories"]

    memory_text = "\n".join(
        f"- {memory['key']}: {memory['value']}"
        for memory in saved_memories
    )

    conversation[0]["content"] = (
        SYSTEM_PROMPT
        + f"\nCurrent date and time: {current_time.isoformat()}"
        + "\n\nSaved long-term memories:\n"
        + (memory_text or "No memories saved yet.")
    )

    conversation.append({
        "role": "user",
        "content": user_message
    })

    # Allow several rounds of tool calls.
    for _ in range(5):
        response = chat(
            model=MODEL,
            messages=conversation,
            tools=TOOLS,
            stream=False,
            think=False
        )

        conversation.append(
            response.message.model_dump(exclude_none=True)
        )

        tool_calls = response.message.tool_calls or []

        # If no tools were requested, return the answer.
        if not tool_calls:
            raw_answer = response.message.content or ""
            answer = raw_answer.rsplit(
                "</think>", 1
            )[-1].strip()

            return answer or "I couldn't generate a response."

        # Execute all requested tools.
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = tool_call.function.arguments or {}

            function = TOOL_FUNCTIONS.get(function_name)

            if function is None:
                result = {"error": "Unknown tool requested"}
            else:
                try:
                    result = function(**arguments)
                except Exception as error:
                    result = {"error": str(error)}

            print(f"[Tool used: {function_name}]")

            conversation.append({
                "role": "tool",
                "tool_name": function_name,
                "content": json.dumps(result)
            })

    return "I reached my tool execution limit."





initialize_memory()

print("J.A.R.V.I.S. ONLINE")
print("Conversation memory enabled.")
print("Type 'exit' to shut down.\n")


print("\nJ.A.R.V.I.S. VOICE MODE ONLINE")
print("Press Enter to speak.")
print("Type a message to use text mode.")
print("Type 'exit' to shut down.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ("exit", "quit"):
        break

    # Empty input activates the microphone.
    if not user_input:
        try:
            user_input = listen()
        except Exception as error:
            print(f"Microphone error: {error}")
            continue

        if not user_input:
            print("JARVIS: I didn't hear anything.")
            continue

        print(f"You said: {user_input}")

    answer = ask_jarvis(user_input)

    print(f"\nJARVIS: {answer}\n")

    speak(answer)

print("JARVIS: Shutting down. Goodbye.")