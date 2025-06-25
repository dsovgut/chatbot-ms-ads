# Generative AI Principles Midterm
This guide explains how to run the Chainlit frontend for the MS in Applied Data Science program AI chatbot.

**Prerequisites:**
* Python 3.9 or higher installed on your system.
* Access to an OpenAI API key.

**Setup Steps:**

1.  **Place Project Files:**
    * Ensure all project files (`app/main.py`, `requirements.txt`, `public/` folder, `chainlit.md`, `chainlit.toml`, etc.) are in a single project folder on your computer (e.g., `MS-ADS-ADVISOR`).

2.  **Open a Terminal:**
    * Navigate into your project folder using your terminal (e.g., Command Prompt, PowerShell, or macOS/Linux Terminal).
        ```bash
        cd path/to/your/MS-ADS-ADVISOR
        ```

3.  **Create and Activate a Virtual Environment (Highly Recommended):**
    * This keeps the project's Python packages separate from others on your system.
        ```bash
        # Create a virtual environment named .venv
        python3 -m venv .venv 
        
        # Activate it:
        # On macOS/Linux:
        source .venv/bin/activate
        # On Windows (Command Prompt):
        # .venv\Scripts\activate.bat
        # On Windows (PowerShell):
        # .venv\Scripts\Activate.ps1
        ```
    * Your terminal prompt should now show `(.venv)` at the beginning.

4.  **Install Required Packages:**
    * With the virtual environment active, install all dependencies:
        ```bash
        pip install -r requirements.txt
        ```

5.  **Set Up Environment Variables (API Key):**
    * In the main project folder (`MS-ADS-ADVISOR`), create a new file named `.env`.
    * Open this `.env` file with a text editor and add your OpenAI API key:
        ```
        OPENAI_API_KEY=sk-your_actual_openai_api_key_here
        ```
    * Replace `sk-your_actual_openai_api_key_here` with your real API key. Save the file.

**Running the Application:**

1.  **Ensure your virtual environment is active** (you should see `(.venv)` in your terminal prompt).
2.  From the project's main folder in your terminal, run:
    ```bash
    chainlit run app/main.py -w --port 8005
    ```
    * You can change `8005` to another port number (e.g., `8001`) if `8005` is already in use.
    * The `-w` flag enables auto-reload if you make changes to the `app/main.py` file.
3.  Open your web browser and go to `http://localhost:8005` (or the port you used). You should see the chat interface.
