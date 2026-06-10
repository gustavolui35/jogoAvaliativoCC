
import cx_Freeze

build_exe_options = {
    "packages": [
        "pygame",
        "pyttsx3"
    ],

    "includes": [
        "pyttsx3.drivers",
        "pyttsx3.drivers.sapi5"
    ],

    "include_files": [
        "bases",
        "recursos"
    ]
}

executaveis = [
    cx_Freeze.Executable(
        script="main.py",
        icon="bases/Icone.png",   # ou coloque o caminho correto do seu ícone .ico
        target_name="TaxiGTA.exe"
    )
]

cx_Freeze.setup(
    name="Taxi GTA",
    version="1.0",
    description="Jogo de Táxi",
    options={
        "build_exe": build_exe_options
    },
    executables=executaveis
)

# python setup.py build
# python setup.py bdist_msi