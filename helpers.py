from flask import render_template
from flask_login import current_user


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """

        ## これのいみがわからない
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
        
    return render_template("apology.html", top=code, bottom=escape(message), user=current_user), code


def show_datetime(t):
    return t.strftime('%Y-%m-%d')