# GUI Ground Station

The [command line ground station](https://github.com/huiminlim/ground_stn) was built previously, so it's time for the GUI ground station to be built.

## Getting Started

To begin, download the Ground Station Desktop app.

| Column 1 Header | Column 2 Header | Column 3 Header |
| --------------- | --------------- | --------------- |
| Row 1 Column 1 | Row 1 Column 2 | Row 1 Column 3 |
| Row 2 Column 1 | Row 2 Column 2 | Row 2 Column 3 |
| Row 3 Column 1 | Row 3 Column 2 | Row 3 Column 3 |

Download the latest version of the Ground Station Desktop app `Ground_Stn.exe` from the `Releases` page [here](https://github.com/huiminlim/ground_stn-gui/releases).

Navigate to the section as shown in the screenshot below to find the latest version of the Ground Station Desktop app.

| |
|-|
![Ground Station exe releases](images/ground_stn_exe_releases.png)
| |

You can find the latest version of the Ground Station Desktop app and the Version tag in the table below.

| Executable Name  | Version Number |
|------------------|----------------|
| `Ground_Stn.exe` | `v-beacon-hk`  |

Click on the `Ground_Stn.exe` under the `Assets` section to download it.

After downloading the Desktop app, start the Ground Station Desktop app.

A security warning may pop up in some cases. In such cases, click on `More Info` as shown in the screenshot below.

![Security Warning 1](images/security_warning1.png)

After that, click on `Run anyway`.

![Security Warning 2](images/security_warning2.png)

To check if the Ground Station is downloaded correctly, the Ground Station Desktop app will appear, like in the screenshot below.

![Desktop App](images/app_start.png)

## Features

The Ground Station app has several functions to interact with the CubeSat.

### Port Setup

This.

| ⚠️ | **Ensure that your Ground Station app is closed before continuing with this section.** |
| --- | -------------------------------------------------------------------------------------- |

To setup the Ground Station, connect the 2 transceivers to talk to the TT&C and Payload to your laptop.

The transceivers need a intermediary bridge to connect its pins to the USB ports of laptops and an USB adapter is used.

This is how the TT&C transceiver connected to the USB adapter.

![TT&C Ground Station](images/ttnc_ground_station.jpg)

Similarly, this is how the Payload transceiver is connected to the USB adapter.

![Payload Ground Station](images/payload_ground_station.jpg)

The first page of the Ground Station app shows the serial port selection.

![Ground Station Ports Selection](images/ground_station_page1.PNG)

#### For Windows

This.

| 💡 | **Plug the transceivers into your laptop sequentially for this step** |
| --- | -------------------------------------------------------------------- |

Plug in the USB adapter for the TT&C transceiver to the laptop.

#### For Mac

### Beacons

### Housekeeping Data Telecommands

### Mission and Downlink Telecommands

## Requirements Gathering

## UI/UX Design and Mockup

The beacons screen were added first.

![Beacons](images/beacons.png)

This is how the initial beacon tickers work.

![Beacon GUI](images/beacon.gif)

## Software Architecture

## Info

How to run a long running process alongside Tkinter GUI: [here](https://zetcode.com/articles/tkinterlongruntask/)
