import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import asyncio
import subprocess
from mylocale import tr
import locale
from pathlib import Path


class JarSigner(toga.App):
    def startup(self):
        self.mypath = self.paths.app.absolute()
        self.tr_file = f"{self.mypath}/resources/localisation.csv"
        self.locale = locale.getlocale()[0].split("_")[0]
        self.bundletool = "bundletool-all-1.17.2.jar"
        self.keystore_label = toga.Label(
            tr(
                csv_file=self.tr_file,
                langcode=self.locale,
                target_key="NOKEYFILESELECTED",
            ),
            style=Pack(text_align="center", padding=10),
        )
        self.android_label = toga.Label(
            tr(
                csv_file=self.tr_file,
                langcode=self.locale,
                target_key="NOAPK_AABFILESSELECTED",
            ),
            style=Pack(text_align="center", padding=10),
        )
        self.select_key = toga.Button(
            tr(
                csv_file=self.tr_file,
                langcode=self.locale,
                target_key="SELECTKEY",
            ),
            on_press=self.key_action_open_file_dialog,
            style=Pack(text_align="center", padding=10),
        )
        self.android_file_btn = toga.Button(
            tr(
                csv_file=self.tr_file,
                langcode=self.locale,
                target_key="SELECTAPK",
            ),
            style=Pack(text_align="center", padding=10),
            on_press=self.android_action_open_file_dialog,
        )
        self.alias_name = toga.TextInput(
            placeholder=tr(
                csv_file=self.tr_file,
                langcode=self.locale,
                target_key="ALIAS",
            ),
            style=Pack(text_align="center", padding=10),
        )
        self.password = toga.PasswordInput(
            placeholder=tr(
                csv_file=self.tr_file,
                langcode=self.locale,
                target_key="PASSWORD",
            ),
            style=Pack(text_align="center", padding=10),
        )
        signbtn = toga.Button(
            "Sign",
            style=Pack(text_align="center", padding=10),
            on_press=lambda _: self.sign(),
        )
        main_box = toga.Box(
            children=[
                self.keystore_label,
                self.android_label,
                self.select_key,
                self.android_file_btn,
                self.alias_name,
                self.password,
                signbtn,
            ],
            style=Pack(alignment="center", direction="column", flex=1),
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    async def android_action_open_file_dialog(self, widget):
        try:
            self.androidfile = await self.main_window.dialog(
                toga.OpenFileDialog("Open file with Toga", file_types=["apk", "aab"])
            )
            print(self.androidfile)
            if self.androidfile is not None:
                self.android_label.text = f"File to open: {self.androidfile}"
            else:
                self.android_label.text = "No apkfiles selected..."
        except ValueError:
            self.android_label.text = "Open file dialog was canceled"

    async def key_action_open_file_dialog(self, widget):
        try:
            self.keyfile = await self.main_window.dialog(
                toga.OpenFileDialog("Open file with Toga", file_types=["keystore"])
            )
            print(self.keyfile)
            if self.keyfile is not None:
                self.keystore_label.text = f"File to open: {self.keyfile}"
            else:
                self.keystore_label.text = "No keyfiles selected..."
        except ValueError:
            self.keystore_label.text = "Open file dialog was canceled"

    def sign(self):
        filetype = Path(str(self.androidfile)).suffix
        print(filetype)

    def sign_apk(self):
        try:
            self.cmd = f"jarsigner -keystore {self.keyfile} -storepass {self.password.value} {self.androidfile} {self.alias_name.value}"
            self.cmd = self.cmd.split(" ")
            print(self.cmd)
            process1 = subprocess.run(self.cmd)
            self.cmd_java = f"java -jar {self.bundletool} build-apks --bundle=app-release.aab --output=output.apks --ks={self.keyfile} --ks-key-alias={self.alias_name}"
            self.cmd_java = self.cmd_java.split(" ")
            print(self.cmd_java)
            process2 = subprocess.run(self.cmd_java)
            print(process1, process2)
            print("ready")
        except:
            print("Fail.")


def main():
    return JarSigner()
