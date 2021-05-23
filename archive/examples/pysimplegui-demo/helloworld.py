import PySimpleGUI as sg

sg.theme('Reddit')

# Add a text row and button
layout = [
    [sg.Text('Hello, world!')],
    [sg.Button("OK")]
]
# Create window
window = sg.Window("Demo", layout)

# Create event loop
# Idea: GUI waits continuously until event happens from UI and handle
while True:
    event, values = window.read()
    # End program when button is clicked
    if event == 'OK' or event == sg.WIN_CLOSED:
        break


window.close()