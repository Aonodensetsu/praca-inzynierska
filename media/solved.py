# Definicje sprawiające, że ten plik jest prawidłowy składniowo.
# Można zignorować, kod ten nie odpowiada kodowi laboratoriów.
ntfy_topic = ...
values = {}
class Metric:
    temperature = ...
    pressure = ...
    humidity = ...
    flag = ...
    pressed = ...
    BOARD = ...
    OUT = ...
    HIGH = ...
    LOW = ...
    def __init__(*args): ...
    def set_imu_config(self, *args): ...
    def get_orientation_radians(self): return {}
    def set_pixels(self, *args): ...
    def setCursor(self, *args): ...
    def write(self, *args): ...
    def get_time(self): return 0
    def update_sensor(self): ...
    def get_proximity(self, **kwargs): ...
    def get_lux(self, **kwargs): ...
    def spl(self): ...
    def setmode(self, *args): ...
    def setup(self, *args): ...
    def output(self, *args): ...
GroveUltrasonicRanger = Metric
GroveDisplay = Metric
GPIO = Metric()
sense = Metric()
motion = Metric()
btn = Metric()
bme280 = Metric()
ltr559 = Metric()
sph0645lm4h_b = Metric()
def calculate_leds(*args): ...
def get_cpu_temperature(): ...
def compensate_temperature(*args): ...
def proximity_to_mm(*args): ...
def post(*args, **kwargs): ...
def data_loop(*args): return [0]
def insert_vals(*args): ...
def display_text(*args): ...
async def sleep(*args): ...


# --- Lab 0 ---

# Przykład
def example(v):
    return v


# --- Lab 1 ---

# Z2.
def set_imu():
    sense.set_imu_config(True, True, False)

# Z3.
def get_yaw():
    return sense.get_orientation_radians()['yaw']

# Z4.
def draw_compass(yaw):
    sense.set_pixels(calculate_leds(yaw))


# --- Lab 2 ---

# Z1.
LCD_address = 0x3E

# Z2.
# w zależności od połączeń fizycznych
Sonar_port = '5, 16, 18, 22, 24, albo 26'

# Z3.
sonar = GroveUltrasonicRanger(Sonar_port)
display = GroveDisplay(LCD_address)

# Z4.
def time_to_dist(t: float) -> float:
    sekundy = t / 10**6
    metry = sekundy * 343  # m/s
    centymetry = metry * 100
    jedna_strona = centymetry / 2
    return jedna_strona

# Z5.
def show_measurement(val: float, prev: float):
    display.setCursor(0, 0)
    display.write(f'cur: {val:>8.2f} cm')
    display.setCursor(1, 0)
    display.write(f'prv: {prev:>8.2f} cm')

async def z6(): 
    # Z6.
    previous = 0
    while True:
        current = time_to_dist(sonar.get_time())
        show_measurement(current, previous)
        previous = current
        await sleep(1)


# --- Lab 3 ---

# Z1.
# w zależności od połączeń fizycznych
sensor_port = '5, 16, 18, 22, 24, albo 26'
led_pin = '5, 16, 18, 22, 24, albo 26, ale nie ten sam co sensor_port'
btn_pin = 'led_pin + 1'

# Z2.
def motion_detected():
    if motion.flag:
        btn.led = True

# Z3.
def btn_pressed():
    if btn.pressed:
        btn.led = False

async def z4():
    # Z4.
    while True:
        motion_detected()
        btn_pressed()
        await sleep(2)


# --- Lab 4 ---

# Z1.
def update_sensors():
    bme280.update_sensor()
    ltr559.update_sensor()
    
# Z2.
metrics = [
    Metric('CPU',   '°C',  lambda: get_cpu_temperature()),
    # dodaj linijki metryk dla temperatury, ciśnienia, wilgotności, bliskości, jasności, głośności SPL
    Metric('<temperatura>', '°C', lambda: compensate_temperature(bme280.temperature)),
    Metric('<ciśnienie>', 'Pa', lambda: bme280.pressure),
    Metric('<wilgotność>', '%', lambda: bme280.humidity),
    Metric('<bliskość>', 'mm', lambda: proximity_to_mm(ltr559.get_proximity(passive=True))),
    Metric('<jasność>', 'lux', lambda: ltr559.get_lux(passive=True)),
    Metric('<głośność>', 'SPL', lambda: sph0645lm4h_b.spl()),
]

# Z3.
def send_message():
    if values['<bliskość>'][-1] < 0.1:
        post(f'https://ntfy.sh/{ntfy_topic}', json={
            k: float(v[-1]) for k, v in values.items()
        })

# Z4.
async def loop():
    update_sensors()
    for i in data_loop(metrics):
        update_sensors()
        insert_vals(metrics)
        display_text(i)
        send_message()
        await sleep(1)


# --- Lab 5 ---

# Z1.
def gpio_config():
    GPIO.setmode(GPIO.BOARD)

# Z2.
led_red = 16
led_yellow = 18
led_green = 22

# Z3.
def port_config():
    GPIO.setup(led_red, GPIO.OUT)
    GPIO.setup(led_yellow, GPIO.OUT)
    GPIO.setup(led_green, GPIO.OUT)

# Z4.
async def red_to_green():
    GPIO.output(led_yellow, GPIO.HIGH)
    await sleep(2)
    GPIO.output(led_green, GPIO.HIGH)
    GPIO.output(led_red, GPIO.LOW)
    GPIO.output(led_yellow, GPIO.LOW)

async def green_to_red():
    GPIO.output(led_yellow, GPIO.HIGH)
    GPIO.output(led_green, GPIO.LOW)
    await sleep(2)
    GPIO.output(led_red, GPIO.HIGH)
    GPIO.output(led_yellow, GPIO.LOW)

# Z5.
"curl https://ntfy.sh/<identyfikator> -d 'zaliczono'"

# Z6.
import requests
import json

async def sender():
    for i in range(3):
        await green_to_red()
        await sleep(5)
        requests.post(f"https://ntfy.sh/{ntfy_topic}", data=b'rg')
        await sleep(20)
        requests.post(f"https://ntfy.sh/{ntfy_topic}", data=b'gr')
        await sleep(5)
        await red_to_green()
        await sleep(20)
    requests.post(f"https://ntfy.sh/{ntfy_topic}", data=b'stop')

async def receiver():
    resp = requests.get(f"https://ntfy.sh/{ntfy_topic}/json", stream=True)
    for line in resp.iter_lines():
        try:
            j = json.loads(line)
            match j['message']:
                case 'rg':
                    await red_to_green()
                case 'gr':
                    await green_to_red()
                case 'stop':
                    break
        except:
            pass
