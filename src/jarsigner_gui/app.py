"""
My first application
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import asyncio


class JarSigner(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        # jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore my_application.apk alias_name
        self.keystore_label = toga.Label("No files selected...")
        self.select_key = toga.Button(
            "Select Key",
            on_press=self.key_action_open_file_dialog,
        )
        self.apk_file = toga.Button(
            "Select APK file",
            on_press=self.apk_action_open_file_dialog,
        )
        self.alias_name = toga.TextInput(placeholder="Alias")
        self.password = toga.PasswordInput(placeholder="Password")
        signbtn = toga.Button("Sign")
        main_box = toga.Box(
            children=[
                self.keystore_label,
                self.select_key,
                self.apk_file,
                self.alias_name,
                self.password,
                signbtn,
            ]
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    async def apk_action_open_file_dialog(self, widget):
        try:
            self.apkfile = await self.main_window.dialog(
                toga.OpenFileDialog("Open file with Toga", file_types=["apk"])
            )
            print(self.apkfile)
            if self.apkfile is not None:
                self.keystore_label = f"File to open: {self.apkfile}"
            else:
                self.keystore_label = "No files selected..."
        except ValueError:
            self.keystore_label = "Open file dialog was canceled"

    async def key_action_open_file_dialog(self, widget):
        try:
            self.keyfile = await self.main_window.dialog(
                toga.OpenFileDialog("Open file with Toga", file_types=["keystore"])
            )
            if self.keyfile is not None:
                self.keystore_label = f"File to open: {self.keyfile}"
            else:
                self.keystore_label = "No file selected!"
        except ValueError:
            self.keystore_label = "Open file dialog was canceled"


def main():
    return JarSigner()
