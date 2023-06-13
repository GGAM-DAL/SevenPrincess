# Disply Site Logo & Home Button
def title():
    html="""
    <style>
    a {
    text-decoration-line: none;
    }
    </style>
    <a href="http://localhost:8501/" target="_self">🏠 Home</a>
    <center>
        <img src='https://github.com/GGAM-DAL/SevenPrincess/blob/GGAM-DAL/static/logo.png?raw=true'
        alt='logo' style='width: 600px;'><hr><br>
    </center>
    
    """
    return html