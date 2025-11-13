import RPi.GPIO as GPIO

# Wybór trybu adresacji BCM, zgodny z powyższym rysunkiem.
GPIO.setmode(GPIO.BCM)

# Pin 23 w adresacji BCM (16 w adresacji fizycznej) uruchomiony jako wyjściowy.
GPIO.setup(23, direction=GPIO.OUT)

# Ustawiony wysoki stan wyjścia (= 3,3V).
GPIO.output(23, value=GPIO.HIGH)

# Uwolnienie blokady pinów przy zakończeniu programu.
GPIO.cleanup()
