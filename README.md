# 🧠 SenseMate
### An Accessible & Beginner-Friendly Human-AI Platform for Qualitative Data Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![AI-Powered](https://img.shields.io/badge/AI-Rationale--Extraction-orange.svg)]()

**SenseMate** is a novel semi-automated platform designed to streamline the qualitative coding process. By bridging the gap between manual human judgment and machine efficiency, SenseMate helps researchers and community organizations transform unstructured data into actionable insights with higher reliability and less effort.

---

## ✨ Key Features

- **🤖 Rationale Extraction Models:** Unlike black-box LLMs, SenseMate provides theme recommendations paired with human-interpretable explanations (rationales), ensuring transparency in AI suggestions.
- **📈 Increased Reliability:** Scientifically proven to increase intercoder reliability (Cohen’s Kappa) by **29%** and coding F-scores by **10%** for novice coders.
- **🎨 Human-Centered UI:** Designed specifically for beginners and non-technical users, featuring an intuitive dashboard for managing unstructured datasets.
- **🔍 Cognitive Forcing Functions:** Purposefully designed workflows that prevent AI over-reliance, encouraging users to critically evaluate machine suggestions.
- **⚖️ Privacy-First:** Focused on localizable models and rationale extraction to maintain data control and user privacy.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js & NPM (for frontend components)
- [Add any specific database requirements here, e.g., PostgreSQL/MongoDB]

### Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/Chakrabortysoura/SenseMate.git](https://github.com/Chakrabortysoura/SenseMate.git)
   cd SenseMate

2. **Set up Backend**
cd backend
pip install -r requirements.txt
python manage.py migrate  # If using Django
python manage.py runserver

3. **Set up frontend**
cd frontend
npm install
npm start

🛠 How It Works
SenseMate follows a three-step workflow to assist in sensemaking:
a. Upload: Import your unstructured corpus (interviews, community feedback, survey responses).
b. AI Analysis: The Rationale Extraction Model scans the text, highlighting specific segments and recommending relevant themes/codes.
c. Refine: Human coders review the AI's "rationale," accepting, rejecting, or modifying the codes to ensure high-quality, nuanced analysis.

📊 Evaluation & Impact
Based on research conducted at the MIT Media Lab, SenseMate was evaluated through experiments involving 180+ participants. Results showed:
Accuracy: Significant reduction in differences between novice and expert coding decisions.
Usability: High system usability scores from community-based organization members.
Engagement: Users felt more confident in their coding decisions when supported by the rationale-extraction interface.

🏗 Project Structure
SenseMate/
├── backend/            # Python/Django API & ML Models
│   ├── models/         # Rationale Extraction Logic
│   └── api/            # REST Endpoints
├── frontend/           # React/Vue.js User Interface
├── data/               # Sample datasets and annotations
├── docs/               # Technical documentation and Research Paper
└── README.md

🤝 Contributing
Contributions are welcome! Whether it's improving the ML models, fixing UI bugs, or enhancing documentation:

1. Fork the Project.
2. Create your Feature Branch (git checkout -b feature/AmazingFeature).
3. Commit your Changes (git commit -m 'Add some AmazingFeature').
4. Push to the Branch (git push origin feature/AmazingFeature).
5. Open a Pull Request.

📄 License
Distributed under the MIT License. See LICENSE for more information.
