# 🐱 Cats and Dogs — Hand Tracking Game  

A Python game where you control a cat with your index finger using your webcam. Collect coins, avoid dogs, and enjoy a fun mix of computer vision and game mechanics.  

🏆 Built during a hackathon with my teammate **Ana Paula Castro**, where we achieved **Runner-Up**.  
🔗 Devpost project page: [Cats and Dogs](https://devpost.com/software/cats-and-dogs)  

---

## ✨ Features  
- 🎮 **Hand Tracking Control** → Move the cat with your index finger using your webcam  
- 🪙 **Coin Collection** → Earn points by collecting coins  
- 🐶 **Random Dog Movement** → Avoid the dogs, or the game ends!  
- 🎵 **Background Music** → Fun and immersive gameplay  

---

## 🛠️ Tech Stack  
- **Python 3.10+**  
- **Pygame** → graphics & sound  
- **OpenCV** → video capture  
- **MediaPipe** → hand tracking  

---

## 📂 Project Structure  

cats-and-dogs-hand-tracking/
├─ assets/ # Images and music
│ ├─ cat.png
│ ├─ dog.png
│ └─ cat_song.wav
├─ src/
│ └─ main.py # Game entry point
├─ requirements.txt # Dependencies
├─ README.md
├─ .gitignore
└─ LICENSE


---

## 🚀 Quick Start  

### 1. Clone the repo  
```bash
git clone https://github.com/angela-hg/cats-and-dogs-hand-tracking.git
cd cats-and-dogs-hand-tracking


### 2. Set up a virtual environment (recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run the game
python src/main.py


💡 If macOS asks for camera permissions, grant access to your terminal or IDE in System Settings → Privacy & Security → Camera.

🎮 Controls

- Move your index finger in front of the webcam to move the cat 🐱
- Collect coins 🪙 → +1 point each
- Avoid the dogs 🐶 → collision ends the game
- Close the window to quit

🧩 Troubleshooting

- Webcam not detected → ensure no other app is using it & permissions are granted.
- MediaPipe errors → works best on Python 3.10 or 3.11.
- No music → check that assets/cat_song.wav exists.

📄 License

MIT — see LICENSE

🙌 Credits

Created by Angela and Ana during a hackathon.
Built with Pygame, OpenCV, and MediaPipe.


