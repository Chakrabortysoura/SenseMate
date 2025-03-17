from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
app=FastAPI()

def execute_shell_command(shell_script_name: str):
    cmd="./"+shell_script_name
    os.system(cmd)
@app.post("/build")
def build():
    execute_shell_command("build_apk.sh") #Execute the build script
    path="Android_application/bin/"
    path+=os.listdir(path)[0]
    return FileResponse(path)

@app.get("/download/apk")
async def download_apk():
    path="Android_application/bin/"
    path+=os.listdir(path)[0]
    return FileResponse(path)