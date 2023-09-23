# Xcode Build Settings Extractor

A CLI tool to extract information about the Xcode build settings from a local Xcode installation.
This tool can extract the Xcode build settings and exort them as a JSON file or as a Swift file that can be used with [tuist](https://tuist.io).

## Requirements

This CLI requires Python 3.10.

## Setup

First you should set up a virtual environment with `python3 -m venv ./venv` and activate it with `source venv/bin/activate`.
Then install all required dependencies `pip3 install -r requirements.txt`.

## Usage

To extract the settings, you need to pass the path to a local Xcode installation. 
In order to export the settings to a JSON file, just pass an output path via the option `--out-json or -j`:
`python3 -m extractor extract -j 'output.json' /Applications/Xcode.app`

To export them to a Swift file for Tuist, pass an output path with the option `--out-swift or -s`:
`python3 -m extractor extract -s 'output.swift' /Applications/Xcode.app`