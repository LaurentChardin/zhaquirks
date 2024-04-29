"""Yokis MTR500E-UP."""

""" https://github.com/zigpy/zha-device-handlers/blob/dm/quirks-v2-documentation/quirks_v2.md """

from zigpy import types as t
from zigpy.quirks import CustomCluster
from zigpy.zcl import ClusterType
from zigpy.zcl.foundation import (
    BaseAttributeDefs,
    BaseCommandDefs,
    ZCLAttributeDef,
    ZCLCommandDef,
)
from zigpy.zcl.clusters.general import (
    Basic,
    GreenPowerProxy,
    Groups,
    Identify,
    OnOff,
    Ota,
    Scenes,
)
from zigpy.zcl.clusters.lightlink import LightLink

from zigpy.profiles import zgp, zha
from zigpy.quirks.v2 import add_to_registry_v2

Manufacturer_Name = "YOKIS"
Manufacturer_ID = 0x132d

class manuSpecificYokisDevice(CustomCluster):
    """Allows you to manage the parameters related to the device."""

    cluster_id = 0xfc01
    ep_attribute = 'yokis_device'

    class AttributeDefs(BaseAttributeDefs):
        configurationChanged = ZCLAttributeDef( 
            id=0x0005, 
            type=t.enum16, 
            is_manufacturer_specific=False, 
        ) 

class manuSpecificYokisInput(CustomCluster):
    """Cluster used to configure the different inputs options of a device (NO/NC, ContactMode …)."""

    cluster_id = 0xfc02
    ep_attribute = 'yokis_input'

    class AttributeDefs(BaseAttributeDefs):
        #Indicate how the input should be handle: 0 -> Unknown, 1 -> Push button, 2 -> Switch, 3 -> Relay, 4 -> FP_IN
        inputMode = ZCLAttributeDef( 
            id=0x0000, 
            type=t.enum8, 
            is_manufacturer_specific=True, 
        )
        #Indicate the contact nature of the entry: 0 -> NC, 1 -> NO
        contactMode = ZCLAttributeDef( 
            id=0x0001, 
            type=t.Bool, 
            is_manufacturer_specific=True, 
        )
        #Indicate the last known state of the local BP (Bouton Poussoir, or Push Button)
        lastLocalCommandState = ZCLAttributeDef( 
            id=0x0002, 
            type=t.Bool, 
            is_manufacturer_specific=True, 
        )
        #Indicate the last known state of the Bp connect
        lastLocalCommandState = ZCLAttributeDef( 
            id=0x0003, 
            type=t.Bool, 
            is_manufacturer_specific=True, 
        )
        #Indicate the last known state of the Bp connect
        backlightIntensity = ZCLAttributeDef( 
            id=0x0004, 
            type=t.uint8_t, 
            is_manufacturer_specific=True, 
        )

class manuSpecificYokisEntryConfigurator(CustomCluster):
    """Cluster used to configure press duration, time between press,..."""

    cluster_id = 0xfc03
    ep_attribute = 'yokis_entryconfigurator'

    class AttributeDefs(BaseAttributeDefs):
        #Use to enable short press action
        eShortPress = ZCLAttributeDef( 
            id=0x0001, 
            type=t.Bool, 
            is_manufacturer_specific=True, 
        )
        #Use to enable long press action
        eLongPress = ZCLAttributeDef( 
            id=0x0002, 
            type=t.Bool, 
            is_manufacturer_specific=True, 
        )
        #Define long Press duration in milliseconds. Default: 0x0BB8, Min-Max: 0x00 - 0x1388
        longPressDuration = ZCLAttributeDef( 
            id=0x0003, 
            type=t.uint16_t, 
            is_manufacturer_specific=True, 
        )
        #Define the maximum time between 2 press to keep in a sequence (In milliseconds). Default: 0x01F4, Min-Max: 0x0064 - 0x0258
        timeBetweenPress = ZCLAttributeDef( 
            id=0x0004, 
            type=t.uint16_t, 
            is_manufacturer_specific=True, 
        )
        #Enable R12M Long Press action
        eR12MLongPress = ZCLAttributeDef( 
            id=0x0005, 
            type=t.Bool, 
            is_manufacturer_specific=True, 
        )
        #Disable local configuration
        eLocalConfigLock = ZCLAttributeDef( 
            id=0x0006, 
            type=t.Bool, 
            is_manufacturer_specific=True, 
        )

class manuSpecificYokisSubSystem(CustomCluster):
    """Define specific behavior of device sub system."""

    cluster_id = 0xfc04
    ep_attribute = 'yokis_subsystem'

    class AttributeDefs(BaseAttributeDefs):
        #Define the device behavior after power failure : 0 -> LAST STATE, 1 -> OFF, 2 -> ON, 3-> BLINK
        powerFailureMode = ZCLAttributeDef( 
            id=0x0001, 
            type=t.enum8, 
            is_manufacturer_specific=True, 
        )

class manuSpecificYokisLoadManager(CustomCluster):
    """Cluster used to define values of LoadManager on the device."""

    cluster_id = 0xfc05
    ep_attribute = 'yokis_loadmanager'

class manuSpecificYokisLightControl(CustomCluster):
    """Cluster used to create for complex On/Off commands. It expend the classic cluster On/Off (ID : 0x0006)."""

    cluster_id = 0xfc06
    ep_attribute = 'yokis_lightcontrol'

    class AttributeDefs(BaseAttributeDefs):
        #Use to know which state is the relay
        onOff = ZCLAttributeDef( 
            id=0x0000, 
            type=t.Bool, 
            is_manufacturer_specific=True, 
        )
        #Indicate the previous state before action
        prevState = ZCLAttributeDef( 
            id=0x0001, 
            type=t.Bool, 
            is_manufacturer_specific=True, 
        )
        #Define the ON embedded timer duration in seconds.  Default: 0x00, Min-Max: 0x00 – 0x00409980
        onTimer = ZCLAttributeDef( 
            id=0x0002, 
            type=t.uint32_t, 
            is_manufacturer_specific=True, 
        )
        #Enable (0x01) / Disable (0x00) use of onTimer.
        eOnTimer = ZCLAttributeDef( 
            id=0x0003, 
            type=t.Bool, 
            is_manufacturer_specific=True, 
        )
        #Define the PRE-ON embedded delay in seconds.  Default: 0x00, Min-Max: 0x00 – 0x00409980
        preOnDelay = ZCLAttributeDef( 
            id=0x0004, 
            type=t.uint32_t, 
            is_manufacturer_specific=True, 
        )
        #Enable (0x01) / Disable (0x00) use of PreOnTimer.
        ePreOnDelay = ZCLAttributeDef( 
            id=0x0005, 
            type=t.Bool, 
            is_manufacturer_specific=True, 
        )
        #Define the PRE-OFF embedded delay in seconds.  Default: 0x00, Min-Max: 0x00 – 0x00409980
        preOffDelay = ZCLAttributeDef( 
            id=0x0008, 
            type=t.uint32_t, 
            is_manufacturer_specific=True, 
        )
        #Enable (0x01) / Disable (0x00) PreOff delay.
        ePreOffDelay = ZCLAttributeDef( 
            id=0x0009, 
            type=t.Bool, 
            is_manufacturer_specific=True, 
        )
        #Set the value of ON pulse length. Default: 0x01F4, Min-Max: 0x0014 – 0xFFFE
        pulseDuration = ZCLAttributeDef( 
            id=0x000A, 
            type=t.uint16_t, 
            is_manufacturer_specific=True, 
        )
        #Indicates the current Type of time selected that will be used during push button configuration: 0x00 -> Seconds, 0x01 -> Minutes
        timeType = ZCLAttributeDef( 
            id=0x000B, 
            type=t.enum8, 
            is_manufacturer_specific=True, 
        )
        #Set the value of the LONG ON embedded timer in seconds.  Default: 0x5460 (1h), Min-Max: 0x00 – 0x00409980
        longOnDuration = ZCLAttributeDef( 
            id=0x000C, 
            type=t.uint32_t, 
            is_manufacturer_specific=True, 
        )
        #Indicates the operating mode: 0x00 -> Timer, 0x01 -> Staircase, 0x02 -> Pulse
        operatingMode = ZCLAttributeDef( 
            id=0x000D, 
            type=t.enum8, 
            is_manufacturer_specific=True, 
        )
        #Time before goes off after the stop announce blinking. (In seconds).  Default: 0x0000, Min-Max: 0x00 – 0x00409980
        stopAnnounceTime = ZCLAttributeDef( 
            id=0x0013, 
            type=t.uint32_t, 
            is_manufacturer_specific=True, 
        )
        #Enable (0x01) / Disable (0x00) the announcement before turning OFF.
        eStopAnnounce = ZCLAttributeDef( 
            id=0x0014, 
            type=t.Bool, 
            is_manufacturer_specific=True, 
        )
        #Enable (0x01) / Disable (0x00) Deaf Actions.
        eDeaf = ZCLAttributeDef( 
            id=0x0015, 
            type=t.Bool, 
            is_manufacturer_specific=True, 
        )
        #Enable (0x01) / Disable (0x00) Blink Actions.
        eBlink = ZCLAttributeDef( 
            id=0x0016, 
            type=t.Bool, 
            is_manufacturer_specific=True, 
        )
        #Number of blinks done when receiving the corresponding order. One blink is considered as one ON step followed by one OFF step. Default: 0x03, Min-Max: 0x00 – 0x14
        blinkAmount = ZCLAttributeDef( 
            id=0x0017, 
            type=t.uint8_t, 
            is_manufacturer_specific=True, 
        )
        #Duration for the ON time on a blink period (In millisecond).  Default: 0x000001F4, Min-Max: 0x00 – 0x00409980
        blinkOnTime = ZCLAttributeDef( 
            id=0x0018, 
            type=t.uint32_t, 
            is_manufacturer_specific=True, 
        )
        #Duration for the OFF time on a blink period (In millisecond).  Default: 0x000001F4, Min-Max: 0x00 – 0x00409980
        blinkOffTime = ZCLAttributeDef( 
            id=0x0019, 
            type=t.uint32_t, 
            is_manufacturer_specific=True, 
        )
        #Define number of blink to do when receiving the DEAF action. One blink is considered as one ON step followed by one OFF step. Default: 0x03, Min-Max: 0x00 – 0x14
        deafBlinkAmount = ZCLAttributeDef( 
            id=0x001A, 
            type=t.uint8_t, 
            is_manufacturer_specific=True, 
        )
        #Define duration of a blink ON (In millisecond). Default: 0x0320, Min-Max: 0x0064– 0x4E20
        deafBlinkTime = ZCLAttributeDef( 
            id=0x001B, 
            type=t.uint16_t, 
            is_manufacturer_specific=True, 
        )
        #Indicate which state must be apply after a blink sequence: 0x00 -> State before blinking, 0x01 -> OFF, 0x02 -> ON
        stateAfterBlink = ZCLAttributeDef( 
            id=0x001C, 
            type=t.enum8, 
            is_manufacturer_specific=True, 
        )
        #Indicate which state must be apply after a blink sequence: 0x00 -> State before blinking, 0x01 -> OFF, 0x02 -> ON
        eNcCommand = ZCLAttributeDef( 
            id=0x001D, 
            type=t.Bool, 
            is_manufacturer_specific=True, 
        )

class manuSpecificYokisDimmer(CustomCluster):
    """TBD."""

    cluster_id = 0xfc07
    ep_attribute = 'yokis_dimmer'

class manuSpecificYokisWindowCovering(CustomCluster):
    """TBD."""

    cluster_id = 0xfc08
    ep_attribute = 'yokis_windowcovering'

class manuSpecificYokisChannel(CustomCluster):
    """TBD."""

    cluster_id = 0xfc09
    ep_attribute = 'yokis_channel'

class manuSpecificYokisPilotWire(CustomCluster):
    """TBD."""

    cluster_id = 0xfc0A
    ep_attribute = 'yokis_pilotwire'

class manuSpecificYokisStats(CustomCluster):
    """TBD."""

    cluster_id = 0xfcf0
    ep_attribute = 'yokis_stats'

(
    add_to_registry_v2(Manufacturer_Name, "MTR500E-UP")
    .also_applies_to(Manufacturer_Name, "MTR1300E-UP")
    .also_applies_to(Manufacturer_Name, "MTR2000E-UP")
    .adds(manuSpecificYokisDevice)
    .adds(manuSpecificYokisDevice, cluster_type=ClusterType.Client)
    .adds(manuSpecificYokisInput)
    .adds(manuSpecificYokisEntryConfigurator)
    .adds(manuSpecificYokisSubSystem)
    .adds(manuSpecificYokisLightControl)
    .adds(manuSpecificYokisLightControl, cluster_type=ClusterType.Client)
    .removes(GreenPowerProxy.cluster_id, endpoint_id = 242)
    .removes(GreenPowerProxy.cluster_id, cluster_type=ClusterType.Client, endpoint_id = 242)
)
