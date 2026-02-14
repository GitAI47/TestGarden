# def get_exercises_menu(username=None):
def get_exercises_menu():
    return [
        {"name": "Oefening 1", "endpoint": "exercises.een_overview"},    
    ]


def get_instructions_menu():
    return [
        {"name": "Softwaretesten", "endpoint": "instructions.testen_overview"},
        {"name": "Git & GitHub", "endpoint": "instructions.git_overview"},
    ]


def get_scripts_menu():
    return [
        {"name": "Testcases", "endpoint": "scripts.cases_list"},
        {"name": "Nieuwe testcase", "endpoint": "scripts.cases_new"},
        {"name": "Start testrun", "endpoint": "scripts.run_start"},

    ]


def get_tools_menu():    return [
        {"name": "QRCode", "endpoint": "tools.qrcode_page"},
    ]

def get_main_menu(logged_in=False):
    if logged_in:
        return [
            {"name": "Home", "endpoint": "core.index"},
            {"name": "Logout", "endpoint": "users.logout"},
        ]
    return [
        {"name": "Home", "endpoint": "core.index"},
        {"name": "Login", "endpoint": "users.login"},
        {"name": "Register", "endpoint": "users.register"},
    ]


def get_all_menus(logged_in=False, username=None):
    return {
        "main": get_main_menu(logged_in),
        "exercises": get_exercises_menu(),
        "instructions": get_instructions_menu(),
        "tools": get_tools_menu(),
        "scripts": get_scripts_menu(),
    }


