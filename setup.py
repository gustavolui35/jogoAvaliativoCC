# pip install cx_freeze
import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(
                   script="main.py", 
                   icon="assets/icone.ico",
                    target_name="IronManMarcao.exe"
                   ) ]
cx_Freeze.setup(
    name = "Taxi GTA",
    options={
        "build_exe":{
            "packages":["pygame"],
            "include_files":["bases","recursos"]
        }
    }, executables = executaveis
)

# python setup.py build
# python setup.py bdist_msi