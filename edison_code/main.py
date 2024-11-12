# -*- coding: utf-8 -*-
import mraa
import time
import math
import threading
import json
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

class TemperaturaSensor:
    def __init__(self, pin, B=4275, R0=100000):
        self.sensor = mraa.Aio(pin)
        self.B = B
        self.R0 = R0

    def ler_temperatura(self):
        a = self.sensor.read()
        R = 1023.0 / a - 1.0
        R = self.R0 * R
        temperatura = 1.0 / (math.log(R / self.R0) / self.B + 1 / 298.15) - 273.15
        return temperatura


class LEDController:
    def __init__(self, pin_verde, pin_vermelho):
        self.led_verde = mraa.Gpio(pin_verde)
        self.led_vermelho = mraa.Gpio(pin_vermelho)
        self.led_verde.dir(mraa.DIR_OUT)
        self.led_vermelho.dir(mraa.DIR_OUT)

    def atualizar_leds(self, estado_verde, estado_vermelho):
        self.led_verde.write(1 if estado_verde else 0)
        self.led_vermelho.write(1 if estado_vermelho else 0)

    def desligar_leds(self):
        self.led_verde.write(0)
        self.led_vermelho.write(0)


class GravadorLogger:
    def __init__(self, arquivo="logger.txt"):
        self.arquivo = arquivo
        self.ultimo_status = None
        self.ultima_temperatura = None

    def gravar(self, status, temperatura):
        with open(self.arquivo, "a") as f:
            data = {
                "status": status,
                "temperatura": temperatura,
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            f.write(json.dumps(data) + "\n")
            self.ultimo_status = status
            self.ultima_temperatura = temperatura

    def ler_ultimo_log(self):
        try:
            with open(self.arquivo, "r") as f:
                linhas = f.readlines()
                if linhas:
                    return json.loads(linhas[-1].strip())
                else:
                    return {}
        except Exception as e:
            print("Erro ao ler o logger:", e)
            return {}


class SistemaMonitoramento:
    def __init__(self, sensor_pin=0, led_verde_pin=5, led_vermelho_pin=7, porta_estado_pin=8):
        self.sensor_temperatura = TemperaturaSensor(sensor_pin)
        self.leds = LEDController(led_verde_pin, led_vermelho_pin)
        self.porta_estado = mraa.Gpio(porta_estado_pin)
        self.porta_estado.dir(mraa.DIR_IN)
        self.logger = GravadorLogger()

    def monitorar(self, intervalo=1.0):
        print("Iniciando monitoramento...")
        try:
            while True:
                temperatura = self.sensor_temperatura.ler_temperatura()
                estado_porta = self.porta_estado.read()

                if estado_porta == 1:
                    status = "lhc aberto"
                    self.leds.atualizar_leds(estado_verde=True, estado_vermelho=False)
                else:
                    status = "lhc fechado"
                    self.leds.atualizar_leds(estado_verde=False, estado_vermelho=True)

                # Loga o estado e a temperatura
                self.logger.gravar(status, temperatura)
                print("Temperatura = {}C, Estado = {}".format(temperatura, status))

                time.sleep(intervalo)

        except KeyboardInterrupt:
            print("Monitoramento interrompido pelo usuário.")

        finally:
            self.leds.desligar_leds()
            print("Finalizando o monitoramento.")


class StatusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/status/":
            ultimo_log = sistema.logger.ler_ultimo_log()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(ultimo_log))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")


def iniciar_servidor_http():
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, StatusHandler)
    print("Servidor HTTP rodando na porta 8080...")
    httpd.serve_forever()


# Inicializa o sistema de monitoramento e roda as threads
if __name__ == "__main__":
    sistema = SistemaMonitoramento()

    # Thread para o sistema de monitoramento
    thread_monitoramento = threading.Thread(target=sistema.monitorar, args=(1.0,))
    thread_monitoramento.start()

    # Thread para o servidor HTTP
    thread_http = threading.Thread(target=iniciar_servidor_http)
    thread_http.start()

    thread_monitoramento.join()
    thread_http.join()
