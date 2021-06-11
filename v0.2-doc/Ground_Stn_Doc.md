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

## Prerequisites (For Windows)

This step is needed if you are using a computer that runs on a **Windows** operating system.

The Ground Station app requires an additional software **Cygwin** to run.

<div class= "container" markdown="1">

### Step 1: Visit the Cygwin website

To download Cygwin, click the link [here](https://www.cygwin.com/).

Link to download Cygwin: <https://www.cygwin.com/>

The Cygwin page should look like this:

<img src="images/cygwin-download.png" alt="Cygwin Download Page"/>

</div>

### Step 2: Download Cygwin installer

Click on the link `setup-x86_64.exe` to download the Cygwin installer, as shown in the **<span style="color: lime">green</span>** box in the screenshot above.

<div class= "container" markdown="1">

### Step 3: Install Cygwin

Proceed to install Cygwin using the installer.

When prompted to choose Installation Directory, ensure that the Root Directory is `C:\cygwin64`.

The step and the correct Root Directory is shown in the **<span style="color: lime">green</span>** box in the screenshot below.

<img src="images/cygwin-save-location.png" alt="Cygwin Root Install Directory" width="55%"/>

</div>

## Getting Started

### Step 1: Download the Ground Station app

To begin, download the Ground Station app.

Download the latest version of the Ground Station app `Ground_Stn.exe` from the `Releases` page [here](https://github.com/dream2space/dream2space-ground_station/releases).

[comment]: <> (TODO: Update to a direct link to the exact releases)

Link to download Ground Station app: <https://github.com/dream2space/dream2space-ground_station/releases/>

[comment]: <> (TODO: Update to a direct link to the exact releases)

The `Releases` page should look like this:

![Ground Station exe releases](images/ground_stn_exe_releases.png)  <!--TODO: Fix to correct image and rename to replace-->

You can find the latest version of the Ground Station app and the Version tag in the table below.

| Executable Name      | Version Number |
| -------------------- | -------------- |
| `Ground_Station.exe` | `v-hk-logs`    |

[comment]: <> (TODO: Correct the version number to match the screenshot/latest version)

Click on the `Ground_Station.exe` under the `Assets` section to download it.

### Step 2: Setup the Ground Station transceivers

The Ground Station has 2 transceivers that work at 433 MHz to communicate with the TT&C and the Payload of the Dream2space cubesat respectively.
