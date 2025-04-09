import board
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Задержка при запуске, чтобы избежать срабатывания при подключении
time.sleep(2)

# Инициализация клавиатуры
keyboard = Keyboard(usb_hid.devices)

# Настройка LED для индикации
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Настройка кнопки
button = digitalio.DigitalInOut(board.GP15)  # GP15 - это пин для кнопки
button.direction = digitalio.Direction.INPUT
# button.pull = digitalio.Pull.DOWN  # Подтягивающий резистор к земле
button.pull = digitalio.Pull.UP  # Внутренняя подтяжка к 3.3V

# Параметры для работы с кнопкой
debounce_time = 0.05  # Время для устранения дребезга контактов
last_button_state = False

# Настройка режима отладки
DEBUG_MODE = False  # Измените на True для включения пауз при отладке
DEBUG_PAUSE = 2.0  # Длительность паузы в секундах для отладки

def blink_led(times=1, delay=0.2):
    """Мигание светодиодом для индикации"""
    for _ in range(times):
        led.value = True
        time.sleep(delay)
        led.value = False
        time.sleep(delay)

def debug_pause():
    """Пауза для отладки, которую можно включать и отключать"""
    if DEBUG_MODE:
        print(f"Пауза для отладки ({DEBUG_PAUSE} сек)...")
        time.sleep(DEBUG_PAUSE)

def press_key(key, delay=0.4):
    """Нажатие одной клавиши с задержкой"""
    keyboard.press(key)
    keyboard.release_all()
    time.sleep(delay)
    debug_pause()

def press_key_multiple(key, count, delay=0.4):
    """Нажатие клавиши несколько раз с задержкой"""
    for i in range(count):
        print(f"Нажатие {i+1} из {count}")
        keyboard.press(key)
        keyboard.release_all()
        time.sleep(delay)
    debug_pause()

def wait_for_button_press():
    """Ожидание нажатия кнопки"""
    last_state = button.value
    while True:
        current_state = button.value
        if current_state and not last_state:
            time.sleep(debounce_time)  # Защита от дребезга
            return
        last_state = current_state
        time.sleep(0.01)

def execute_sequence():
    press_key(Keycode.GUI)
    press_key(Keycode.SPACEBAR)
    
    # Открытие настроек
    press_key(Keycode.UP_ARROW)
    press_key_multiple(Keycode.RIGHT_ARROW, 4)
    press_key(Keycode.SPACEBAR)
    
    time.sleep(5)
    # Открыть интернет настройки
    press_key(Keycode.RIGHT_ARROW)
    press_key(Keycode.SPACEBAR)
    
    time.sleep(2)
    # Отключить интернет
    press_key(Keycode.RIGHT_ARROW)
    press_key(Keycode.DOWN_ARROW)
    press_key(Keycode.SPACEBAR)
    time.sleep(1)
    # Добавляем геймпас аккаунт
    press_key(Keycode.GUI)
    press_key(Keycode.RIGHT_ARROW)
    press_key(Keycode.DOWN_ARROW)
    press_key(Keycode.SPACEBAR)
    press_key(Keycode.DOWN_ARROW)
    press_key(Keycode.SPACEBAR)
    time.sleep(5)
    
    # Включаем интернет
    press_key(Keycode.SPACEBAR)
    time.sleep(1)
    press_key(Keycode.SPACEBAR)
    time.sleep(15)
    
    # Выходим с аккаунта
    press_key(Keycode.GUI)
    press_key(Keycode.RIGHT_ARROW)
    press_key_multiple(Keycode.DOWN_ARROW, 2)
    press_key_multiple(Keycode.SPACEBAR, 2)
    time.sleep(3)
    
    # Меняем время
    press_key(Keycode.LEFT_ARROW)
    press_key_multiple(Keycode.DOWN_ARROW, 2)
    press_key(Keycode.RIGHT_ARROW)
    press_key_multiple(Keycode.DOWN_ARROW, 3)
    press_key(Keycode.SPACEBAR)
    time.sleep(1)
    press_key(Keycode.SPACEBAR)
    
    # Вверх 4 раза с паузой 0.4 сек
    for i in range(4):
        press_key(Keycode.UP_ARROW, 0.4)
    
    press_key(Keycode.SPACEBAR)
    time.sleep(5)
    
    # Добавляем снова аккаунт
    press_key(Keycode.GUI)
    press_key(Keycode.RIGHT_ARROW)
    press_key(Keycode.DOWN_ARROW)
    press_key(Keycode.SPACEBAR)
    press_key(Keycode.DOWN_ARROW)
    press_key(Keycode.SPACEBAR)
    
    wait_for_button_press()
    
    # Инжектимся
    press_key(Keycode.GUI)
    press_key(Keycode.RIGHT_ARROW)
    press_key_multiple(Keycode.DOWN_ARROW, 2)
    press_key(Keycode.SPACEBAR)
    press_key(Keycode.DOWN_ARROW)
    press_key(Keycode.SPACEBAR)
    time.sleep(1)
    
    blink_led(3, 0.3)  # Индикация завершения
    time.sleep(10)
    
    # Входим в игру
    press_key(Keycode.GUI)
    press_key(Keycode.SPACEBAR)
    time.sleep(1)
    press_key(Keycode.SPACEBAR)
    time.sleep(15)
    press_key(Keycode.GUI)
    press_key(Keycode.RIGHT_ARROW)
    press_key(Keycode.SPACEBAR)
    press_key(Keycode.DOWN_ARROW)
    press_key(Keycode.SPACEBAR)

# Инициализация - считываем начальное состояние кнопки
last_button_state = button.value
time.sleep(0.1)  # Небольшая задержка для стабилизации

print("Устройство готово к работе")
print(f"Режим отладки: {'ВКЛЮЧЕН' if DEBUG_MODE else 'ВЫКЛЮЧЕН'}")

# Основной цикл программы
while True:
    try:
        print("Ожидание нажатия кнопки...")
        wait_for_button_press()
        print("Кнопка нажата, начинаем выполнение...")
        execute_sequence()
        
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        blink_led(5, 0.1)  # Индикация критической ошибки
        time.sleep(1)  # Пауза перед продолжением работы 