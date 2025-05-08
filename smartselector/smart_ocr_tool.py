import tkinter as tk
from pynput import mouse, keyboard
import threading
import pyautogui
import easyocr
from googletrans import Translator
import pyperclip
from PIL import Image, ImageDraw
import sys
import time
from tkinter.messagebox import showerror, showwarning, showinfo

# === Глобальные переменные ===
start_pos = None
end_pos = None
overlay = None
is_dragging = False
region = None
reader = easyocr.Reader(['ru', 'en'], gpu=False)
translator = Translator()
text_window = None
tray_icon = None


# === GUI рамка ===
def draw_overlay(x1, y1, x2, y2):
    global overlay
    if overlay:
        overlay.destroy()

    overlay = tk.Tk()
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-alpha', 0.3)
    overlay.configure(bg='blue')

    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    overlay.geometry(f"{width}x{height}+{left}+{top}")
    overlay.update()


def on_click(x, y, button, pressed):
    global start_pos, end_pos, is_dragging, overlay, region

    if button.name != 'left':
        return

    if pressed:
        start_pos = (x, y)
        is_dragging = True
        threading.Thread(target=track_mouse_drag, daemon=True).start()
    else:
        is_dragging = False
        end_pos = (x, y)
        if overlay:
            overlay.destroy()
            overlay = None
        region = (
            min(start_pos[0], end_pos[0]),
            min(start_pos[1], end_pos[1]),
            abs(end_pos[0] - start_pos[0]),
            abs(end_pos[1] - start_pos[1])
        )
        print(f"[INFO] Region selected: {region}")


def track_mouse_drag():
    global is_dragging
    while is_dragging:
        x, y = pyautogui.position()
        draw_overlay(start_pos[0], start_pos[1], x, y)
        time.sleep(0.01)


def perform_ocr_and_translate():
    global region
    if not region or region[2] == 0 or region[3] == 0:
        print("[WARN] Invalid region")
        return

    screenshot = pyautogui.screenshot(region=region)
    screenshot.save("temp_capture.png")
    result = reader.readtext("temp_capture.png", detail=0)
    text = ' '.join(result).strip()

    if not text:
        print("[INFO] No text recognized.")
        return

    pyperclip.copy(text)
    print(f"[OCR] Recognized: {text}")

    translated = ''
    try:
        if any(c.isalpha() and ord(c) < 128 for c in text):  # английский
            translated = translator.translate(text, dest='ru').text
    except Exception as e:
        translated = f"[Translation error] {e}"

    show_text_window(text, translated)


def show_text_window(text, translated=''):
    global text_window

    if text_window and text_window.winfo_exists():
        text_widget = text_window.winfo_children()[0]
        text_widget.config(state='normal')
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, "📝 Распознанный текст:\n" + text + "\\n")
        if translated:
            text_widget.insert(tk.END, "\\n📘 Перевод:\n" + translated)
        text_widget.config(state='disabled')
    else:
        text_window = tk.Toplevel()
        text_window.title("OCR Result")
        text_window.geometry("500x300")
        text_window.attributes('-topmost', True)

        text_widget = tk.Text(text_window, wrap=tk.WORD, font=("Arial", 12))
        text_widget.insert(tk.END, "📝 Распознанный текст:\n" + text + "\\n")
        if translated:
            text_widget.insert(tk.END, "\\n📘 Перевод:\n" + translated)
        text_widget.configure(state='disabled')
        text_widget.pack(expand=True, fill='both')


def on_hotkey():
    perform_ocr_and_translate()


def listen_keyboard():
    COMBO = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode(char='f')}
    current = set()

    def on_press(key):
        if key in COMBO:
            current.add(key)
        if all(k in current for k in COMBO):
            on_hotkey()

    def on_release(key):
        if key in current:
            current.remove(key)

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def create_image():
    image = Image.new('RGB', (64, 64), color='white')
    draw = ImageDraw.Draw(image)
    draw.rectangle((10, 10, 54, 54), outline='blue', width=4)
    draw.text((20, 20), "OCR", fill='black')
    return image


def quit_action(icon, item):
    print("[INFO] Exiting.")
    icon.stop()
    sys.exit()


def run_tray():
    global tray_icon
    tray_icon = Icon("SmartOCR")
    tray_icon.icon = create_image()
    tray_icon.menu = Menu(MenuItem("Выход", quit_action))
    tray_icon.run()


def main():
    threading.Thread(target=listen_keyboard, daemon=True).start()
    threading.Thread(target=lambda: mouse.Listener(on_click=on_click).run(), daemon=True).start()
    run_tray()


if __name__ == "__main__":
    print("[INFO] SmartOCR запущен. Выдели область мышью, затем нажми Ctrl+Alt+f.")
    main()