# Developers' Guide

## Software Architecture

## Production in Windows OS

To create EXE for production in Windows, type the following command into Windows Powershell:

```bash
pyinstaller Ground_Station.spec
```

The backup command is:

```bash
pyinstaller --onefile -w -i "assets/satellite.ico" Ground_Station.py
```

## Downlink Notes

This note is for downlink mission implementation.

## Useful Guides

How to run a long running process alongside Tkinter GUI: [here](https://zetcode.com/articles/tkinterlongruntask/)
