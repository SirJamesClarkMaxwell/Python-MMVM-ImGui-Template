
from app import App
from imgui_bundle import hello_imgui,imgui

def main():

    app = App.get()
    runner_params = app.initialize()
    runner_params.imgui_window_params.default_imgui_window_type = \
    hello_imgui.DefaultImGuiWindowType.provide_full_screen_dock_space|\
    hello_imgui.DefaultImGuiWindowType.provide_full_screen_window
    hello_imgui.run(runner_params)

if __name__ == "__main__":
    main()
