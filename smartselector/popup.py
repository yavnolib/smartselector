from kivy_app import MyApp

if __name__ == '__main__':
    while True:
        answer = input()
        if answer.lower() == 'y':
            MyApp().run()