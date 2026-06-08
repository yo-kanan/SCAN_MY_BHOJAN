import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime
import random

class ScanMyBhojanDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("ScanMyBhojan - Sensor Dashboard")
        self.root.geometry("1600x900")
        self.root.configure(bg='#0a0e27')
        
        # Color scheme
        self.bg_dark = '#0a0e27'
        self.bg_card = '#151b3d'
        self.accent_cyan = '#00d4ff'
        self.accent_green = '#00ff88'
        self.accent_purple = '#a259ff'
        self.accent_orange = '#ff6b35'
        self.accent_yellow = '#ffd93d'
        self.text_white = '#ffffff'
        self.text_gray = '#8892b0'
        
        # Sensor data - more technical/hardware focused
        self.sensors = {
            'Weight Sensor': {'status': 'Active', 'value': 0, 'unit': 'g', 'color': self.accent_cyan},
            'IR Proximity': {'status': 'Active', 'value': 0, 'unit': 'cm', 'color': self.accent_green},
            'Color RGB': {'status': 'Active', 'value': [0, 0, 0], 'unit': '', 'color': self.accent_purple},
            'Temperature': {'status': 'Active', 'value': 0, 'unit': '°C', 'color': self.accent_orange},
            'Camera FPS': {'status': 'Active', 'value': 0, 'unit': 'fps', 'color': self.accent_yellow},
            'Light Intensity': {'status': 'Active', 'value': 0, 'unit': 'lux', 'color': '#ff1744'}
        }
        
        # System metrics
        self.system_metrics = {
            'CPU Usage': 0,
            'Memory': 0,
            'Scan Time': 0,
            'Data Points': 0
        }
        
        self.weight_history = []
        self.temp_history = []
        self.light_history = []
        self.scan_count = 0
        self.scanning = True
        
        self.setup_ui()
        self.animate_sensors()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.bg_dark, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # Logo and title
        logo_frame = tk.Frame(header_frame, bg=self.bg_dark)
        logo_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        logo = tk.Label(logo_frame, text="📷", font=("Helvetica", 40), 
                       bg=self.bg_dark, fg=self.accent_cyan)
        logo.pack(side=tk.LEFT, padx=(0, 15))
        
        title_container = tk.Frame(logo_frame, bg=self.bg_dark)
        title_container.pack(side=tk.LEFT, fill=tk.Y)
        
        title = tk.Label(title_container, text="ScanMyBhojan", 
                        font=("Helvetica", 36, "bold"),
                        fg=self.accent_cyan, bg=self.bg_dark, anchor='w')
        title.pack(anchor='w')
        
        subtitle = tk.Label(title_container, text="Hardware Sensor Monitor & Analysis", 
                           font=("Helvetica", 13),
                           fg=self.text_gray, bg=self.bg_dark, anchor='w')
        subtitle.pack(anchor='w')
        
        # System info in header
        info_frame = tk.Frame(header_frame, bg=self.bg_dark)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20)
        
        self.scan_count_label = tk.Label(info_frame, text="Scans: 0", 
                                         font=("Helvetica", 14, "bold"),
                                         fg=self.text_white, bg=self.bg_dark)
        self.scan_count_label.pack(anchor='e')
        
        self.status_label = tk.Label(info_frame, text="● SCANNING", 
                                     font=("Helvetica", 14, "bold"),
                                     fg=self.accent_green, bg=self.bg_dark)
        self.status_label.pack(anchor='e')
        
        # Main content grid
        content_frame = tk.Frame(main_frame, bg=self.bg_dark)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left section - Sensors (40%)
        left_frame = tk.Frame(content_frame, bg=self.bg_dark)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        
        self.create_sensor_grid(left_frame)
        
        # Right section - Charts and metrics (60%)
        right_frame = tk.Frame(content_frame, bg=self.bg_dark)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0))
        
        self.create_charts_section(right_frame)
        
    def create_sensor_grid(self, parent):
        # Title
        title_frame = tk.Frame(parent, bg=self.bg_dark)
        title_frame.pack(fill=tk.X, pady=(0, 12))
        
        title = tk.Label(title_frame, text="HARDWARE SENSORS", 
                        font=("Helvetica", 18, "bold"),
                        fg=self.text_white, bg=self.bg_dark, anchor='w')
        title.pack(side=tk.LEFT)
        
        # Sensor cards in 2x3 grid
        sensors_container = tk.Frame(parent, bg=self.bg_dark)
        sensors_container.pack(fill=tk.BOTH, expand=True)
        
        self.sensor_widgets = {}
        sensor_names = list(self.sensors.keys())
        
        for i, sensor_name in enumerate(sensor_names):
            row = i // 2
            col = i % 2
            
            # Create frame for this sensor
            sensor_frame = tk.Frame(sensors_container, bg=self.bg_dark)
            sensor_frame.grid(row=row, column=col, sticky='nsew', padx=6, pady=6)
            
            card = tk.Frame(sensor_frame, bg=self.bg_card, relief=tk.FLAT, 
                           highlightbackground=self.sensors[sensor_name]['color'],
                           highlightthickness=2)
            card.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
            
            # Card content
            content = tk.Frame(card, bg=self.bg_card)
            content.pack(fill=tk.BOTH, expand=True, padx=20, pady=18)
            
            # Header with status
            header = tk.Frame(content, bg=self.bg_card)
            header.pack(fill=tk.X)
            
            name_label = tk.Label(header, text=sensor_name.upper(), 
                                 font=("Helvetica", 10, "bold"),
                                 fg=self.text_gray, bg=self.bg_card, anchor='w')
            name_label.pack(side=tk.LEFT)
            
            status_dot = tk.Label(header, text="●", 
                                 font=("Helvetica", 20),
                                 fg=self.accent_green, bg=self.bg_card)
            status_dot.pack(side=tk.RIGHT)
            
            # Value display with fixed height
            value_frame = tk.Frame(content, bg=self.bg_card, height=100)
            value_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 10))
            value_frame.pack_propagate(False)
            
            value_label = tk.Label(value_frame, text="0", 
                                  font=("Helvetica", 42, "bold"),
                                  fg=self.sensors[sensor_name]['color'], 
                                  bg=self.bg_card, width=12, anchor='center')
            value_label.pack(expand=True)
            
            unit_label = tk.Label(value_frame, text=self.sensors[sensor_name]['unit'], 
                                 font=("Helvetica", 12),
                                 fg=self.text_gray, bg=self.bg_card, anchor='center')
            unit_label.pack()
            
            # Progress indicator
            progress_bg = tk.Frame(content, bg='#0d1126', height=8)
            progress_bg.pack(fill=tk.X)
            
            progress_fill = tk.Frame(progress_bg, bg=self.sensors[sensor_name]['color'], 
                                    height=8)
            progress_fill.place(relwidth=0, rely=0, relheight=1)
            
            self.sensor_widgets[sensor_name] = {
                'value': value_label,
                'unit': unit_label,
                'progress': progress_fill,
                'status': status_dot
            }
        
        # Configure grid weights
        for i in range(3):
            sensors_container.grid_rowconfigure(i, weight=1)
        for i in range(2):
            sensors_container.grid_columnconfigure(i, weight=1)
    
    def create_charts_section(self, parent):
        # Top row - Real-time graphs
        top_section = tk.Frame(parent, bg=self.bg_dark)
        top_section.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        
        # Weight sensor live feed
        weight_card = tk.Frame(top_section, bg=self.bg_card)
        weight_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))
        
        weight_title = tk.Label(weight_card, text="WEIGHT SENSOR - LIVE FEED", 
                               font=("Helvetica", 12, "bold"),
                               fg=self.text_white, bg=self.bg_card)
        weight_title.pack(pady=(12, 5))
        
        self.weight_fig = Figure(figsize=(5, 3), facecolor=self.bg_card)
        self.weight_ax = self.weight_fig.add_subplot(111)
        self.weight_canvas = FigureCanvasTkAgg(self.weight_fig, weight_card)
        self.weight_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Temperature & Light dual chart
        dual_card = tk.Frame(top_section, bg=self.bg_card)
        dual_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(4, 0))
        
        dual_title = tk.Label(dual_card, text="TEMPERATURE & LIGHT INTENSITY", 
                             font=("Helvetica", 12, "bold"),
                             fg=self.text_white, bg=self.bg_card)
        dual_title.pack(pady=(12, 5))
        
        self.dual_fig = Figure(figsize=(5, 3), facecolor=self.bg_card)
        self.temp_ax = self.dual_fig.add_subplot(111)
        self.light_ax = self.temp_ax.twinx()
        self.dual_canvas = FigureCanvasTkAgg(self.dual_fig, dual_card)
        self.dual_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Bottom row - System metrics and controls
        bottom_section = tk.Frame(parent, bg=self.bg_dark)
        bottom_section.pack(fill=tk.BOTH, expand=True, pady=(8, 0))
        
        # System metrics
        metrics_card = tk.Frame(bottom_section, bg=self.bg_card)
        metrics_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))
        
        metrics_title = tk.Label(metrics_card, text="SYSTEM PERFORMANCE", 
                                font=("Helvetica", 12, "bold"),
                                fg=self.text_white, bg=self.bg_card)
        metrics_title.pack(pady=(12, 15))
        
        self.create_system_metrics(metrics_card)
        
        # Sensor activity radar
        radar_card = tk.Frame(bottom_section, bg=self.bg_card)
        radar_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(4, 0))
        
        radar_title = tk.Label(radar_card, text="SENSOR ACTIVITY LEVELS", 
                              font=("Helvetica", 12, "bold"),
                              fg=self.text_white, bg=self.bg_card)
        radar_title.pack(pady=(12, 5))
        
        self.radar_fig = Figure(figsize=(4, 3), facecolor=self.bg_card)
        self.radar_ax = self.radar_fig.add_subplot(111, projection='polar')
        self.radar_canvas = FigureCanvasTkAgg(self.radar_fig, radar_card)
        self.radar_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def create_system_metrics(self, parent):
        metrics_frame = tk.Frame(parent, bg=self.bg_card)
        metrics_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 15))
        
        self.metric_widgets = {}
        
        metrics_layout = [
            ['CPU Usage', 'Memory'],
            ['Scan Time', 'Data Points']
        ]
        
        colors = [self.accent_cyan, self.accent_green, self.accent_orange, self.accent_purple]
        metric_idx = 0
        
        for row_metrics in metrics_layout:
            row_frame = tk.Frame(metrics_frame, bg=self.bg_card, height=90)
            row_frame.pack(fill=tk.BOTH, expand=True, pady=8)
            row_frame.pack_propagate(False)
            
            for metric_name in row_metrics:
                metric_card = tk.Frame(row_frame, bg='#0d1126')
                metric_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6)
                
                inner = tk.Frame(metric_card, bg='#0d1126')
                inner.pack(fill=tk.BOTH, expand=True, padx=18, pady=15)
                
                label = tk.Label(inner, text=metric_name.upper(), 
                               font=("Helvetica", 9, "bold"),
                               fg=self.text_gray, bg='#0d1126', anchor='w')
                label.pack(fill=tk.X)
                
                value = tk.Label(inner, text="0", 
                               font=("Helvetica", 32, "bold"),
                               fg=colors[metric_idx], bg='#0d1126', anchor='w', width=6)
                value.pack(fill=tk.X, pady=(8, 0))
                
                unit_text = '%' if metric_name in ['CPU Usage', 'Memory'] else ('ms' if metric_name == 'Scan Time' else '')
                unit = tk.Label(inner, text=unit_text, 
                              font=("Helvetica", 10),
                              fg=self.text_gray, bg='#0d1126', anchor='w')
                unit.pack(fill=tk.X)
                
                self.metric_widgets[metric_name] = value
                metric_idx += 1
        
        # Control buttons
        button_frame = tk.Frame(metrics_frame, bg=self.bg_card)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        scan_btn = tk.Button(button_frame, text="🔄 NEW SCAN", 
                            font=("Helvetica", 12, "bold"),
                            fg=self.text_white, bg=self.accent_cyan,
                            activebackground=self.accent_green,
                            relief=tk.FLAT, cursor="hand2",
                            command=self.new_scan, bd=0)
        scan_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6), ipady=12)
        
        self.pause_btn = tk.Button(button_frame, text="⏸ PAUSE", 
                                   font=("Helvetica", 12, "bold"),
                                   fg=self.text_white, bg=self.accent_orange,
                                   activebackground='#ff8c61',
                                   relief=tk.FLAT, cursor="hand2",
                                   command=self.toggle_scanning, bd=0)
        self.pause_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0), ipady=12)
    
    def update_graphs(self):
        # Weight sensor line chart
        self.weight_ax.clear()
        if len(self.weight_history) > 0:
            x = list(range(len(self.weight_history)))
            self.weight_ax.plot(x, self.weight_history, color=self.accent_cyan, 
                               linewidth=3, alpha=0.9)
            self.weight_ax.fill_between(x, self.weight_history, alpha=0.2, 
                                        color=self.accent_cyan)
        
        self.weight_ax.set_facecolor(self.bg_card)
        self.weight_ax.tick_params(colors=self.text_gray, labelsize=9)
        for spine in self.weight_ax.spines.values():
            spine.set_color(self.text_gray)
            spine.set_linewidth(0.5)
        self.weight_ax.grid(True, alpha=0.15, color=self.text_gray, linestyle='--')
        self.weight_ax.set_ylabel('Weight (g)', color=self.text_gray, fontsize=10)
        self.weight_fig.tight_layout()
        self.weight_canvas.draw()
        
        # Temperature & Light dual chart
        self.temp_ax.clear()
        self.light_ax.clear()
        
        if len(self.temp_history) > 0:
            x = list(range(len(self.temp_history)))
            self.temp_ax.plot(x, self.temp_history, color=self.accent_orange, 
                             linewidth=2.5, label='Temperature', alpha=0.9)
            self.light_ax.plot(x, self.light_history, color=self.accent_yellow, 
                              linewidth=2.5, label='Light', alpha=0.9, linestyle='--')
        
        self.temp_ax.set_facecolor(self.bg_card)
        self.temp_ax.tick_params(colors=self.text_gray, labelsize=9)
        self.light_ax.tick_params(colors=self.text_gray, labelsize=9)
        
        for spine in self.temp_ax.spines.values():
            spine.set_color(self.text_gray)
            spine.set_linewidth(0.5)
        
        self.temp_ax.set_ylabel('Temp (°C)', color=self.accent_orange, fontsize=10)
        self.light_ax.set_ylabel('Light (lux)', color=self.accent_yellow, fontsize=10)
        self.temp_ax.grid(True, alpha=0.15, color=self.text_gray, linestyle='--')
        
        # Add legend
        lines1, labels1 = self.temp_ax.get_legend_handles_labels()
        lines2, labels2 = self.light_ax.get_legend_handles_labels()
        self.temp_ax.legend(lines1 + lines2, labels1 + labels2, 
                           loc='upper left', fontsize=8, 
                           facecolor=self.bg_card, edgecolor=self.text_gray,
                           labelcolor=self.text_gray)
        
        self.dual_fig.tight_layout()
        self.dual_canvas.draw()
        
        # Radar chart for sensor activity
        self.radar_ax.clear()
        
        categories = ['Weight', 'IR Prox', 'Color', 'Temp', 'Camera', 'Light']
        values = [
            min(self.sensors['Weight Sensor']['value'] / 500 * 100, 100),
            min(self.sensors['IR Proximity']['value'] / 30 * 100, 100),
            min(sum(self.sensors['Color RGB']['value']) / 765 * 100, 100),
            min(self.sensors['Temperature']['value'] / 50 * 100, 100),
            min(self.sensors['Camera FPS']['value'] / 30 * 100, 100),
            min(self.sensors['Light Intensity']['value'] / 1000 * 100, 100)
        ]
        
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]
        
        self.radar_ax.plot(angles, values, 'o-', linewidth=2, color=self.accent_cyan)
        self.radar_ax.fill(angles, values, alpha=0.25, color=self.accent_cyan)
        self.radar_ax.set_xticks(angles[:-1])
        self.radar_ax.set_xticklabels(categories, fontsize=9, color=self.text_white)
        self.radar_ax.set_ylim(0, 100)
        self.radar_ax.set_facecolor(self.bg_card)
        self.radar_ax.tick_params(colors=self.text_gray, labelsize=8)
        self.radar_ax.grid(True, alpha=0.2, color=self.text_gray)
        self.radar_fig.patch.set_facecolor(self.bg_card)
        self.radar_canvas.draw()
    
    def animate_sensors(self):
        if not self.scanning:
            self.root.after(100, self.animate_sensors)
            return
        
        # Simulate realistic sensor readings
        self.sensors['Weight Sensor']['value'] = random.randint(150, 450)
        self.sensors['IR Proximity']['value'] = round(random.uniform(2.5, 25.0), 1)
        
        # RGB color sensor
        r, g, b = random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)
        self.sensors['Color RGB']['value'] = [r, g, b]
        
        self.sensors['Temperature']['value'] = round(random.uniform(18.0, 38.0), 1)
        self.sensors['Camera FPS']['value'] = random.randint(24, 30)
        self.sensors['Light Intensity']['value'] = random.randint(200, 900)
        
        # Update sensor cards
        for sensor_name, data in self.sensors.items():
            widgets = self.sensor_widgets[sensor_name]
            
            if sensor_name == 'Color RGB':
                r, g, b = data['value']
                widgets['value'].config(text=f"{r},{g},{b}")
                widgets['unit'].config(text="RGB")
                progress = (r + g + b) / 765
            else:
                widgets['value'].config(text=f"{data['value']}")
                
                if sensor_name == 'Weight Sensor':
                    progress = data['value'] / 500
                elif sensor_name == 'IR Proximity':
                    progress = data['value'] / 30
                elif sensor_name == 'Temperature':
                    progress = data['value'] / 50
                elif sensor_name == 'Camera FPS':
                    progress = data['value'] / 30
                elif sensor_name == 'Light Intensity':
                    progress = data['value'] / 1000
            
            widgets['progress'].place(relwidth=min(progress, 1), rely=0, relheight=1)
        
        # Update histories
        self.weight_history.append(self.sensors['Weight Sensor']['value'])
        if len(self.weight_history) > 30:
            self.weight_history.pop(0)
        
        self.temp_history.append(self.sensors['Temperature']['value'])
        if len(self.temp_history) > 30:
            self.temp_history.pop(0)
        
        self.light_history.append(self.sensors['Light Intensity']['value'])
        if len(self.light_history) > 30:
            self.light_history.pop(0)
        
        # Update system metrics
        self.system_metrics['CPU Usage'] = random.randint(35, 85)
        self.system_metrics['Memory'] = random.randint(45, 75)
        self.system_metrics['Scan Time'] = random.randint(120, 350)
        self.system_metrics['Data Points'] = len(self.weight_history) * 6
        
        for metric_name, value in self.system_metrics.items():
            if metric_name in self.metric_widgets:
                self.metric_widgets[metric_name].config(text=str(value))
        
        self.update_graphs()
        self.root.after(1000, self.animate_sensors)
    
    def new_scan(self):
        self.scan_count += 1
        self.scan_count_label.config(text=f"Scans: {self.scan_count}")
        
        for sensor in self.sensors.values():
            if isinstance(sensor['value'], list):
                sensor['value'] = [0, 0, 0]
            else:
                sensor['value'] = 0
        
        self.weight_history = []
        self.temp_history = []
        self.light_history = []
        self.update_graphs()
        
        if not self.scanning:
            self.toggle_scanning()
    
    def toggle_scanning(self):
        self.scanning = not self.scanning
        if self.scanning:
            self.status_label.config(text="● SCANNING", fg=self.accent_green)
            self.pause_btn.config(text="⏸ PAUSE", bg=self.accent_orange)
        else:
            self.status_label.config(text="● PAUSED", fg=self.accent_orange)
            self.pause_btn.config(text="▶ RESUME", bg=self.accent_green)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScanMyBhojanDashboard(root)
    root.mainloop()
