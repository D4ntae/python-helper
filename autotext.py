from pynput import keyboard
import colorama
import webbrowser

colorama.init()
keyboard_controller = keyboard.Controller()
MEMORY = ""
TO_BROWSE = ""
browser = webbrowser.Chrome(
    "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe")
PAUSE = False
# Make num one less that what to delete
SHORTCUTS_AUTOTYPE = {
    ("ALFA<ctrl_l>", 4): "Α",
    ("alfa<ctrl_l>", 4): "α",
    ("BETA<ctrl_l>", 4): "B",
    ("beta<ctrl_l>", 4): "β",
    ("GAMMA<ctrl_l>", 5): "Γ",
    ("gamma<ctrl_l>", 5): "γ",
    ("DELTA<ctrl_l>", 5): "Δ",
    ("delta<ctrl_l>", 5): "δ",
    ("EPSILON<ctrl_l>", 7): "E",
    ("epsilon<ctrl_l>", 7): "ε",
    ("ZETA<ctrl_l>", 4): "Z",
    ("zeta<ctrl_l>", 4): "ζ",
    ("EETA><ctrl_l>", 4): "H",
    ("eeta<ctrl_l>", 4): "η",
    ("THETA<ctrl_l>", 5): "Θ",
    ("theta<ctrl_l>", 5): "θ",
    ("IOTA<ctrl_l>", 4): "Ι",
    ("iota<ctrl_l>", 4): "ι",
    ("KAPPA<ctrl_l>", 5): "K",
    ("kappa<ctrl_l>", 5): "κ",
    ("LAMBDA<ctrl_l>", 6): "Λ",
    ("lambda<ctrl_l>", 6): "λ",
    ("MU<ctrl_l>", 2): "M",
    ("mu<ctrl_l>", 2): "μ",
    ("NU<ctrl_l>", 2): "N",
    ("nu<ctrl_l>", 2): "ν",
    ("XI<ctrl_l>", 2): "Ξ",
    ("xi<ctrl_l>", 2): "ξ",
    ("OMICRON<ctrl_l>", 6): "Ο",
    ("omicron<ctrl_l>", 6): "ο",
    ("PI<ctrl_l>", 2): "Π",
    ("pi<ctrl_l>", 2): "π",
    ("RHO<ctrl_l>", 3): "P",
    ("rho<ctrl_l>", 3): "ρ",
    ("SIGMA<ctrl_l>", 5): "Σ",
    ("sigma<ctrl_l>", 5): "σ",
    ("TAU<ctrl_l>", 3): "T",
    ("tau<ctrl_l>", 3): "τ",
    ("UPSILON<ctrl_l>", 6): "Y",
    ("upsilon<ctrl_l>", 6): "υ",
    ("PHI<ctrl_l>", 3): "Φ",
    ("phi<ctrl_l>", 3): "φ",
    ("CHI<ctrl_l>", 3): "X",
    ("chi<ctrl_l>", 3): "χ",
    ("PSI<ctrl_l>", 3): "Ψ",
    ("psi<ctrl_l>", 3): "ψ",
    ("OMEGA<ctrl_l>", 5): "Ω",
    ("omega<ctrl_l>", 5): "ω",
    ("ty<ctrl_l>", 2): "Thank you"
}


def log(*args, level=1):
    to_print = ""
    for i in args:
        to_print += i
        if len(args) > 1:
            to_print += ", "

    if level == 1:
        var = f"[INFO] {to_print}"
        print(colorama.Fore.GREEN, var)
    elif level == 2:
        var = f"[WARN] {to_print}"
        print(colorama.Fore.YELLOW, var)
    elif level == 3:
        var = f"[ERROR] {to_print}"
        print(colorama.Fore.RED, var)


def autotype_module():
    global MEMORY
    for mapping in SHORTCUTS_AUTOTYPE.keys():
        if mapping[0] in MEMORY:
            keyboard_controller.release(keyboard.Key.ctrl_l)
            for i in range(mapping[1]):
                keyboard_controller.press(keyboard.Key.backspace)
                keyboard_controller.release(keyboard.Key.backspace)
            keyboard_controller.type(SHORTCUTS_AUTOTYPE[mapping])
            MEMORY = ""
            break


def browser_module(key):
    global MEMORY
    global TO_BROWSE
    if "-google" in MEMORY:
        if key == "<shift>":
            query = TO_BROWSE.split(" ")
            query = query[1:]
            query = "+".join(query)
            browser.open(f"https://www.google.com/search?q={query}")
            MEMORY = ""
            TO_BROWSE = ""
        elif key == "<backspace>":
            TO_BROWSE = TO_BROWSE[:-1]
        elif key == "<space>":
            TO_BROWSE += " "
        else:
            TO_BROWSE += key


def on_press(key):
    global MEMORY

    k = str(key).replace("'", "")
    if "Key." in k:
        k = k.replace("Key.", "<")
        k += ">"

    # Make backspace possible
    if k == "<backspace>":
        MEMORY = MEMORY[:-1]
    else:
        MEMORY += k
    if not PAUSE:
        autotype_module()
        browser_module(k)

    if len(MEMORY) > 100:
        MEMORY = ""


def on_release(key):
    global PAUSE
    global MEMORY
    if "quitlogging" in MEMORY:
        log("Quiting logging...")
        for i in range(11):
            keyboard_controller.press(keyboard.Key.backspace)
            keyboard_controller.release(keyboard.Key.backspace)
        return False
    elif "pauselogging" in MEMORY:
        for i in range(12):
            keyboard_controller.press(keyboard.Key.backspace)
            keyboard_controller.release(keyboard.Key.backspace)
        PAUSE = True
    elif "continuelogging" in MEMORY:
        for i in range(15):
            keyboard_controller.press(keyboard.Key.backspace)
            keyboard_controller.release(keyboard.Key.backspace)
        PAUSE = False
    elif "clearlogmem" in MEMORY:
        MEMORY = ""


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
