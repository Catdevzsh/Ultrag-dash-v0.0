import tkinter as tk
from tkinter import messagebox
import random
import pygame.midi
import time
import sys

# Initialize Pygame MIDI
pygame.midi.init()
midi_initialized = False

try:
    player = pygame.midi.Output(0)
    midi_initialized = True
    player.set_instrument(0)  # Use piano as the instrument
except pygame.midi.MidiException as e:
    print("Error initializing MIDI:", e)
    pygame.midi.quit()

class GeometryDashGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Geometry Dash by AI")
        self.root.geometry("600x400")
        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.score = 0
        self.running = True

        self.player = self.canvas.create_rectangle(50, 350, 70, 370, fill="blue")
        self.obstacles = []

        self.jump_height = -10
        self.gravity = 1
        self.jump_speed = 0
        self.is_jumping = False

        self.root.bind("<space>", self.jump)
        self.root.after(100, self.spawn_obstacle)
        self.root.after(100, self.update)

    def play_sound(self):
        if midi_initialized:
            # Play a random note
            note = random.randint(60, 72)  # Random note in one octave
            player.note_on(note, 127)
            time.sleep(0.1)
            player.note_off(note, 127)

    def jump(self, event):
        if self.running and not self.is_jumping:
            self.jump_speed = self.jump_height
            self.is_jumping = True
            self.play_sound()

    def spawn_obstacle(self):
        if self.running:
            x = 600
            y = 350
            obstacle = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="red")
            self.obstacles.append(obstacle)
            self.root.after(random.randint(1500, 2500), self.spawn_obstacle)

    def update(self):
        if self.running:
            if self.is_jumping:
                self.canvas.move(self.player, 0, self.jump_speed)
                self.jump_speed += self.gravity
                if self.canvas.coords(self.player)[1] >= 350:
                    self.canvas.coords(self.player, 50, 350, 70, 370)
                    self.is_jumping = False

            for obstacle in self.obstacles:
                self.canvas.move(obstacle, -10, 0)
                pos = self.canvas.coords(obstacle)
                if pos[2] < 0:
                    self.canvas.delete(obstacle)
                    self.obstacles.remove(obstacle)
                    self.score += 1
                elif self.check_collision(self.player, obstacle):
                    self.running = False
                    messagebox.showinfo("Game Over", f"Game Over! Your score: {self.score}")
                    self.root.destroy()
                    if midi_initialized:
                        pygame.midi.quit()
                    return
            self.root.after(50, self.update)

    def check_collision(self, player, obstacle):
        player_coords = self.canvas.coords(player)
        obstacle_coords = self.canvas.coords(obstacle)
        overlap = self.canvas.find_overlapping(*player_coords)
        return obstacle in overlap

if __name__ == "__main__":
    root = tk.Tk()
    game = GeometryDashGame(root)
    root.mainloop()
