# SmartSelector
**SmartSelector** is a utility that lets you take a screenshot of a selected screen area using a hotkey, recognize the text inside this area (OCR), and automatically translate it into Russian using Google Translate. The translated text is shown in a popup window and copied to the clipboard.

**This tool is especially useful when translating subtitles in videos, reading documentation or articles in a foreign language, or quickly understanding any on-screen text without having to manually retype it into a translator**. It significantly speeds up the translation workflow by automating OCR and translation in just a few clicks.
## 🔧 Features

- 📸 Take screenshots and select arbitrary screen regions with the mouse
- 🧠 Text recognition (OCR) from the selected area
- 🌍 Automatic language detection
- 🇷🇺 Translation into Russian (from English and other languages)
- 🔔 Desktop notifications
- 📋 Automatically copies recognized text to the clipboard

## ⌨️ Hotkeys

Press **Ctrl + Alt + F** to:
1. Take a full-screen screenshot
2. Select the desired region with the mouse
3. Recognize and translate text from the selected area

## 🖥️ Dependencies

The project uses the following libraries:

- `pynput`
- `pyautogui`
- `easyocr`
- `deep_translator`
- `pynotifier`
- `pyperclip`
- `Pillow` (`PIL`)
- `tkinter` (part of the Python standard library)

## 📦 Installation

At the moment the project is in beta version and the work has been tested only on Linux.

Make sure you have Python 3.11+ and pip installed. Then install the dependencies:

```bash
sudo apt-get install xclip  # required for clipboard functionality on Linux

poetry install
```

## 🚀 Usage

```bash
python smartselector/selector_v2.py
```

Once launched, the script will wait for the hotkey **Ctrl + Alt + F** to be pressed.

## 🛠️ Notes

- For accurate OCR, make sure the fonts in the image are readable.
- GPU not required: EasyOCR is launched with `gpu=False` — it's slower but does not require CUDA.

## 📌 TODO / Possible Improvements

- Run as a systemd service
- Support more translation languages
- Allow choosing translation language
- Enhanced popup UI with readable fonts
- Integration with system tray

## 📄 License

This project is licensed under the MIT License. You are free to use and modify it for your own needs.
