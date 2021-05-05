import eel

eel.init('web')


# Exposing this python function to call from JS
@eel.expose
def my_python_method(param1, param2):
    print(param1 + param2)


eel.start('index.html', size=(1200, 680))

