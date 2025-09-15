#!/usr/bin/env python3
from flask import Flask, render_template, jsonify
import psutil
import subprocess
import os

app = Flask(__name__)

def get_system_info():
    # Температура CPU
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = int(f.read().strip()) / 1000
    except:
        temp = 0
    
    # Состояние вентилятора
    try:
        with open('/sys/class/thermal/cooling_device0/cur_state', 'r') as f:
            fan_state = int(f.read().strip())
    except:
        fan_state = 0
    
    # CPU и память
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Uptime
    try:
        uptime_sec = float(open('/proc/uptime').read().split()[0])
        uptime_hours = uptime_sec / 3600
    except:
        uptime_hours = 0
    
    return {
        'temperature': round(temp, 1),
        'fan_state': fan_state,
        'cpu_percent': round(cpu_percent, 1),
        'memory_percent': round(memory.percent, 1),
        'memory_used_gb': round(memory.used / (1024**3), 2),
        'memory_total_gb': round(memory.total / (1024**3), 2),
        'disk_percent': round(disk.percent, 1),
        'disk_used_gb': round(disk.used / (1024**3), 2),
        'disk_total_gb': round(disk.total / (1024**3), 2),
        'uptime_hours': round(uptime_hours, 1)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def api_stats():
    return jsonify(get_system_info())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
