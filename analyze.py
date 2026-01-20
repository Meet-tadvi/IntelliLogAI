import ollama
from pathlib import Path

# ================= CONFIG =================
LOG_FILES = ["sample1.log", "sample2.log", "sample3.log","sample.log"] 
OUTPUT_FILE = "output.txt"
MAX_LINES = 5000 
# =========================================

def read_log_files(file_list: list[str]) -> list[str]:
    combined_content = []
    for file_name in file_list:
        path = Path(file_name)
        if path.exists():
            try:
                # Reading all lines and then slicing the last 5000
                with path.open("r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    last_lines = lines[-MAX_LINES:]  # Standard list slicing
                    
                    for line in last_lines:
                        combined_content.append(f"[{file_name}] {line.strip()}")
            except Exception as e:
                combined_content.append(f"[{file_name}] Error reading file: {e}")
    return combined_content

def analyze_with_ollama(all_logs: list[str], user_prompt: str) -> str:
    log_context = "\n".join(all_logs) if all_logs else "No logs available."

    prompt = f"""
You are a helpful AI assistant with access to system logs.

SYSTEM LOG DATA:
{log_context}

USER QUESTION:
{user_prompt}

INSTRUCTIONS:
1. Answer based on the SYSTEM LOG DATA if relevant.
2. Provide general knowledge if the question is unrelated to logs.
3. If logs are referenced, mention which sample file the info came from.
"""

    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.4}
        )
        return response["message"]["content"]
    except Exception as e:
        return f"❌ Connection Error: {e}"

def main():
    print("--- Log Chat System Active (Type 'bye' to quit) ---")
    
    while True:
        user_prompt = input("\nHow can I help you? ").strip()
        
        # Exit condition
        if user_prompt.lower() == "bye":
            print("Shutting down. Goodbye!")
            break

        if not user_prompt:
            continue

        # Prepare and Analyze
        all_logs = read_log_files(LOG_FILES)
        
        print("🤖 Thinking...")
        result = analyze_with_ollama(all_logs, user_prompt)
        
        # Save to output file
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(f"\nUser: {user_prompt}\nAI: {result}\n" + "-"*30)
            
        print("\n" + "="*40)
        print(result)
        print("="*40)

if __name__ == "__main__":
    main()