# 🚀 Retirement Readiness
Our venture helps prepare individuals who are on a path to retirement and want to be educated in various retirement plans. 

---

## 👥 Team Members & Roles
- **Javier Castillo** — Project Lead
- **Joaquin Castillo** — AI Dev
- **Abcde Mireles** — UI Designer
- **Jose Torres** — Data Gatherer

---
## Link to Latest Docs
[**PRD**](https://github.com/jcastillo0220/Retirement-Readiness/blob/main/docs/PRD.pdf)<br>
[**Spike Plan**](https://github.com/jcastillo0220/Retirement-Readiness/blob/main/docs/Spike%20Plan.pdf)<br>
[**Pitch Deck**](https://github.com/jcastillo0220/Retirement-Readiness/blob/bbb02bedf890d70adcc42897e60de980f2cbb1ea/docs/Pitch%20Deck.pdf)<br>

## 🛠️ How to Run the Project in VS Code 
### Backend
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Check if you have Python installed. If you do, skip to step 4.
   ```bash
   py --version
   ```
3. Install Python from its offical [website](https://www.python.org/downloads/)
   -  Once it finishes installed, restart VS Code and redo step 2.
4. Check if you have pip installed. If you do, skip to step 6.
   ```bash
   py -m pip --version
   ```
5. Install pip in your terminal. Once installed, restart VS Code and redo step 4.
   ```bash
   py -m ensurepip --upgrade
   ```
6. Check if you have uvicorn installed. If you do, skip to step 8.
   ```bash
   py -m uvicorn --version
   ```
7. Install uvicorn in your terminal. Once installed, restart VS Code and redo step 6.
   ```bash
   py -m pip install uvicorn
   ```
8. Install fastapi module
   ```bash
   py -m pip install fastapi
   ```
9. Install dotenv package
   ```bash
   py -m pip install python-dotenv
   ```
10. Install BeautifulSoup package
   ```bash
   py -m pip install beautifulsoup4
   ```
11. Install requests package
   ```bash
   py -m pip install requests
   ```
12. Install PyPDF2 reader
   ```bash
   py -m pip install PyPDF2
   ```
13. Install google-genai module
   ```bash
   py -m pip install google-genai
   ```
14. Check if the backend is running correctly. **Make sure to always have this running when you want to use the application**
   ```bash
   py -m uvicorn endpoint:app --reload
   ```

### Frontend
1. Navigate to frontend folder on a different terminal - **Still keep the older terminal**
   ```bash
   cd frontend
   ```
2. Check if you have Node.js installed, if not, install from offical [website](https://nodejs.org/en/download) and restart VS Code
   ```bash
   node --version
   ```
3. Install npm in the frontend folder
   ```bash
   npm install
   ```
4. Install vite and restart VS Code after installation.
   ```bash
   npm install -g vite
   ```
5. Install Tailwind and PostCSS
   ```bash
   npm install -D tailwindcss postcss autoprefixer
   ```
6. Install Rehype-raw
   ```bash
   npm install rehype-raw
   ```
7. Now Run:
   ```bash
   npm run dev
   ```
8. Navigate to the local host link in the terminal. **Make sure you always run your frontend as well when connecting to the application**

