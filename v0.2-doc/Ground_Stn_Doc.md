# Dream2space Cubesat Ground Station
<!-- markdownlint-disable MD033 -->

[comment]: <> (TODO: Break down into smaller steps per header)

The Dream2space GUI Ground Station allows you to interact with your Dream2space Cubesat.

<img src="../images/gui-front.png" alt="Ground Station Start Page" width="50%"/>

<!-- markdownlint-disable MD025 MD003 -->
Contents
========
<!-- markdownlint-enable MD025 MD003 -->

- [Prerequisites (For Windows)](#prerequisites-for-windows)
  - [Step 1: Visit the Cygwin website](#step-1-visit-the-cygwin-website)
  - [Step 2: Download Cygwin installer](#step-2-download-cygwin-installer)
  - [Step 3: Install Cygwin](#step-3-install-cygwin)
- [Getting Started](#getting-started)
  - [Step 1: Download the Ground Station app](#step-1-download-the-ground-station-app)
  - [Step 2: Setup the Ground Station transceivers](#step-2-setup-the-ground-station-transceivers)
  - [Step 3: Connect the TTnC transceiver to the Computer](#step-3-connect-the-ttnc-transceiver-to-the-computer)
  - [Step 4: Connect the Payload transceiver to the Computer](#step-4-connect-the-payload-transceiver-to-the-computer)
  - [Step 5: Open up the Ground Station app](#step-5-open-up-the-ground-station-app)
- [Configuring the Ground Station app](#configuring-the-ground-station-app)
  - [Step 1: Select the TTnC COM port](#step-1-select-the-ttnc-com-port)
  - [Step 2: Select the Payload COM port](#step-2-select-the-payload-com-port)
  - [Step 3: Confirm and Start running app](#step-3-confirm-and-start-running-app)
- [Ground Station Beacon Panel](#ground-station-beacon-panel)
- [Ground Station Housekeeping Data Panel](#ground-station-housekeeping-data-panel)
- [Ground Station Mission Panel](#ground-station-mission-panel)

## Prerequisites (For Windows)

This step is needed if you are using a computer that runs on a **Windows** operating system.

The Ground Station app requires an additional software **Cygwin** to run.

### Step 1: Visit the Cygwin website

To download Cygwin, click the link [here](https://www.cygwin.com/).

Link to download Cygwin: <https://www.cygwin.com/>

The Cygwin page should look like this:

### Step 2: Download Cygwin installer

Click on the link `setup-x86_64.exe` to download the Cygwin installer, as shown in the **<span style="color: lime">green</span>** box in the screenshot above.

### Step 3: Install Cygwin

Proceed to install Cygwin using the installer.

When prompted to choose Installation Directory, ensure that the Root Directory is `C:\cygwin64`.

The step and the correct Root Directory is shown in the **<span style="color: lime">green</span>** box in the screenshot below.

<img src="images/cygwin-save-location.png" alt="Cygwin Root Install Directory" width="55%"/>

## Getting Started

### Step 1: Download the Ground Station app

To begin, download the Ground Station app.

Download the latest version of the Ground Station app `Ground_Station.exe` from the `Releases` page [here](https://github.com/dream2space/dream2space-ground_station/releases/tag/v1.0).

Link to download Ground Station app: <https://github.com/dream2space/dream2space-ground_station/releases/tag/v1.0>

The `Releases` page should look like this:

![Ground Station exe releases](images/ground_stn_exe_releases.png)

You can find the latest version of the Ground Station app and the Version tag in the table below.

| Executable Name      | Version Number |
| -------------------- | -------------- |
| `Ground_Station.exe` | `v1.0`         |

Scroll down to view the download link of the `Ground_Station.exe` app.

![Download app](ground_stn_exe_releases-dow.png)

Click on the `Ground_Station.exe` under the `Assets` section to download it.

### Step 2: Setup the Ground Station transceivers

The Ground Station has two 433 MHz transceivers to communicate with the TT&C and the Payload of the Dream2space cubesat respectively.

This is how a transceiver looks like:

<img src="images/transceiver-front-back.png" alt="Transceiver" width="50%"/>

The transceiver uses the Universal asynchronous receiver-transmitter (UART) protocol to send data to and from the computer and a USB-UART bridge to connect the transceiver to the computer's USB ports.

This is how a USB-UART bridge looks like:

<img src="images/usb-uart-bridge.png" alt="USB-UART bridge" width="50%"/>

An example of the transceiver connected to the USB-UART bridge that you have received is shown below:

<img src="images/transceiver-bridge-connected.jpg" alt="USB-UART bridge connected to transceiver" width="40%"/>

Double check that the pin connections are done as shown in the table below:

| USB-UART bridge | Transceiver |
| --------------- | ----------- |
| `5V`            | `Vcc`       |
| `GND`           | `GND`       |
| `TX`            | `RX`        |
| `RX`            | `TX`        |

### Step 3: Connect the TTnC transceiver to the Computer

| ⚠️ | **The sequence of plugging in the USB-UART bridges is important. Do try to follow the sequence.** |
| - | ------------------------------------------------------------------------------------------------ |

The computer identifies the USB-UART bridges as virtual `COM` ports and each bridge is assigned a unique `COM` port number upon plugging in the USB.

The Ground Station app needs to know `COM` port number for the TT&C and Payload transceiver to read and write to the respective transceivers.

The TT&C transceiver comes with a label on the transceiver, as shown in the image below.

<img src="images/ttnc-transceiver-bridge.jpg" alt="USB-UART bridge connected to TT&C transceiver" width="80%"/>

Plug in the TT&C transceiver's USB-UART bridge into the computer. The computer should detect the USB `COM` port and the `COM` port can be found using the Device Manager.

Note down the `COM` port for the TT&C transceiver's USB-UART bridge.

### Step 4: Connect the Payload transceiver to the Computer

| ⚠️ | **The sequence of plugging in the USB-UART bridges is important. Do try to follow the sequence.** |
| - | ------------------------------------------------------------------------------------------------ |

The payload transceiver comes with a label on the transceiver, as shown in the image below.

<img src="images/payload-transceiver-bridge.jpg" alt="USB-UART bridge connected to payload transceiver" width="80%"/>

Plug in the Payload transceiver's USB-UART bridge into the computer. The computer should detect the USB `COM` port and the `COM` port can be found using the Device Manager.

Note down the `COM` port for the Payload transceiver's USB-UART bridge.

### Step 5: Open up the Ground Station app

| ⚠️ | **This is the recommended way to open up the GUI exe. Other methods may cause errors.** |
| - | --------------------------------------------------------------------------------------- |

Navigate to the folder containing the downloaded GUI exe, as shown in the folder below.

<img src="images/downloads-folder.png" alt="Downloads folder with GUI exe"/>

Double click on the icon to launch the app. The icon is boxed in **<span style="color: lime">green</span>** in the the screenshot below.

If the app has launched successfully, the Start Page, as shown in screenshot below, will appear.

<img src="images/app-start-page.png" alt="App Start Page" width="50%"/>

A `dream2space` folder will also be created in the same folder to store data collected from the app.

The folder is boxed in **<span style="color: lime">green</span>** in the the screenshot below.

<img src="images/downloads-folder-after-open.png" alt="App Start Page" />

| ⚠️ | **Do not delete that folder while the app is running!** |
| - | ------------------------------------------------------ |

## Configuring the Ground Station app

| 💡 | TIP! |
| -- | ---- |

<img src="images/app-start-refresh.png" alt="Serial port refresh" width="50%"/>

If you cannot spot the COM ports noted down previously, try clicking on the **🔄 Refresh** button.

The **🔄 Refresh** button is boxed in **<span style="color: lime">green</span>** in the screenshot above.

### Step 1: Select the TTnC COM port

To view the list of COM ports available for selection as the TT&C transceiver's port, click on the dropdown menu.

The dropdown menu is boxed in **<span style="color: lime">green</span>** in the screenshot below.

<img src="images/app-start-select-ttnc-port.png" alt="Show ttnc serial port" width="50%"/>

The list of discovered COM ports will be displayed.

<img src="images/app-start-find-ttnc-port.png" alt="Select ttnc serial port" width="50%"/>

Select the COM port that you have noted down after plugging in the TT&C transceiver's USB-UART bridge.

### Step 2: Select the Payload COM port

To view the list of COM ports available for selection as the Payload transceiver's port, click on the dropdown menu.

The dropdown menu is boxed in **<span style="color: lime">green</span>** in the screenshot below.

<img src="images/app-start-select-payload-port.png" alt="Show payload serial port" width="50%"/>

The list of discovered COM ports will be displayed.

<img src="images/app-start-find-payload-port.png" alt="Select payload serial port" width="50%"/>

Select the COM port that you have noted down after plugging in the Payload transceiver's USB-UART bridge.

### Step 3: Confirm and Start running app

After selecting COM ports for the TT&C and Payload transceivers, click on the Start button to proceed.

The Start button is boxed in **<span style="color: lime">green</span>** in the screenshot below.

<img src="images/app-start-confirm-port.png" alt="Confirm ports selected" width="50%"/>

After which, the app will display the Ground Station main page as shown below.

<img src="images/app-start-start-success.png" alt="Ports selection success" width="90%"/>

## Ground Station Beacon Panel

<img src="images/app-beacon-refresh.png" alt="Refresh ports" width="90%"/>

## Ground Station Housekeeping Data Panel

<img src="images/app-hk-button.png" alt="Housekeeping request button" width="90%"/>

<img src="images/app-hk-start.png" alt="Send housekeeping command" width="90%"/>

<img src="images/app-hk-success.png" alt="Housekeeping command success" width="90%"/>

<img src="images/app-hk-success-log-location.png" alt="Housekeeping logs location"/>

<img src="images/app-hk-logs.png" alt="Housekeeping logs csv" width="60%"/>

## Ground Station Mission Panel

<img src="images/app-mission-button.png" alt="Mission command button" width="90%"/>

<img src="images/app-mission-window.png" alt="Mission command window" width="90%"/>

<img src="images/app-mission-window-submit.png" alt="Mission command submit button" width="90%"/>

<img src="images/app-mission-sending-cmd.png" alt="Mission command sending" width="90%"/>

<img src="images/app-mission-downlink-standby.png" alt="Downlink standby" width="90%"/>

<img src="images/app-mission-view-completed.png" alt="Mission view completed button" width="90%"/>

<img src="images/app-mission-view-overall-status.png" alt="View overall status of missions" width="90%"/>

<img src="images/app-mission-view-location.png" alt="Mission saved location" width="90%"/>

<img src="images/app-mission-view-mission-folder.png" alt="View mission folder" width="90%"/>

<img src="images/app-mission-view-mission-status.png" alt="View mission status" width="90%"/>

<img src="images/app-mission-view-overall-status-fail.png" alt="View overall status of missions with fail" width="90%"/>

<img src="images/app-mission-view-mission-status-fail.png" alt="View mission status with fail" width="90%"/>
