from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
import serial.tools.list_ports 
import time
import threading 
import serial
import time

import serial
import time

# Initialize serial connection to Arduino
arduino = serial.Serial('COM7', 9600, timeout=1)  # Replace 'COM3' with the correct port for your system
time.sleep(2)  # Give time for connection to establish


def start_heart_rate_reading():
    # Send command to Arduino to start readings
    arduino.write(b'Take readings\n')
    
    # List to hold the heart rate readings
    heart_rate_readings = []
    
    while len(heart_rate_readings) < 3:
        # Read line from serial
        line = arduino.readline().decode('utf-8').strip()
        
        if line.isdigit():  # Check if the reading is a number (heart rate)
            heart_rate = int(line)
            print(f"Heart Rate Reading {len(heart_rate_readings) + 1}: {heart_rate} BPM")
            heart_rate_readings.append(heart_rate)
            
            # Optional delay if needed to allow time between readings
            time.sleep(1)
        else:
            print(line)  # Print any other messages from Arduino, e.g., "Waiting..."
    
    # Calculate and return the average heart rate after three readings
    average_heart_rate = sum(heart_rate_readings) / len(heart_rate_readings)
    print(f"Average Heart Rate: {average_heart_rate:.2f} BPM")
    return average_heart_rate


try:
    start_heart_rate_reading()
except KeyboardInterrupt:
    print("Stopping heart rate reading.")
finally:
    arduino.close()  # Close the serial connection when done
