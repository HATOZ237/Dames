# commande à taper en ligne de commande après la sauvegarde de ce fichier:
# python setup.py build

from cx_Freeze import setup, Executable
  
executables = [
        Executable(script = "main.py", base = "Win32GUI" )
]
# ne pas mettre "base = ..." si le programme n'est pas en mode graphique, comme c'est le cas pour chiffrement.py.
  
buildOptions = dict( 
        includes = ["math","sys","pygame","PyQt5.QtWidgets"],
        include_files = ["pion_noir.png", "pion_blanc.png", "dame_noir.png", "dame_blanc.png","Mouse Click - Free Sound Effect.mp3", "Super Mario Bros. Soundtrack-mc.mp3", "damier.py",
        "pion_pygame.py", "pion.py"]
)
  
setup(
    name = "Damier",
    version = "1.2",
    description = "Jeu de dames",
    author = "Duroy & Joyan",
    options = dict(build_exe = buildOptions),
    executables = executables
)