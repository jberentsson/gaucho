from enum import Enum
from time import sleep

import launchpad_py as launchpad
from pycaw.pycaw import AudioUtilities
from pycaw.utils import AudioSession


class ModeType(Enum):
    PRO = "Pro"
    PROMK3 = "ProMk3"
    MK1 = "MK1"
    MK2 = "MK2"
    XL = "XL"
    LKM = "LKM"
    DCR = "DCR"
    F64 = "F64"
    F3D = "F3D"


def detect_controller():
    """
    Detect what type of controller we have.
    """
    if launchpad.LaunchpadPro().Check(0):
        lp = launchpad.LaunchpadPro()
        if lp.Open(0):
            print("Launchpad Pro")
            return lp

    elif launchpad.LaunchpadProMk3().Check(0):
        lp = launchpad.LaunchpadProMk3()
        if lp.Open(0):
            print("Launchpad Pro Mk3")
            return lp

    elif launchpad.LaunchpadMiniMk3().Check(1):
        lp = launchpad.LaunchpadMiniMk3()
        if lp.Open(1):
            print("Launchpad Mini Mk3")
            return lp

    elif launchpad.LaunchpadLPX().Check(1):
        lp = launchpad.LaunchpadLPX()
        if lp.Open(1):
            print("Launchpad X")
            return lp

    elif launchpad.LaunchpadMk2().Check(0):
        lp = launchpad.LaunchpadMk2()
        if lp.Open(0):
            print("Launchpad Mk2")
            return lp

    print("Did not find any Launchpads, meh...")
    return None


def list_programs():
    """
    List programs in the audio mixer.
    """
    return AudioUtilities.GetAllSessions()


def note2xy(note: int):
    """
    Convert a note value into a (x, y) value
    """
    print(note)
    x = int(str(note)[1]) - 1
    y = 8 - int(str(note)[0])
    return (x, y)


def set_volume(ac: AudioSession, value: int):
    """
    Set program volume by ID.
    """
    try:
        decibels = float(((10 - value) * 10) / 100)
        volume = min(1.0, max(0.0, decibels))
        ac.SimpleAudioVolume.SetMasterVolume(volume, None)
    except:
        print(f"set_volume error! id: {id}, value: {value}")
        pass


def get_volume(ac: AudioSession, id: int):
    """
    Get program volume by ID.
    """
    try:
        volume = ac.SimpleAudioVolume.GetMasterVolume()
        if volume:
            return int(volume * 10)

        return None
    except:
        print(f"set_volume error! id: {id}")
        return None
