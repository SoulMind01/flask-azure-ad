# Flask Azure AD Task Manager

This is a simple task manager application built with Flask and integrated with Azure Active Directory (Azure AD) for authentication. The application allows users to log in using their Azure AD credentials, view their tasks, add new tasks.


## Setup

### Prerequisites

- Python 3.x
- Azure AD tenant and application registration
- Flask

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/SoulMind01/flask-azure-ad.git 
    cd flask-azure-ad
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Update the Azure AD credentials in .py`app`:

    ```python
    CLIENT_ID = "your_client_id"
    TENANT_ID = "your_tenant_id"
    CLIENT_SECRET = "your_client_secret"
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    REDIRECT_URI = "http://localhost:5000/getToken"  # Update this with your Redirect URI if you do not deploy locally
    SCOPES = ["User.Read"]
    ```

5. Initialize the SQLite database:

    ```sh
    python app.py
    ```

## Running the Application

1. Start the Flask development server:

    ```sh
    python app.py
    ```

2. Open your web browser and navigate to `http://localhost:5000`.

## Application Routes

- `/`: Home page with login link.
- `/login`: Redirects to Azure AD login page.
- `/getToken`: Callback URL for Azure AD to get the authorization token.
- `/tasks`: Displays the user's tasks.
- `/add`: Adds a new task (POST method).
- `/delete/<int:id>`: Deletes a task (admin only).
- `/logout`: Logs out the user.

## Templates

- [home.html](http://_vscodecontentref_/3): Home page template.
- [tasks.html](http://_vscodecontentref_/4): Tasks page template.
