import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator

# =========================
# Language Dictionary
# =========================

LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Arabic": "ar",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Portuguese": "pt",
    "Russian": "ru",
    "Italian": "it",
    "Turkish": "tr",
    "Urdu": "ur"
}

history = []

# =========================
# Functions
# =========================

def translate_text():
    text = input_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning(
            "Empty Input",
            "Please enter text."
        )
        return

    source = LANGUAGES[src_lang.get()]
    target = LANGUAGES[tgt_lang.get()]

    if source == target and source != "auto":
        messagebox.showinfo(
            "Same Language",
            "Source and target language are same."
        )
        return

    try:
        translated = GoogleTranslator(
            source=source,
            target=target
        ).translate(text)

        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated)
        output_text.config(state="disabled")

        history.append(
            f"{src_lang.get()} → {tgt_lang.get()}\n{translated}"
        )

        update_history()

    except Exception as e:
        messagebox.showerror(
            "Translation Error",
            str(e)
        )


def update_history():
    history_box.config(state="normal")
    history_box.delete("1.0", tk.END)

    for item in history[-10:]:
        history_box.insert(tk.END, item + "\n\n")

    history_box.config(state="disabled")


def copy_translation():
    text = output_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning(
            "Warning",
            "Nothing to copy."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(text)

    messagebox.showinfo(
        "Copied",
        "Translation copied."
    )


def save_translation():
    text = output_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning(
            "Warning",
            "Nothing to save."
        )
        return

    with open(
        "translation.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(text)

    messagebox.showinfo(
        "Saved",
        "Translation saved as translation.txt"
    )


def clear_all():
    input_text.delete("1.0", tk.END)

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.config(state="disabled")

    count_label.config(text="Characters: 0")


def swap_languages():
    if src_lang.get() == "Auto Detect":
        return

    source = src_lang.get()
    target = tgt_lang.get()

    src_lang.set(target)
    tgt_lang.set(source)


def count_characters(event=None):
    count = len(
        input_text.get("1.0", tk.END).strip()
    )

    count_label.config(
        text=f"Characters: {count}"
    )


# =========================
# Main Window
# =========================

root = tk.Tk()
root.title("Language Translation Tool")
root.geometry("800x700")
root.configure(bg="#1e1e2f")
root.resizable(False, False)

# =========================
# Title
# =========================

title = tk.Label(
    root,
    text="🌐 Language Translation Tool",
    font=("Segoe UI", 18, "bold"),
    bg="#1e1e2f",
    fg="#7c6ef5"
)
title.pack(pady=10)

subtitle = tk.Label(
    root,
    text="CodeAlpha Artificial Intelligence Internship",
    bg="#1e1e2f",
    fg="gray"
)
subtitle.pack()

# =========================
# Language Selection
# =========================

frame_lang = tk.Frame(
    root,
    bg="#1e1e2f"
)
frame_lang.pack(pady=15)

src_lang = tk.StringVar()
src_lang.set("Auto Detect")

tgt_lang = tk.StringVar()
tgt_lang.set("Hindi")

tk.Label(
    frame_lang,
    text="Source Language",
    bg="#1e1e2f",
    fg="white"
).grid(row=0, column=0)

tk.Label(
    frame_lang,
    text="Target Language",
    bg="#1e1e2f",
    fg="white"
).grid(row=0, column=2)

src_box = ttk.Combobox(
    frame_lang,
    textvariable=src_lang,
    values=list(LANGUAGES.keys()),
    state="readonly",
    width=20
)
src_box.grid(row=1, column=0, padx=10)

swap_btn = tk.Button(
    frame_lang,
    text="⇄",
    font=("Arial", 14, "bold"),
    command=swap_languages,
    bg="#333344",
    fg="white"
)
swap_btn.grid(row=1, column=1)

tgt_box = ttk.Combobox(
    frame_lang,
    textvariable=tgt_lang,
    values=list(LANGUAGES.keys())[1:],
    state="readonly",
    width=20
)
tgt_box.grid(row=1, column=2, padx=10)

# =========================
# Input Text
# =========================

tk.Label(
    root,
    text="Enter Text",
    bg="#1e1e2f",
    fg="white",
    font=("Segoe UI", 10, "bold")
).pack(anchor="w", padx=40)

input_text = tk.Text(
    root,
    height=8,
    width=80,
    bg="#2b2b3c",
    fg="white",
    insertbackground="white"
)
input_text.pack(padx=40, pady=5)

input_text.bind(
    "<KeyRelease>",
    count_characters
)

count_label = tk.Label(
    root,
    text="Characters: 0",
    bg="#1e1e2f",
    fg="#bbbbbb"
)
count_label.pack(anchor="e", padx=40)

# =========================
# Buttons
# =========================

button_frame = tk.Frame(
    root,
    bg="#1e1e2f"
)
button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text="Translate",
    command=translate_text,
    bg="#7c6ef5",
    fg="white",
    font=("Segoe UI", 10, "bold")
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Copy",
    command=copy_translation,
    bg="#40a02b",
    fg="white"
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Save",
    command=save_translation,
    bg="#209fb5",
    fg="white"
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Clear",
    command=clear_all,
    bg="#e64553",
    fg="white"
).pack(side="left", padx=5)

# =========================
# Output
# =========================

tk.Label(
    root,
    text="Translation",
    bg="#1e1e2f",
    fg="white",
    font=("Segoe UI", 10, "bold")
).pack(anchor="w", padx=40)

output_text = tk.Text(
    root,
    height=8,
    width=80,
    bg="#2b2b3c",
    fg="#9eff9e",
    state="disabled"
)
output_text.pack(padx=40, pady=5)

# =========================
# History
# =========================

tk.Label(
    root,
    text="Translation History",
    bg="#1e1e2f",
    fg="white",
    font=("Segoe UI", 10, "bold")
).pack(anchor="w", padx=40, pady=(15, 0))

history_box = tk.Text(
    root,
    height=8,
    width=80,
    bg="#2b2b3c",
    fg="#cccccc",
    state="disabled"
)
history_box.pack(padx=40, pady=5)

# =========================
# Run App
# =========================

root.mainloop()