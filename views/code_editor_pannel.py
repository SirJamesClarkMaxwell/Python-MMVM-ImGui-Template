from imgui_bundle import imgui, imgui_ctx
try:
    from imgui_bundle import imgui_color_text_edit
except ImportError:
    from utils.logger import AppLogger
    AppLogger.get().error("Failed to import imgui_color_text_edit. Code highlighting will be disabled.")
    imgui_color_text_edit = None

from views import Panel
from utils.logger import AppLogger
from views.runtime_panel import RuntimePanel


class CodeEditorPanel(Panel):
    def __init__(self, view_model):
        super().__init__(view_model)

    def render(self):
        avail_x, avail_y = imgui.get_content_region_avail()
        if imgui.begin_table(
            "CodeEditorLayout", 1, 0  # Using 0 for no flags
        ):
            # === Row 0: Dockable editor space ===
            imgui.table_next_row()
            imgui.table_set_column_index(0)

            imgui.dock_space(
                imgui.get_id("EditorDockspace"), imgui.ImVec2(avail_x, avail_y * 0.75)
            )

            self.render_code_space()  # Renders windows inside dock

            # === Row 1: Output area ===
            imgui.table_next_row()
            imgui.table_set_column_index(0)

            self.render_code_actions()
            imgui.table_next_row()
            imgui.table_set_column_index(0)

            imgui.separator()
            imgui.text("Output:")

            with imgui_ctx.begin_child(
                "EditorOutput", imgui.ImVec2(-1, 100), 0  # Using 0 for no flags
            ):
                if current := self.view_model.editors.get(
                    self.view_model.data.current_tab_name
                ):
                    _, tab = current
                    imgui.text_wrapped(tab.output or "No output yet.")

            imgui.end_table()

        # === Popup: Unsaved Changes ===
        if self.view_model.confirming_close_name:
            imgui.open_popup("UnsavedChangesPopup")

        if imgui.begin_popup_modal("UnsavedChangesPopup")[0]:
            self.close_script_tab_actions()
            imgui.end_popup()

        self.render_runtime_panels()

    def render_code_actions(self):
        data = self.view_model.scope["app"].application_data
        if imgui.button("Run"):  # , imgui.ImVec2(-1, 24)):
            self.view_model.run_current_script()

        imgui.same_line()

        # Reload Button
        if imgui.button("Reload"):  # , imgui.ImVec2(-1, 24)):
            self.view_model.reload_current_script()
        imgui.same_line()

        # Clear Button
        if imgui.button("Clear"):  # , imgui.ImVec2(-1, 24)):
            self.view_model.clear_output()
        imgui.same_line()

        if imgui.button("Reload Script Panles"):
            self.view_model.reload_script_panels()

    def close_script_tab_actions(self):
        name = self.view_model.confirming_close_name
        imgui.text(f"Script '{name}' has unsaved changes.")
        imgui.separator()

        if imgui.button("Save and Close"):
            self.view_model.save_script(name)
            self.view_model.force_close_editor(name)
            self.view_model.confirming_close_name = None
            imgui.close_current_popup()

        imgui.same_line()
        if imgui.button("Close Without Saving"):
            self.view_model.force_close_editor(name)
            self.view_model.confirming_close_name = None
            imgui.close_current_popup()

        imgui.same_line()
        if imgui.button("Cancel"):
            self.view_model.confirming_close_name = None
            imgui.close_current_popup()

    def render_code_space(self):
        to_close = []
        for name, (editor, tab) in self.view_model.editors.items():
            opened, visible = imgui.begin(name, True)

            if visible:
                self.view_model.data.current_tab_name = name
                imgui.text(f"Editing: {name}")
                if imgui_color_text_edit:
                    editor.render(name, imgui.get_content_region_avail())
                    # Update content from editor after rendering
                    new_content = editor.update_model()
                    if new_content != tab.content:
                        tab.content = new_content
                        tab.is_dirty = True
                else:
                    # Fallback to basic input text
                    changed, new_content = imgui.input_text_multiline(
                        "##editor",
                        tab.content,
                        imgui.get_content_region_avail(),
                        0
                    )
                    if changed:
                        tab.content = new_content
                        tab.is_dirty = True
            imgui.end()

            if not opened:
                if tab.is_dirty:
                    self.view_model.confirming_close_name = name
                else:
                    to_close.append(name)

        for name in to_close:
            self.view_model.force_close_editor(name)

    def render_runtime_panels(self):
        panels_to_remove = []
        for label, panel in self.view_model.runtime_panels.items():
            try:
                keep_open = panel.render()
                if keep_open is False:
                    panels_to_remove.append(label)
            except Exception as e:
                AppLogger.get().error(
                    f"❌ Failed to render runtime panel '{label}': {e}"
                )

        for label in panels_to_remove:
            del self.view_model.runtime_panels[label]



