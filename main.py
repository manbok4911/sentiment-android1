# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
import threading

# کتابخانه‌های سبک
try:
    from textblob import TextBlob
    HAS_TEXTBLOB = True
except:
    HAS_TEXTBLOB = False

try:
    from googletrans import Translator
    HAS_TRANSLATOR = True
except:
    HAS_TRANSLATOR = False

import pyttsx3

class SimpleSentimentApp(App):
    def build(self):
        Window.size = (400, 700)
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        
        # لایه اصلی
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # عنوان
        title = Label(
            text='📊 Sentiment Analyzer',
            font_size=26,
            bold=True,
            color=(0.1, 0.3, 0.7, 1),
            size_hint=(1, 0.15)
        )
        layout.add_widget(title)
        
        # زبان مبدا
        layout.add_widget(Label(text='Source Language:', font_size=18))
        self.source_lang = Spinner(
            text='Persian',
            values=['Persian', 'English', 'Arabic', 'Spanish', 'French'],
            size_hint=(1, 0.08),
            background_color=(0.2, 0.5, 0.8, 1)
        )
        layout.add_widget(self.source_lang)
        
        # زبان مقصد
        layout.add_widget(Label(text='Target Language:', font_size=18))
        self.target_lang = Spinner(
            text='English',
            values=['Persian', 'English', 'Arabic', 'Spanish', 'French'],
            size_hint=(1, 0.08),
            background_color=(0.2, 0.5, 0.8, 1)
        )
        layout.add_widget(self.target_lang)
        
        # جعبه متن
        self.text_input = TextInput(
            hint_text='Type or paste text here...',
            size_hint=(1, 0.25),
            font_size=16,
            background_color=(1, 1, 1, 1)
        )
        layout.add_widget(self.text_input)
        
        # دکمه تحلیل
        self.analyze_btn = Button(
            text='🔍 ANALYZE SENTIMENT',
            size_hint=(1, 0.1),
            background_color=(0.1, 0.6, 0.3, 1),
            font_size=18
        )
        self.analyze_btn.bind(on_press=self.start_analysis)
        layout.add_widget(self.analyze_btn)
        
        # برچسب نتیجه
        self.result_label = Label(
            text='Result will appear here...',
            font_size=16,
            size_hint=(1, 0.3),
            halign='center',
            valign='middle'
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        layout.add_widget(self.result_label)
        
        return layout
    
    def start_analysis(self, instance):
        text = self.text_input.text.strip()
        if not text:
            self.result_label.text = "Please enter some text!"
            return
        
        self.analyze_btn.disabled = True
        self.result_label.text = "Analyzing... Please wait"
        
        # اجرا در رشته جداگانه
        thread = threading.Thread(target=self.perform_analysis, args=(text,))
        thread.daemon = True
        thread.start()
    
    def perform_analysis(self, text):
        try:
            # زبان‌ها
            lang_codes = {
                'Persian': 'fa',
                'English': 'en',
                'Arabic': 'ar',
                'Spanish': 'es',
                'French': 'fr'
            }
            
            src = lang_codes.get(self.source_lang.text, 'en')
            tgt = lang_codes.get(self.target_lang.text, 'en')
            
            # ترجمه (اگر کتابخانه نصب باشه)
            translated_text = text
            if HAS_TRANSLATOR and src != 'en':
                try:
                    translator = Translator()
                    translated = translator.translate(text, src=src, dest='en')
                    translated_text = translated.text
                except:
                    pass
            
            # تحلیل احساسات (اگر کتابخانه نصب باشه)
            sentiment = "Neutral"
            confidence = 0.5
            
            if HAS_TEXTBLOB:
                try:
                    blob = TextBlob(translated_text)
                    polarity = blob.sentiment.polarity
                    
                    if polarity > 0.1:
                        sentiment = "Positive 😊"
                        confidence = polarity
                    elif polarity < -0.1:
                        sentiment = "Negative 😔"
                        confidence = abs(polarity)
                    else:
                        sentiment = "Neutral 😐"
                        confidence = 0.5
                except:
                    pass
            
            # تولید صوت
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)
                engine.say(f"This text is {sentiment}")
                engine.runAndWait()
            except:
                pass
            
            # نمایش نتیجه
            result = f"""
            📝 Text: {text[:80]}...
            
            🌐 Source: {self.source_lang.text}
            🌍 Target: {self.target_lang.text}
            
            ⭐ Sentiment: {sentiment}
            🔍 Confidence: {confidence*100:.0f}%
            
            📊 Analysis Complete!
            """
            
            # آپدیت رابط کاربری
            App.get_running_app().result_label.text = result
            App.get_running_app().analyze_btn.disabled = False
            
        except Exception as e:
            result = f"Error during analysis: {str(e)}"
            App.get_running_app().result_label.text = result
            App.get_running_app().analyze_btn.disabled = False

# اجرای برنامه
if __name__ == '__main__':
    SimpleSentimentApp().run()