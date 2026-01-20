#
# MuMuConnect.py
#
# 用于连接和断开MuMu模拟器的ADB连接
#
import subprocess
import sys

# 连接MuMu模拟器的函数
def connect_to_mumu(ip="127.0.0.1", port="5555"):
    print("="*50)
    print("正在尝试连接MuMu模拟器...")
    try:
        connect_result = subprocess.run(
            ["adb", "connect", f"{ip}:{port}"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=20
        )
        output = (connect_result.stdout or "") + (connect_result.stderr or "")
        if connect_result.returncode != 0 or "cannot" in output.lower():
            str = color_text("无法连接到MuMu模拟器，请检查IP和端口是否正确，或者MuMu模拟器是否正在运行。", "red")
            print(str)
            print(output)
        else:
            str = color_text(f"成功连接到MuMu模拟器：{ip}:{port}！", "green")
            print(str)
            print(output)
    except subprocess.TimeoutExpired:
        str = color_text("连接MuMu模拟器超时，请确保MuMu模拟器已启动并运行。", "red")
        print(str)
    except Exception as e:
        str = color_text(f"连接MuMu模拟器失败，错误信息如下：{str(e)}", "red")
        print(str)

# 检查MuMu连接状态的函数
def check_mumu_connection()-> str:
    print("="*50)
    print("正在检查MuMu模拟器连接状态...")
    try:
        devices_result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=20
        )
        output = (devices_result.stdout or "") + (devices_result.stderr or "")
        if devices_result.returncode != 0:
            str = color_text("无法检查设备连接状态，请确保ADB已正确安装并配置。", "red")
            print(str)
            print(output)
            return ""
        else:
            str = color_text("设备连接状态如下：", "green")
            print(str)
            print(color_text(devices_result.stdout, "green"))
            return devices_result.stdout
    except subprocess.TimeoutExpired:
        str = color_text("检查设备连接状态超时，请重试。", "red")
        print(str)
        return ""
    except Exception as e:
        str = color_text(f"检查设备连接状态失败，错误信息如下：{str(e)}", "red")
        print(str)
        return ""

# 断开MuMu模拟器连接的函数
def disconnect_mumu(device):
    print("="*50)
    print("正在断开MuMu模拟器连接...")
    try:
        disconnect_result = subprocess.run(
            ["adb", "disconnect", device],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=20
        )
        output = (disconnect_result.stdout or "") + (disconnect_result.stderr or "")
        if disconnect_result.returncode != 0:
            str = color_text("断开连接失败，请检查设备名称是否正确。", "red")
            print(str)
            print(output)
            return
        else:
            device_result = check_mumu_connection()
            if device not in device_result:
                str = color_text(f"设备{device}已成功断开连接。", "green")
                print(str)
    except subprocess.TimeoutExpired:
        str = color_text("断开连接超时，请重试。", "red")
        print(str)
    except Exception as e:
        str = color_text(f"断开连接失败，错误信息如下：{str(e)}", "red")
        print(str)

# 彩色文本输出函数，支持红色和绿色
def color_text(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m'
    }
    return f"{colors.get(color, '')}{text}\033[0m"

# 提供用户交互的连接服务函数
def connect_server():
    ip = input("请输入MuMu模拟器的IP地址（默认为127.0.0.1）：").strip()
    port = input("请输入MuMu模拟器的端口号（默认为5555）：").strip()
    if not ip: ip = "127.0.0.1"
    if not port: port = "5555"
    connect_to_mumu(ip, port)

# 提供用户交互的检查连接状态服务函数
def check_server():
    check_mumu_connection()

# 提供用户交互的断开连接服务函数
def disconnect_server():
    device = input("请输入要断开连接的MuMu模拟器设备名称（例如127.0.0.1:5555）：").strip()
    if device == "":
        str = color_text("未输入设备名称，是否断开所有连接？(y/n)：", "red")
        choice = input(str).strip().lower()
        if choice == 'y':
            disconnect_mumu(device)
        else:
            print(f"{color_text('操作已取消。', 'red')}")
            return

# 环境初始化函数，提供菜单供用户选择操作
def environment_init():
    print("正在初始化MuMu模拟器ADB连接管理工具环境...")
    while True:
        print("="*50)
        print("MuMu模拟器ADB连接管理工具")
        print("1. 连接MuMu模拟器")
        print("2. 检查MuMu模拟器连接状态")
        print("3. 断开MuMu模拟器连接")
        print("4. 环境配置完成，进入下一阶段")
        print("5. 退出")
        choice = input("请选择操作（1-5）：").strip()
        match choice:
            case '1':
                connect_server()
            case '2':
                check_server()
            case '3':
                disconnect_server()
            case '4':
                print(f"{color_text('环境配置完成，进入下一阶段。', 'green')}")
                break
            case '5':
                print(f"{color_text('退出MuMu模拟器连接管理工具。', 'green')}")
                break
            case _:
                print(f"{color_text('无效选择，请输入1到5之间的数字。', 'red')}")

if __name__ == "__main__":
    environment_init()
