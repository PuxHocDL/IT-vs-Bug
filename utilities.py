import pygame
import json


def apply_brightness(surface, brightness):
    """Apply brightness to the surface."""
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    if brightness > 0:
        # Decrease brightness
        overlay.fill((0, 0, 0, int((1 - brightness) * 255)))

    surface.blit(overlay, (0, 0))
    return surface


def load_json(file_path):
    data = None
    with open(file_path) as f:
        data = json.load(f)
    return data
