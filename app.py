import tkinter as tk
from tkinter import filedialog
import pygame
import random

class DrumMachine:
    def __init__(self, master):
        self.master = master
        self.master.title("Professional Drum Machine")
        pygame.mixer.init()

        self.instruments = ["Kick", "Snare", "HiHat", "Clap"]
        self.sample_files = {
            "Kick": "kick.wav",
            "Snare": "snare.wav",
            "HiHat": "hihat.wav",
            "Clap": "clap.wav"
        }
        self.sounds = {}
        for inst in self.instruments:
            try:
                self.sounds[inst] = pygame.mixer.Sound(self.sample_files[inst])
            except Exception as e:
                print(f"Error loading {inst}: {e}")

        self.rows = len(self.instruments)
        self.cols = 16

        self.grid_vars = [
            [tk.IntVar() for _ in range(self.cols)] for _ in range(self.rows)
        ]

        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            tk.Label(master, text=self.instruments[r],
                     font=("Helvetica", 12, "bold")).grid(row=r, column=0, padx=5, pady=5)
            for c in range(self.cols):
                btn = tk.Checkbutton(master, variable=self.grid_vars[r][c])
                btn.grid(row=r, column=c+1, padx=2, pady=2)
                self.buttons[r][c] = btn

        self.bpm = tk.IntVar(value=120)
        tk.Label(master, text="BPM", font=("Helvetica", 10)).grid(
            row=self.rows, column=0, padx=5, pady=5)
        self.bpm_slider = tk.Scale(master, from_=60, to=240, orient=tk.HORIZONTAL, variable=self.bpm)
        self.bpm_slider.grid(row=self.rows, column=1, columnspan=4, padx=5, pady=5)

        self.is_playing = False
        self.current_step = 0

        self.start_button = tk.Button(master, text="Start", command=self.start, width=10)
        self.start_button.grid(row=self.rows+1, column=0, padx=5, pady=5)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop, width=10)
        self.stop_button.grid(row=self.rows+1, column=1, padx=5, pady=5)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset, width=10)
        self.reset_button.grid(row=self.rows+1, column=2, padx=5, pady=5)

        self.random_button = tk.Button(master, text="Random", command=self.randomize, width=10)
        self.random_button.grid(row=self.rows+1, column=3, padx=5, pady=5)

        self.load_buttons = []
        for i, inst in enumerate(self.instruments):
            btn = tk.Button(master, text=f"Load {inst} Sample", command=lambda inst=inst: self.load_sample(inst))
            btn.grid(row=self.rows+2+i, column=0, columnspan=4, padx=5, pady=3)
            self.load_buttons.append(btn)

    def start(self):
        if not self.is_playing:
            self.is_playing = True
            self.run_sequence()

    def stop(self):
        self.is_playing = False
        self.reset_button_highlight()

    def reset(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid_vars[r][c].set(0)
        self.current_step = 0
        self.reset_button_highlight()

    def randomize(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid_vars[r][c].set(random.choice([0, 1]))

    def load_sample(self, instrument):
        file_path = filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])
        if file_path:
            try:
                self.sounds[instrument] = pygame.mixer.Sound(file_path)
                self.sample_files[instrument] = file_path
            except Exception as e:
                print(f"Error loading sample for {instrument}: {e}")

    def reset_button_highlight(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c].configure(bg="SystemButtonFace")

    def run_sequence(self):
        if not self.is_playing:
            return

        bpm_value = self.bpm.get()
        delay = int((60 / bpm_value) * 1000 / 4)

        prev_step = (self.current_step - 1) % self.cols
        for r in range(self.rows):
            self.buttons[r][prev_step].configure(bg="SystemButtonFace")
            self.buttons[r][self.current_step].configure(bg="yellow")

        for r in range(self.rows):
            if self.grid_vars[r][self.current_step].get() == 1:
                inst = self.instruments[r]
                if inst in self.sounds:
                    self.sounds[inst].play()

        self.current_step = (self.current_step + 1) % self.cols
        self.master.after(delay, self.run_sequence)

if __name__ == "__main__":
    root = tk.Tk()
    app = DrumMachine(root)
    root.mainloop()
