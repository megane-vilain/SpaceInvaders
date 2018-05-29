from cx_Freeze import setup, Executable
exe = Executable(
script="main.py",
)

setup(
    executables = [exe],
    version="1.0.0"
    )
