from tkinter.messagebox import showinfo
from pynput import mouse, keyboard
import pyautogui
import easyocr
from deep_translator import GoogleTranslator
from pynotifier import NotificationClient, Notification
from pynotifier.backends import platform
import pyperclip
import numpy as np
from pynput import mouse
import PIL

class App:
    def __init__(self):
        self.reader = easyocr.Reader(['ru', 'en'], gpu=False)
        self.translator = GoogleTranslator(source='auto', target='ru')
        self.notifier = NotificationClient()
        self.notifier.register_backend(platform.Backend())

    def listen_keyboard(self):
        COMBO = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode(char='f')}
        current = set()

        def on_press(key):
            if key in COMBO:
                current.add(key)
            if all(k in current for k in COMBO):
                self.on_hotkey()

        def on_release(key):
            if key in current:
                current.remove(key)

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def perform_ocr_and_translate(self, screen):
        result = self.reader.readtext(np.array(screen), detail=0)
        text = ' '.join(result).strip()
        print(f"[OCR] Recognized: {text}")
        pyperclip.copy(text)

        translated = ''
        try:
            if any(c.isalpha() and ord(c) < 128 for c in text):  # английский
                translated = self.translator.translate(text)
        except Exception as e:
            translated = f"[Translation error] {e}"
        print(f'{translated=}')
        showinfo(title='Распознано', message=f'Текст: {text}\nПеревод:{translated}')

    def make_screen(self) -> PIL.Image:
        notification = Notification(title='SmartTranslate', message='Скриншот выполнен, выделите с помощью ЛКМ интересующую область')
        screenshot = pyautogui.screenshot()
        self.notifier.notify_all(notification=notification)
        return screenshot
    
    def get_coords(self):
        notification = Notification(title='SmartTranslate', message='Область выделена. Выполняется перевод внутри выделенной области')
        coords = {}
        def on_click(x, y, button, pressed):
            if button == mouse.Button.left:
                if pressed:
                    coords['pressed'] = (x, y)
                else:
                    coords['released'] = (x, y)        
                    return False
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
        self.notifier.notify_all(notification=notification)
        return coords
    
    def on_hotkey(self) -> None:
        screen = self.make_screen()
        
        coords = self.get_coords()
        
        ocr_image = screen.crop(list(coords['pressed'])+ list(coords['released']))
        self.perform_ocr_and_translate(ocr_image)

if __name__ == '__main__':
    app = App()
    app.listen_keyboard()