# Multiplication Speed Tester

A modern, visually appealing desktop app to practice and track multiplication speed. Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), this app helps users improve their multiplication skills, visualize progress, and analyze performance stats.

## Features

- **Randomized Questions:** Practice multiplication with numbers 13–20 × 1–10.
- **Speed Tracking:** Measures and displays your response time for each question.
- **Instant Feedback:** Shows if your answer is correct or wrong, with time taken.
- **Animated UI:** Stylish buttons and glass-effect panels for a modern look.
- **Result Plotting:** Visualize your response times with color-coded bar charts (green for correct, red for wrong).
- **Stats Window:** View total attempts, correct/wrong counts, average time, and accuracy.
- **CSV Logging:** All attempts are saved to `records.csv` for persistent tracking.
- **Filter Results:** Plot and analyze only correct, wrong, or all attempts.

## Screenshots

![App Screenshot](screenshot.png)

## Installation

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/yourusername/multiplication-speed-tester.git
   cd multiplication-speed-tester
   ```
2. **Install dependencies:**
   ```powershell
   pip install customtkinter pillow matplotlib
   ```

## Usage

Run the app with:

```powershell
python main.py
```

## File Structure

- `main.py` — Main application code
- `records.csv` — Stores your attempt history
- `README.md` — Project documentation

## Requirements

- Python 3.8+
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Pillow
- Matplotlib

## Contributing

Pull requests and suggestions are welcome! Please open an issue for major changes.

## License

This project is licensed under the MIT License.

---

_Made with ❤️ using CustomTkinter._
