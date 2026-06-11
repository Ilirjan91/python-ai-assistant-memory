import json
import os
from openai import OpenAI
from dotenv import load_dotenv

SYSTEM_PROMPT = """
You are a helpful AI assistant.

You can understand and respond in many languages, including German, English, Albanian, Italian, Spanish and French.

Always detect the language of the user and answer in the same language.
If the user mixes languages, answer in the main language used by the user.

Explain things clearly and simply.
If the user asks about code, explain mistakes step by step and give corrected examples.
If the user asks for a translation, translate naturally and clearly.
If you are unsure, say honestly that you are not sure.

Be friendly, practical and beginner-friendly.
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

MEMORY_FILE = os.path.join(BASE_DIR, "memory.json")
OLLAMA_MODEL = "llama3.2"
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)


def get_ai_response(client, conversation_history, model):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=conversation_history,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Fehler bei der KI-Anfrage: {e}"


def main():
    print("🤖 KI-Assistant")
    print("---------------")
    print("Welches Modell möchtest du verwenden?")
    print("1. LLaMA 3.2 (lokal)")
    print("2. LLaMA 3.3 (GROQ Cloud)")

    wahl = input("Deine Wahl (1 oder 2): ").strip()

    if wahl == "1":
        client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
        )

        model = OLLAMA_MODEL
        print("LLaMA 3.2 wird verwendet...")

    elif wahl == "2":
        if not GROQ_API_KEY:
            print("Fehler: GROQ_API_KEY fehlt in der .env Datei.")
            return

        client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=GROQ_API_KEY,
        )

        model = GROQ_MODEL
        print("LLaMA 3.3 wird verwendet...")

    else:
        print("Ungültige Wahl. Bitte wähle 1 oder 2.")
        return

    memory = load_memory()
    conversation_history = memory.get("conversation_history", [])

    if not conversation_history:
        conversation_history = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

    if "name" in memory:
        print(f"Willkommen zurück, {memory['name']}!")
    else:
        print("Hallo! Ich bin dein KI-Assistant.")

    print("Tippe /help für Befehle oder /exit zum Beenden.\n")

    while True:
        user_input = input("Du: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit", "/exit"]:
            print("Auf Wiedersehen!")
            break

        if user_input.lower() == "/help":
            print("""
Befehle:
/help      Hilfe anzeigen
/reset     Verlauf löschen
/history   Verlauf anzeigen
/model     Aktuelles Modell anzeigen
/exit      Beenden
""")
            continue

        if user_input.lower() == "/reset":
            conversation_history = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ]
            memory["conversation_history"] = conversation_history
            save_memory(memory)
            print("Chatverlauf wurde gelöscht.")
            continue

        if user_input.lower() == "/model":
            print(f"Aktuelles Modell: {model}")
            continue

        if user_input.lower() == "/history":
            messages = [
                msg for msg in conversation_history
                if msg["role"] in ["user", "assistant"]
            ]

            if not messages:
                print("Noch kein Verlauf vorhanden.")
            else:
                for message in messages[-10:]:
                    role = message["role"]
                    content = message["content"]
                    print(f"{role}: {content}")
            continue

        if "mein name ist" in user_input.lower():
            name = user_input.lower().replace("mein name ist", "").strip().title()
            memory["name"] = name
            save_memory(memory)
            print(f"Schön dich kennenzulernen, {name}!")
            continue

        if "wie heißt du" in user_input.lower():
            print("Ich bin dein KI-Assistant.")
            continue

        conversation_history.append({"role": "user", "content": user_input})

        print("KI-Assistant denkt...")

        response = get_ai_response(client, conversation_history, model)

        conversation_history.append({"role": "assistant", "content": response})

        system_message = {
            "role": "system",
            "content": SYSTEM_PROMPT
        }

        chat_messages = [
            msg for msg in conversation_history
            if msg["role"] != "system"
        ]

        memory["conversation_history"] = [system_message] + chat_messages[-20:]
        save_memory(memory)

        print(f"KI-Assistant: {response}")


if __name__ == "__main__":
    main()