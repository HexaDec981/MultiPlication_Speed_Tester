import customtkinter as ctk
from PIL import Image, ImageTk, ImageFilter
import random
import time
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime

# CSV setup
CSV_FILENAME = "records.csv"
CSV_FIELDS = ["Question", "TimeTaken(s)", "Correct", "Timestamp"]

# Create the file if it doesn't exist
if not os.path.isfile(CSV_FILENAME):
    with open(CSV_FILENAME, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()

# Store attempts for plotting and stats
attempts = []

class MultiplicationApp:
    def __init__(self, master):
        self.master = master
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        master.title("Multiplication Speed Tester")
        master.geometry("500x500")

        self.font = ("Segoe UI", 16)
        self.accent_color = "#5e81ac"  # Hyprland blue
        self.bg_color = "#23272e"      # Hyprland dark
        self.glass_color = "#2e3440"

        # Main frame with glass effect
        self.frame = ctk.CTkFrame(master, fg_color=self.glass_color, corner_radius=20)
        self.frame.pack(expand=True, fill="both", padx=30, pady=30)

        # Title
        self.title_label = ctk.CTkLabel(self.frame, text="Multiplication Speed Tester", font=("Segoe UI", 22, "bold"), text_color=self.accent_color)
        self.title_label.pack(pady=(10, 20))

        # Question
        self.question_label = ctk.CTkLabel(self.frame, text="", font=self.font, text_color="#eceff4")
        self.question_label.pack(pady=20)

        # Entry
        self.entry = ctk.CTkEntry(self.frame, font=self.font, corner_radius=10, border_color=self.accent_color, border_width=2)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda event: self.check_answer())

        # Buttons with microanimations
        self.submit_btn = self.create_animated_button(self.frame, "Submit", self.check_answer)
        self.submit_btn.pack(pady=10)

        self.plot_btn = self.create_animated_button(self.frame, "Plot Results", self.plot_results)
        self.plot_btn.pack(pady=10)

        self.stats_btn = self.create_animated_button(self.frame, "View Stats", self.show_stats)
        self.stats_btn.pack(pady=10)

        # Feedback
        self.feedback_label = ctk.CTkLabel(self.frame, text="", font=self.font, text_color="#a3be8c")
        self.feedback_label.pack(pady=5)

        # Filter dropdown
        self.filter_var = ctk.StringVar()
        self.filter_dropdown = ctk.CTkComboBox(self.frame, variable=self.filter_var, values=["All", "Correct Only", "Wrong Only"], font=("Segoe UI", 12), fg_color="#3b4252", button_color=self.accent_color)
        self.filter_dropdown.set("All")
        self.filter_dropdown.pack(pady=5)

        self.next_question()

    def create_animated_button(self, parent, text, command):
        btn = ctk.CTkButton(parent, text=text, command=command, font=("Segoe UI", 15, "bold"), fg_color=self.accent_color, hover_color="#81a1c1", corner_radius=12, text_color="#eceff4")
        # Microanimation: color transition on hover
        def on_enter(e):
            btn.configure(fg_color="#81a1c1")
        def on_leave(e):
            btn.configure(fg_color=self.accent_color)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def next_question(self):
        self.num1 = random.randint(13, 20)
        # Only allow num2 from 2 to 9 (exclude 1 and 10)
        self.num2 = random.randint(2, 9)
        self.answer = self.num1 * self.num2
        self.question_label.configure(text=f"What is {self.num1} × {self.num2}?")
        self.entry.delete(0, ctk.END)
        self.feedback_label.configure(text="")
        self.start_time = time.time()

    def check_answer(self):
        user_input = self.entry.get()
        try:
            user_answer = int(user_input)
            elapsed_time = round(time.time() - self.start_time, 2)
            correct = user_answer == self.answer
            question_str = f"{self.num1}×{self.num2}"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Feedback
            self.feedback_label.configure(
                text=f"{'✅ Correct' if correct else '❌ Wrong'} | Time: {elapsed_time}s"
            )

            # Add to memory
            attempts.append((question_str, elapsed_time, correct))

            # Log to CSV
            with open(CSV_FILENAME, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
                writer.writerow({
                    "Question": question_str,
                    "TimeTaken(s)": elapsed_time,
                    "Correct": correct,
                    "Timestamp": timestamp
                })

            self.master.after(500, self.next_question)
        except ValueError:
            self.feedback_label.configure(text="Please enter a valid number!")

    def plot_results(self):
        if not attempts:
            self.feedback_label.configure(text="No data to plot!")
            return

        selected_filter = self.filter_var.get()
        filtered = []

        if selected_filter == "Correct Only":
            filtered = [t for t in attempts if t[2]]
        elif selected_filter == "Wrong Only":
            filtered = [t for t in attempts if not t[2]]
        else:
            filtered = attempts

        if not filtered:
            self.feedback_label.configure(text="No data matches the filter!")
            return

        times = [t[1] for t in filtered]
        labels = [t[0] for t in filtered]
        colors = ['green' if t[2] else 'red' for t in filtered]

        plt.figure(figsize=(10, 5))
        plt.bar(labels, times, color=colors)
        plt.xlabel("Question")
        plt.ylabel("Time (s)")
        plt.title(f"Response Times ({selected_filter})")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def show_stats(self):
        if not attempts:
            self.feedback_label.configure(text="No attempts yet!")
            return

        total = len(attempts)
        correct = sum(1 for a in attempts if a[2])
        wrong = total - correct
        avg_time = round(sum(a[1] for a in attempts) / total, 2)
        accuracy = round((correct / total) * 100, 2)

        stats_text = (
            f"📊 Stats:\n"
            f"Total Attempts: {total}\n"
            f"Correct: {correct}\n"
            f"Wrong: {wrong}\n"
            f"Average Time: {avg_time} seconds\n"
            f"Accuracy: {accuracy}%"
        )

        # Popup window
        stats_window = ctk.CTkToplevel(self.master)
        stats_window.title("Your Stats")
        stats_window.geometry("320x220")
        stats_window.configure(bg=self.bg_color)

        stats_frame = ctk.CTkFrame(stats_window, fg_color=self.glass_color, corner_radius=18)
        stats_frame.pack(expand=True, fill="both", padx=15, pady=15)

        stats_label = ctk.CTkLabel(stats_frame, text=stats_text, font=("Segoe UI", 13), justify="left", text_color="#eceff4")
        stats_label.pack(padx=20, pady=20)


if __name__ == "__main__":
    root = ctk.CTk()
    app = MultiplicationApp(root)
    root.mainloop()
