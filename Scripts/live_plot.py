from imgui_bundle import imgui, implot
import numpy as np

panel_title = "Test Panel"
start_x = 0.0
end_x = 2 * np.pi
steps_number = 100
plot_func_idx = 0
plot_func_list = [lambda x: np.sin(x), lambda x: np.cos(x)]

# Create ImPlot context once at start
implot.create_context()

def render():
    global start_x, end_x, steps_number, plot_func_idx

    show_panel = imgui.begin(panel_title)
    if show_panel:
        imgui.text("Hello from script!")
        _, start_x = imgui.slider_float("Start x", start_x, -2 * np.pi, 4 * np.pi)
        _, end_x = imgui.slider_float("End x", end_x, -2 * np.pi, 4 * np.pi)
        _, steps_number = imgui.slider_int("Points", steps_number, 1, 1000)
        _, plot_func_idx = imgui.combo("Function", plot_func_idx, ["sin", "cos"])
        imgui.end()
    
    func = plot_func_list[plot_func_idx]
    
    if implot.begin_plot("Live Plot", imgui.ImVec2(500, 400)):
        x = np.linspace(start=start_x, stop=end_x, num=steps_number)
        y = func(x)
        implot.setup_axes("x", "y")
        implot.plot_line("func", x, y)
        implot.end_plot()
