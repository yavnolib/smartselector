from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window


class MyApp(App):
    def build(self):
        # Мы не строим основное окно, только подключаем обработку клавиш
        Window.bind(on_key_down=self._on_key_down)
        return

    def _on_key_down(self, window, key, scancode, codepoint, modifier):
        if key == 308:  # 308 — это код клавиши Alt_L
            self.show_popup()
        return True

    def show_popup(self):
        # Создаем всплывающее окно
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text='Alt_L нажата!'))
        close_button = Button(text='Закрыть', size_hint_y=None, height=40)
        content.add_widget(close_button)

        popup = Popup(title='Всплывающее окно',
                      content=content,
                      size_hint=(0.6, 0.4),
                      auto_dismiss=False)

        close_button.bind(on_release=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    MyApp().run()
