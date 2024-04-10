'''
    Contains the server to run our application.
'''
from flask_failsafe import failsafe
import sys
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))


@failsafe
def create_app():
    '''
        Gets the underlying Flask server from our Dash app.

        Returns:
            The server to be run
    '''
    # The import is intentionally inside to work with the server failsafe
    from src.app import app  # pylint: disable=import-outside-toplevel
    return app.server


server = create_app()

if __name__ == "__main__":
    server.run(port=8050, debug=True)
