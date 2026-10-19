"""
Task 4: Rule-Based Interactive Terminal Assistant / Chatbot
Datheon Python Programming Internship

Run:
    python chatbot.py

The chatbot uses local JSON FAQ data and regular-expression intent matching.
It does not connect to the internet or use an AI language model.
"""

import json
import re
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
FAQ_FILE = BASE_DIR / "faq_data.json"


def load_faq_data():
    """Load FAQ responses from JSON. Return an empty list if unavailable/invalid."""
    try:
        with FAQ_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("FAQ data must be a JSON list.")
        return data
    except FileNotFoundError:
        print(f"Warning: {FAQ_FILE.name} not found. FAQ matching is disabled.")
    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Warning: Could not load FAQ data: {error}")
    return []


INTENT_PATTERNS = [
    ("greeting", r"\b(hi|hello|hey|good morning|good afternoon|good evening)\b"),
    ("thanks", r"\b(thanks|thank you|thx)\b"),
    ("help", r"\b(help|commands|what can you do|options)\b"),
    ("hours", r"\b(opening hours|business hours|what time.*open|when.*open|hours.*open)\b"),
    ("product", r"\b(product|price|cost|feature|features|available|availability|shipping|delivery|return|refund|warranty)\b"),
    ("time", r"\b(what time|current time|time now|tell me the time)\b"),
    ("date", r"\b(what date|today's date|current date|today date|what day is it)\b"),
    ("goodbye", r"\b(bye|goodbye|exit|quit|see you)\b"),
]


def normalize(text):
    """Normalize whitespace and letter case."""
    return re.sub(r"\s+", " ", text.strip().lower())


def match_faq(message, faq_data):
    """Find the first FAQ whose keywords match the normalized message."""
    for item in faq_data:
        keywords = item.get("keywords", [])
        if not isinstance(keywords, list):
            continue
        for keyword in keywords:
            if isinstance(keyword, str) and keyword.strip():
                pattern = r"\b" + re.escape(keyword.strip().lower()) + r"\b"
                if re.search(pattern, message):
                    answer = item.get("answer")
                    if isinstance(answer, str) and answer.strip():
                        return answer
    return None


def detect_intents(message):
    """Return all matching intents, not just the first one."""
    matches = []
    for intent, pattern in INTENT_PATTERNS:
        if re.search(pattern, message):
            matches.append(intent)
    return matches


def get_response(user_text, faq_data):
    """Return a response and exit flag; supports multiple detected intents."""
    message = normalize(user_text)

    if not message:
        return "Please type a message so I can help.", False

    intents = detect_intents(message)

    # Exit takes priority so the program can end predictably.
    if "goodbye" in intents:
        return "Goodbye! Thank you for chatting with the assistant.", True

    responses = []

    if "greeting" in intents:
        responses.append("Hello! How can I help you today?")
    if "help" in intents:
        responses.append(
            "You can ask about business hours, products, prices, delivery, "
            "returns, refunds, or warranty. You can also ask for the date or time. "
            "Type 'bye' to exit."
        )
    if "hours" in intents:
        faq_answer = match_faq(message, faq_data)
        responses.append(faq_answer or "I don't have confirmed business hours in my FAQ data.")
    if "product" in intents:
        faq_answer = match_faq(message, faq_data)
        if faq_answer and faq_answer not in responses:
            responses.append(faq_answer)
        elif not faq_answer:
            responses.append(
                "I couldn't find a matching product FAQ. Please specify the product "
                "or contact the store's support team."
            )
    if "time" in intents:
        responses.append(f"The current local computer time is {datetime.now().strftime('%I:%M:%S %p')}.")
    if "date" in intents:
        responses.append(f"Today's date is {datetime.now().strftime('%A, %d %B %Y')}.")

    # FAQ matching also supports other questions that don't match a broad intent.
    if not responses:
        faq_answer = match_faq(message, faq_data)
        if faq_answer:
            responses.append(faq_answer)

    if "thanks" in intents:
        responses.append("You're welcome!")

    if responses:
        # Avoid duplicate responses while preserving order.
        unique_responses = list(dict.fromkeys(responses))
        return " ".join(unique_responses), False

    return (
        "Sorry, I couldn't understand that question. Try asking about business hours, "
        "products, delivery, returns, refunds, or type 'help' for examples.",
        False,
    )


def main():
    print("=" * 58)
    print("       RULE-BASED CUSTOMER SUPPORT CHATBOT")
    print("=" * 58)
    faq_data = load_faq_data()
    print(f"Loaded {len(faq_data)} FAQ entries.")
    print("Bot: Hello! Ask me a question or type 'help'.")
    print("Bot: Type 'bye', 'exit', or 'quit' to end the chat.")

    while True:
        try:
            user_text = input("\nYou: ")
            response, should_exit = get_response(user_text, faq_data)
            print(f"Bot: {response}")
            if should_exit:
                break
        except (KeyboardInterrupt, EOFError):
            print("\nBot: Chat ended. Goodbye!")
            break
        except Exception as error:
            # Prevent unexpected input/runtime errors from crashing the chat.
            print(f"Bot: Something went wrong while handling that message ({error}). Please try again.")


if __name__ == "__main__":
    main()
