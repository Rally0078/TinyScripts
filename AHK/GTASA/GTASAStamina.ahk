#Requires AutoHotkey v2.0
Up:: {
    while GetKeyState("Up", "P") {
        Send "{LShift down}"
        Sleep 1
          Send "{LShift up}"
          sleep 10
        Send "{LButton down}"
        Sleep 1
          Send "{LButton up}"
          sleep 10
    }
}
Send "{LShift up}"
Send "{LButton up}"
return