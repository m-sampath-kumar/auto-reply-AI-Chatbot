import pyautogui
import pyperclip
import time
import google.generativeai as genai

# API Key
API_KEY = #"keep your gemini api key"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro")  # Supported model

# Function to get the last message dynamically
def get_last_message(copied_text: str):
    """
    Extracts the last message from the copied chat dynamically.
    Returns a tuple: (sender_name, message_text)
    """
    # Split messages by year in timestamp
    messages = copied_text.strip().split("/2025] ")
    
    if not messages:
        return None, None
    
    # Get the last message
    last_msg_line = messages[-1].strip()
    
    # Separate sender and message
    if ": " in last_msg_line:
        sender_name, msg_text = last_msg_line.split(": ", 1)
        return sender_name.strip(), msg_text.strip()
    
    # If no sender found, return None
    return None, last_msg_line

# ----------------- MAIN LOOP -----------------
# Click on the chat icon to open the chat
pyautogui.click(1200, 1043)
time.sleep(1)

while True:
    # Click on profile to make chat active
    pyautogui.click(550, 788)
    time.sleep(1)
    
    # Drag to select last chat messages
    pyautogui.moveTo(967, 306)
    pyautogui.dragTo(877, 1236, duration=3, button="left")
    time.sleep(1)

    # Copy the selected text
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.5)
    copied_text = pyperclip.paste().strip()

    # Deselect text
    pyautogui.click(1690, 871)
    time.sleep(0.5)

    # Get last message and sender dynamically
    sender, last_msg_text = get_last_message(copied_text)
    if not sender or not last_msg_text:
        continue  # Skip if last message not found
    
    print(f"📩 Last message from {sender}: {last_msg_text}")

    # Prepare prompt for Gemini AI
    prompt = f"""
    You are Sampath.You can speak English,Hindi and Telugu.You are from India. 
    reply in the same language as the sender, orelse use English and Telugu if necessary. 
    But use Hindi if they talk in Hindi. 
    send small messages only for small conversation
    if possible take the person name from above{sender} and if necessary you can include it 


    The other person said:
    "{last_msg_text}"

    Now reply as Sampath.
    """

    # Generate AI reply
    sampath_reply = model.generate_content(prompt).text.strip()

    # Paste reply and send
    paste_x, paste_y = 1248, 951
    pyautogui.click(paste_x, paste_y)
    time.sleep(0.1)
    pyperclip.copy(sampath_reply)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(2)
    pyautogui.press("enter")
