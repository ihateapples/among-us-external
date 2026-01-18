# this code belongs to ihateapples on github. this SHOULD be open sourced.
# ^ me leaving it open source is me being nice. you can build it into an exe yourself if u r a lazy fuck and cant just run a python script.
# but this whole thing is simple. it just reads off memory and displays it on a big fancy gui.
# it was ORIGINALLY going to be called jeffrey epstein's among us cheat but i think thats a bit STUPID and i want my actual credit instead of some pedophile getting it...
# once again this whole thing just reads off memory and displays it. theres NOT MUCH happening behind the scenes. sorry to disappoint you

import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import time
import pymem
import os
import sys
import subprocess
import ctypes
import tkinter.font as tkfont
import math

# loading splash effect

def show_loading_splash(): # yeah i reuse the "loading.png" for the splash screen and window icon. it's fine, i can just say it has multiple use cases?
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.attributes("-topmost", True)
    splash.attributes("-transparentcolor", "black")

    try:
        original_img = Image.open("loading.png")
        max_size = (400, 400)
        original_img.thumbnail(max_size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(original_img)
        
        w, h = original_img.size
        screen_w = splash.winfo_screenwidth()
        screen_h = splash.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        splash.geometry(f"{w}x{h}+{x}+{y}")

        label = tk.Label(splash, image=photo, bg="black", bd=0, highlightthickness=0)
        label.image = photo
        label.pack()

        splash.attributes("-alpha", 0.0)
        splash.update()
        for i in range(0, 101, 4):
            splash.attributes("-alpha", i / 100.0)
            splash.update()
            time.sleep(0.015)

        time.sleep(1.5)

        for i in range(100, -1, -5):
            splash.attributes("-alpha", i / 100.0)
            splash.update()
            time.sleep(0.015)

    except Exception:
        splash.geometry("200x100")
        tk.Label(splash, text="...", bg="black", fg="#555", font=("Arial", 60)).pack()
        time.sleep(3)

    splash.destroy()

# this is the main cheat class here with the cool llittle green debug panel and my github being plugged in cool strobing text.

class MemoryReader:
    def __init__(self, root, process_name):
        self.root = root
        self.process_name = process_name
        self.base_address = None
        self.platform = None
        self.auto_running = False
        self.steam_offset = 0x02988984
        
        self.roles = {
            0: "Crewmate", 1: "Impostor", 2: "Scientist", 3: "Engineer",
            4: "Guardian Angel", 5: "Shapeshifter", 6: "Dead", 7: "Dead (Imp)",
            8: "Noise Maker", 9: "Phantom", 10: "Tracker", 12: "Detective", 18: "Viper"
        }
        self.colors_hex = ['#D71E22', '#1D3CE9', '#1B913E', '#FF63D4', '#FF8D1C', '#FFFF67',
                           '#4A565E', '#E9F7FF', '#783DD2', '#80582D', '#44FFF7', '#5BFE4B',
                           '#6C2B3D', '#FFD6EC', '#FFFFBE', '#8397A7', '#9F9989', '#EC7578']
        self.colors_name = ['Red', 'Blue', 'Green', 'Pink', 'Orange', 'Yellow', 'Black',
                            'White', 'Purple', 'Brown', 'Cyan', 'Lime', 'Maroon', 'Rose',
                            'Banana', 'Grey', 'Tan', 'Coral']
        self.row_widgets = {}

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        if sys.platform.startswith('win'):
            try:
                font_path = os.path.abspath("minecraft.ttf")
                ctypes.windll.gdi32.AddFontResourceA(font_path.encode())
                self.root.update()
            except:
                pass

        families = tkfont.families()
        self.font_family = "Minecraft" if "Minecraft" in families else "Arial"
        
        self.header_font = (self.font_family, 24, "bold")
        self.label_font = (self.font_family, 14)
        self.small_font = (self.font_family, 12)

        self.root.title("apple's among us panel ( crafted with the help of Father Yakub )")
        self.root.geometry("900x750")

        self.header = ctk.CTkLabel(self.root, text="apple's among us panel",
                                   font=self.header_font, text_color="#00FF00")
        self.header.pack(padx=20, pady=(20, 10))

        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15, fg_color="#1a1a1a")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=10)

        self.sidebar = ctk.CTkFrame(self.main_frame, width=200, corner_radius=10, fg_color="#252525")
        self.sidebar.pack(side="left", fill="y", padx=(0, 10), pady=10)
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(self.sidebar, text="Controls", font=self.label_font).pack(pady=(10, 5))

        self.scan_btn = ctk.CTkButton(self.sidebar, text="Scan Now", width=180, 
                                      command=self.scan_once, font=self.small_font)
        self.scan_btn.pack(pady=5)

        self.auto_switch = ctk.CTkSwitch(self.sidebar, text="Auto Refresh", 
                                         command=self.toggle_auto, font=self.small_font)
        self.auto_switch.pack(pady=5)

        self.interval_label = ctk.CTkLabel(self.sidebar, text="Interval (s)", font=self.small_font)
        self.interval_label.pack(pady=(5, 0))

        self.interval_slider = ctk.CTkSlider(self.sidebar, from_=0.1, to=1.0, number_of_steps=18)
        self.interval_slider.set(0.2)
        self.interval_slider.pack(pady=5, padx=10)

        self.players_list = ctk.CTkScrollableFrame(self.main_frame, corner_radius=15, fg_color="#1a1a1a")
        self.players_list.pack(side="left", expand=True, fill="both", pady=10)

        header = ctk.CTkFrame(self.players_list, fg_color="#333333", corner_radius=5)
        header.pack(fill="x", padx=10, pady=(10, 5))
        ctk.CTkLabel(header, text="Name", width=250, anchor="w", font=self.small_font).pack(side="left", padx=10)
        ctk.CTkLabel(header, text="Role", width=180, anchor="w", font=self.small_font).pack(side="left", padx=10)
        ctk.CTkLabel(header, text="Color", width=150, anchor="w", font=self.small_font).pack(side="left", padx=10)
        ctk.CTkLabel(header, text="Alive", width=80, anchor="w", font=self.small_font).pack(side="left", padx=10)
        ctk.CTkLabel(header, text="Position", width=120, anchor="w", font=self.small_font).pack(side="left", padx=10)

        self.status_frame = ctk.CTkFrame(self.root, fg_color="#1a1a1a", corner_radius=10)
        self.status_frame.pack(fill="x", padx=20, pady=(0, 5))

        self.status_bar = ctk.CTkLabel(self.status_frame, text="Ready", font=self.small_font, text_color="#AAAAAA")
        self.status_bar.pack(side="left", padx=10)

        self.loading_bar = ctk.CTkProgressBar(self.status_frame, mode="indeterminate", width=300)
        self.loading_bar.pack(side="right", padx=10)
        self.loading_bar.stop()

        # this controls my github footer
        self.footer_frame = ctk.CTkFrame(self.root, fg_color="transparent", height=40)
        self.footer_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.promo = "github.com/ihateapples" # you really can't even hate me for plugging my github.
        self.letter_labels = []

        letter_frame = ctk.CTkFrame(self.footer_frame, fg_color="transparent")
        letter_frame.pack(expand=True)

        for char in self.promo:
            lbl = ctk.CTkLabel(
                letter_frame,
                text=char if char != " " else "  ",
                font=(self.font_family, 14, "bold"),
                text_color="#ffffff"
            )
            lbl.pack(side="left", padx=0)
            self.letter_labels.append(lbl)

        self.rainbow_phase = 0
        self.animate_per_letter_rainbow()

        # this is for the debug panel
        self.debug_frame = ctk.CTkFrame(self.root, fg_color="#0d0d0d", corner_radius=8, height=140)
        self.debug_frame.pack(fill="x", padx=20, pady=(0, 15))
        self.debug_frame.pack_propagate(False)

        self.debug_text = ctk.CTkTextbox(
            self.debug_frame,
            height=120,
            fg_color="#111111",
            text_color="#88ff88",
            font=("Consolas", 11),
            state="disabled"
        )
        self.debug_text.pack(padx=8, pady=8, fill="both", expand=True)

        self.debug_text.tag_config("info", foreground="#88ff88")
        self.debug_text.tag_config("error", foreground="#ff5555")

        self.log_debug("debug panel initalized. press 1 (keybind) or just press scan now. it does the same thing.")

    def animate_per_letter_rainbow(self):
        for i, lbl in enumerate(self.letter_labels):
            # fast wave, bigger step + smaller delay
            hue = (self.rainbow_phase + i * 40) % 360   # 40 = wider spacing between letters
            r = int(127 * (1 + math.sin(math.radians(hue))))
            g = int(127 * (1 + math.sin(math.radians(hue + 120))))
            b = int(127 * (1 + math.sin(math.radians(hue + 240))))
            color = f"#{r:02x}{g:02x}{b:02x}"
            lbl.configure(text_color=color)

        self.rainbow_phase += 12          # faster color cycling
        self.root.after(40, self.animate_per_letter_rainbow)  # ~25 fps so its fast & smooth

    def log_debug(self, message, error=False):
        timestamp = time.strftime("%H:%M:%S")
        prefix = "[ERROR]" if error else "[INFO]"
        tag = "error" if error else "info"

        full_msg = f"{timestamp} {prefix} {message}\n"

        self.debug_text.configure(state="normal")
        self.debug_text.insert("end", full_msg)
        self.debug_text.tag_add(tag, "end-1l", "end")
        self.debug_text.see("end")
        self.debug_text.configure(state="disabled")

        line_count = int(self.debug_text.index("end-1c").split('.')[0])
        if line_count > 60:
            self.debug_text.configure(state="normal")
            self.debug_text.delete("1.0", f"{line_count-50}.0")
            self.debug_text.configure(state="disabled")

    # this searches for Among Us.exe and just sniffs out whats important.
    def detect_platform(self):
        self.log_debug("Attempting to detect platform...")
        try:
            pm = pymem.Pymem("Among Us.exe")
            self.log_debug("Among Us.exe process found")
            module = pymem.process.module_from_name(pm.process_handle, "GameAssembly.dll")
            base = module.lpBaseOfDll
            self.log_debug(f"GameAssembly.dll base: 0x{base:x}")
            steam_addr = pm.read_uint(base + self.steam_offset)
            pm.read_uint(steam_addr + 0x5C)
            self.log_debug("Steam platform signature matched")
            return "steam"
        except Exception as e:
            self.log_debug(f"Platform detection failed: {str(e)}", error=True)
            return "unknown"
        finally:
            try:
                pm.close_process()
            except:
                pass

    def ensure_base(self):
        self.log_debug("Ensuring base address...")
        if self.platform is None or self.base_address is None:
            self.platform = self.detect_platform()
            self.log_debug(f"Platform set to: {self.platform}")
            try:
                pm = pymem.Pymem("Among Us.exe")
                module = pymem.process.module_from_name(pm.process_handle, "GameAssembly.dll")
                base = module.lpBaseOfDll
                if self.platform == "steam":
                    add_off = pm.read_uint(base + self.steam_offset)
                    self.log_debug(f"Steam offset value: 0x{add_off:x}")
                    self.base_address = pm.read_uint(add_off + 0x5C)
                    self.base_address = pm.read_uint(self.base_address)
                    self.log_debug(f"Final base address: 0x{self.base_address:x}")
                pm.close_process()
            except Exception as e:
                self.log_debug(f"Base address calculation failed: {str(e)}", error=True)

    def read_players(self):
        self.log_debug("Reading players...")
        if self.platform == "steam":
            return self.read_players_steam()
        self.log_debug("No supported platform detected", error=True)
        return []

    def read_players_steam(self):
        players = []
        pm = None
        try:
            self.log_debug("Opening process for reading...")
            pm = pymem.Pymem("Among Us.exe")
            allclients_ptr = pm.read_uint(self.base_address + 0x38)
            self.log_debug(f"AllClients pointer: 0x{allclients_ptr:x}")
            items_ptr = pm.read_uint(allclients_ptr + 0x8)
            items_count = pm.read_uint(allclients_ptr + 0xC)
            self.log_debug(f"Player count: {items_count}")

            for i in range(items_count):
                item_base = pm.read_uint(items_ptr + 0x10 + (i * 4))
                item_char_ptr = pm.read_uint(item_base + 0x10)
                item_data_ptr = pm.read_uint(item_char_ptr + 0x58)
                item_role_ptr = pm.read_uint(item_data_ptr + 0x4C)
                item_role = pm.read_uint(item_role_ptr + 0x10)
                role_name = self.roles.get(item_role, f"Unknown ({item_role})")

                rb2d = pm.read_uint(item_char_ptr + 0xD0)
                rb2d_cached = pm.read_uint(rb2d + 0x8)
                x_val = pm.read_float(rb2d_cached + 0x7C)
                y_val = pm.read_float(rb2d_cached + 0x80)

                color_id = pm.read_uint(item_base + 0x28)
                name_ptr = pm.read_uint(item_base + 0x1C)
                name_len = pm.read_uint(name_ptr + 0x8)
                name_addr = name_ptr + 0xC
                raw = pm.read_bytes(name_addr, name_len * 2)
                name = raw.decode('utf-16').rstrip('\x00')

                alive = role_name not in ["Dead", "Dead (Imp)", "Guardian Angel"]

                player_data = {
                    "key": name,
                    "name": name,
                    "role": role_name,
                    "alive": alive,
                    "color_id": color_id,
                    "color_name": self.colors_name[color_id] if 0 <= color_id < len(self.colors_name) else str(color_id),
                    "color_hex": self.colors_hex[color_id] if 0 <= color_id < len(self.colors_hex) else "#AAAAAA",
                    "x": x_val,
                    "y": y_val
                }
                players.append(player_data)
                self.log_debug(f"  Read player: {name} | {role_name} | {player_data['color_name']}")

            self.log_debug(f"Successfully read {len(players)} players")
        except Exception as e:
            self.log_debug(f"Memory read error: {str(e)}", error=True)
        finally:
            if pm:
                try:
                    pm.close_process()
                except:
                    pass
        return players

    def role_style(self, role):
        if role in ["Impostor", "Shapeshifter", "Phantom", "Viper"]:
            return {"fg_color": "#150505", "text_color": "#FF3333"}
        if role in ["Dead", "Dead (Imp)", "Guardian Angel"]:
            return {"fg_color": "#111111", "text_color": "#777777"}
        return {"fg_color": "#0d0d0d", "text_color": "#00FF00"}

    def hex_to_rgb(self, hex_str):
        hex_str = hex_str.lstrip('#')
        return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def upsert_row(self, p):
        key = p["key"]
        style = self.role_style(p["role"])
        
        if key not in self.row_widgets:
            row = ctk.CTkFrame(self.players_list, corner_radius=10, fg_color=style["fg_color"], height=50)
            row.pack(fill="x", padx=10, pady=5)

            name_lbl = ctk.CTkLabel(row, width=250, anchor="w", font=self.small_font)
            role_lbl = ctk.CTkLabel(row, width=180, anchor="w", font=self.small_font)

            color_wrap = ctk.CTkFrame(row, fg_color="transparent")
            color_box = ctk.CTkFrame(color_wrap, width=24, height=20, corner_radius=5)
            color_box.pack_propagate(False)

            color_lbl = ctk.CTkLabel(row, width=120, anchor="w", font=self.small_font)
            alive_lbl = ctk.CTkLabel(row, width=80, anchor="w", font=self.small_font)
            pos_lbl = ctk.CTkLabel(row, width=120, anchor="w", font=self.small_font)

            name_lbl.pack(side="left", padx=10, pady=8)
            role_lbl.pack(side="left", padx=10)
            color_wrap.pack(side="left", padx=10)
            color_box.pack(in_=color_wrap, side="left", pady=8)
            color_lbl.pack(side="left", padx=(0, 10))
            alive_lbl.pack(side="left", padx=10)
            pos_lbl.pack(side="left", padx=10)

            self.row_widgets[key] = {
                "row": row,
                "name": name_lbl,
                "role": role_lbl,
                "color_box": color_box,
                "color_lbl": color_lbl,
                "alive": alive_lbl,
                "pos": pos_lbl
            }

            name_lbl.configure(text=p["name"], text_color=style["text_color"])
            role_lbl.configure(text=p["role"], text_color=style["text_color"])
            color_box.configure(fg_color=p["color_hex"])
            color_lbl.configure(text=p["color_name"], text_color=style["text_color"])
            alive_lbl.configure(text="Yes" if p["alive"] else "No", text_color=style["text_color"])
            pos_lbl.configure(text=f"({p['x']:.2f}, {p['y']:.2f})", text_color=style["text_color"])

            self.fade_in_row(self.row_widgets[key], style)
            self.log_debug(f"Displayed: {p['name']} ({p['role']})")

        else:
            w = self.row_widgets[key]
            w["row"].configure(fg_color=style["fg_color"])
            w["name"].configure(text=p["name"], text_color=style["text_color"])
            w["role"].configure(text=p["role"], text_color=style["text_color"])
            w["color_box"].configure(fg_color=p["color_hex"])
            w["color_lbl"].configure(text=p["color_name"], text_color=style["text_color"])
            w["alive"].configure(text="Yes" if p["alive"] else "No", text_color=style["text_color"])
            w["pos"].configure(text=f"({p['x']:.2f}, {p['y']:.2f})", text_color=style["text_color"])

    def fade_in_row(self, widgets, style):
        base_color = style['text_color']
        target_rgb = self.hex_to_rgb(base_color)
        start_rgb = (max(0, target_rgb[0]//5), max(0, target_rgb[1]//5), max(0, target_rgb[2]//5))

        def fade_step(step=0):
            if step > 20:
                widgets["name"].configure(text_color=base_color)
                widgets["role"].configure(text_color=base_color)
                widgets["color_lbl"].configure(text_color=base_color)
                widgets["alive"].configure(text_color=base_color)
                widgets["pos"].configure(text_color=base_color)
                return

            ratio = step / 20.0
            r = int(start_rgb[0] + (target_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (target_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (target_rgb[2] - start_rgb[2]) * ratio)
            current_color = self.rgb_to_hex((r, g, b))

            widgets["name"].configure(text_color=current_color)
            widgets["role"].configure(text_color=current_color)
            widgets["color_lbl"].configure(text_color=current_color)
            widgets["alive"].configure(text_color=current_color)
            widgets["pos"].configure(text_color=current_color)

            self.root.after(35, lambda: fade_step(step + 1))

        fade_step()

    def prune_rows(self, valid_keys):
        to_remove = [k for k in self.row_widgets if k not in valid_keys]
        for k in to_remove:
            try:
                self.row_widgets[k]["row"].destroy()
            except:
                pass
            self.row_widgets.pop(k, None)
        if to_remove:
            self.log_debug(f"Removed {len(to_remove)} old/invalid player rows")

    def scan_once(self):
        try:
            self.status_bar.configure(text="Scanning...", text_color="#FFFF00")
            self.loading_bar.start()
            self.root.update()

            self.ensure_base()

            players = self.read_players()
            self.log_debug(f"Players retrieved: {len(players)}")

            players.sort(key=lambda x: x["name"].lower())
            valid = set()
            for p in players:
                self.upsert_row(p)
                valid.add(p["key"])

            self.prune_rows(valid)
            self.log_debug(f"Scan finished – {len(players)} players displayed")
            self.status_bar.configure(text=f"Platform: {self.platform} | Players: {len(players)}", text_color="#AAAAAA")
        except Exception as e:
            self.log_debug(f"Critical scan error: {str(e)}", error=True)
            self.status_bar.configure(text=f"Error: {str(e)}", text_color="#FF0000")
        finally:
            self.loading_bar.stop()

    def schedule_auto(self):
        if not self.auto_running:
            return
        self.scan_once()
        interval = max(0.1, float(self.interval_slider.get()))
        self.root.after(int(interval * 1000), self.schedule_auto)

    def toggle_auto(self):
        state = self.auto_switch.get()
        if state and not self.auto_running:
            self.auto_running = True
            self.log_debug("Auto-refresh enabled")
            self.schedule_auto()
        else:
            self.auto_running = False
            self.log_debug("Auto-refresh disabled")

def close_app(root, reader):
    reader.auto_running = False
    root.destroy()

def self_delete(root):
    exe_name = os.path.basename(sys.executable)
    prefetch_name = f"{exe_name.upper()}-*.pf"
    prefetch_dir = r"C:\Windows\prefetch"
    cmd = (
        f"cmd /c ping localhost -n 3 > nul & "
        f"del /f /q \"{sys.executable}\" & "
        f"del /f /q \"{os.path.join(prefetch_dir, prefetch_name)}\""
    )
    subprocess.Popen(cmd, shell=True)
    root.destroy()

# this is the entry point

if __name__ == "__main__":
    show_loading_splash()

    app = ctk.CTk()

    try:
        app.iconbitmap("loading.ico")
    except:
        try:
            icon_img = Image.open("loading.png")
            photo = ImageTk.PhotoImage(icon_img)
            app.iconphoto(True, photo)
        except:
            pass

    reader = MemoryReader(app, "Among Us.exe")

    app.protocol("WM_DELETE_WINDOW", lambda: close_app(app, reader))
    app.mainloop()