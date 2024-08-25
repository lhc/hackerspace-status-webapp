import RPi.GPIO as GPIO
import time
import requests

class EdgeController:
    def __init__(self, pin=18, server_url='http://localhost:5000', debounce_time=0.3):
        self.pin = pin
        self.server_url = server_url
        self.debounce_time = debounce_time
        self.previous_state = None
        self._setup_gpio()

    def _setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.previous_state = GPIO.input(self.pin)

    def monitor_button(self):
        while True:
            current_state = GPIO.input(self.pin)
            if current_state != self.previous_state:
                time.sleep(self.debounce_time)  # Aguarda um pouco para evitar leituras duplicadas
                if current_state == GPIO.input(self.pin):  # Confirma que o estado ainda é o mesmo
                    if current_state == False:
                        self._send_request('/lhc_fechado')
                    else:
                        self._send_request('/lhc_aberto')
                    self.previous_state = current_state
            time.sleep(0.2)

    def _send_request(self, endpoint):
        try:
            requests.get(f'{self.server_url}{endpoint}')
        except requests.RequestException as e:
            print(f"Error sending request: {e}")
