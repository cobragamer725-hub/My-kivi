import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from groq import Groq

class BuntaiLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        
        # Set mobile background color to a sleek dark tech theme
        Window.clearcolor = (0.04, 0.06, 0.1, 1)

        # Application Header Title
        self.add_widget(Label(
            text='Buntai AI (Free)',
            font_size='24sp',
            bold=True,
            size_hint_y=None,
            height=40,
            color=(1, 1, 1, 1)
        ))

        # Text input area where you type your questions
        self.user_input = TextInput(
            hint_text='Ask Buntai AI anything for free...',
            multiline=True,
            size_hint_y=None,
            height=120,
            font_size='16sp',
            background_color=(0.12, 0.16, 0.22, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.6, 0.6, 0.6, 1)
        )
        self.add_widget(self.user_input)

        # Action Execution Button
        self.submit_btn = Button(
            text='Run Free AI Query',
            size_hint_y=None,
            height=50,
            font_size='16sp',
            bold=True,
            background_color=(0.06, 0.72, 0.51, 1)
        )
        self.submit_btn.bind(on_press=self.ask_buntai)
        self.add_widget(self.submit_btn)

        # Scrollable area to handle long AI answers
        scroll = ScrollView()
        self.output_label = Label(
            text='Free Buntai AI Engine Active...',
            font_size='15sp',
            size_hint_y=None,
            color=(0.9, 0.9, 0.9, 1),
            halign='left',
            valign='top'
        )
        self.output_label.bind(size=self.update_label_size)
        scroll.add_widget(self.output_label)
        self.add_widget(scroll)

    def update_label_size(self, instance, value):
        instance.text_size = (instance.width, None)
        instance.height = instance.texture_size[1] + 20

    def ask_buntai(self, instance):
        prompt = self.user_input.text.strip()
        if not prompt:
            self.output_label.text = "Error: Please type something first!"
            return

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            self.output_label.text = "Error: GROQ_API_KEY environment variable missing."
            return

        self.output_label.text = "Buntai AI is thinking..."

        try:
            # Initialize connection to Groq API using your free environment key
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are Buntai AI, a brilliant, concise, and ultra-fast AI running inside an Android application framework."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            self.output_label.text = response.choices[0].message.content
        except Exception as e:
            self.output_label.text = f"Connection Failed: {str(e)}"

class BuntaiAI(App):
    def build(self):
        return BuntaiLayout()

if __name__ == '__main__':
    BuntaiAI().run()
