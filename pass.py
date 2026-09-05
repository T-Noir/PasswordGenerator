import customtkinter as ctk
import secrets
import string
import tkinter as tk

APP_NAME = "pass"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


def generate_password(length: int) -> str:
    length = max(4, int(length))
    groups = [
        string.ascii_uppercase,
        string.ascii_lowercase,
        string.digits,
        string.punctuation,
    ]
    password = [secrets.choice(group) for group in groups]
    alphabet = "".join(groups)
    password += [secrets.choice(alphabet) for _ in range(length - 4)]
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


class PasswordApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("620x390")
        self.minsize(560, 350)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(
            self, text="Password Generator",
            font=ctk.CTkFont(size=28, weight="bold"),
        )
        title.grid(row=0, column=0, padx=30, pady=(28, 10))

        frame = ctk.CTkFrame(self, corner_radius=18)
        frame.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        self.password_var = tk.StringVar(value="")
        self.password_entry = ctk.CTkEntry(
            frame, textvariable=self.password_var, height=48,
            font=ctk.CTkFont(size=18), justify="center",
        )
        self.password_entry.grid(row=0, column=0, columnspan=2, padx=25, pady=(25, 15), sticky="ew")

        length_label = ctk.CTkLabel(frame, text="Length")
        length_label.grid(row=1, column=0, padx=25, pady=5, sticky="w")

        self.length = ctk.CTkSlider(frame, from_=4, to=64, number_of_steps=60, command=self.update_length)
        self.length.set(16)
        self.length.grid(row=2, column=0, padx=25, pady=(0, 2), sticky="ew")

        self.length_value = ctk.CTkLabel(frame, text="16")
        self.length_value.grid(row=2, column=1, padx=(5, 25), pady=(0, 2))

        self.generate_button = ctk.CTkButton(frame, text="Create", height=44, corner_radius=12, command=self.create_password)
        self.generate_button.grid(row=3, column=0, padx=(25, 8), pady=25, sticky="ew")

        self.copy_button = ctk.CTkButton(frame, text="Copy", height=44, corner_radius=12, command=self.copy_password)
        self.copy_button.grid(row=3, column=1, padx=(8, 25), pady=25, sticky="ew")

        self.status = ctk.CTkLabel(frame, text="")
        self.status.grid(row=4, column=0, columnspan=2, pady=(0, 18))

    def update_length(self, value):
        self.length_value.configure(text=str(round(value)))

    def create_password(self):
        password = generate_password(round(self.length.get()))
        self.password_var.set(password)
        self.status.configure(text="Password created")

    def copy_password(self):
        password = self.password_var.get()
        if not password:
            self.status.configure(text="Create a password first")
            return
        self.clipboard_clear()
        self.clipboard_append(password)
        self.update()
        self.status.configure(text="Copied ✓")


if __name__ == "__main__":
    app = PasswordApp()
    app.mainloop()
