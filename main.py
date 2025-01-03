import pygame
import sys
import io
import cairosvg
from PIL import Image

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Skateboard Shop")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 100, 255)

# Fonts
font = pygame.font.Font(None, 36)

def svg_to_pygame_surface(svg_path, width=None, height=None):
    """Convert SVG to Pygame surface"""
    try:
        if width and height:
            png_data = cairosvg.svg2png(url=svg_path, output_width=width, output_height=height)
        else:
            png_data = cairosvg.svg2png(url=svg_path)
        
        bytes_io = io.BytesIO(png_data)
        image = Image.open(bytes_io)
        return pygame.image.fromstring(image.tobytes(), image.size, image.mode)
    except Exception as e:
        # Fallback to colored rectangle if SVG loading fails
        surface = pygame.Surface((100, 200))
        surface.fill(BLUE)
        return surface

# Load assets
try:
    background = svg_to_pygame_surface("assets/shop_background.svg", SCREEN_WIDTH, SCREEN_HEIGHT)
    deck_images = [
        svg_to_pygame_surface("assets/deck1.svg", 100, 300),
        svg_to_pygame_surface("assets/deck2.svg", 100, 300)
    ]
    grip_tape_image = svg_to_pygame_surface("assets/grip_tape.svg", 100, 300)
except Exception as e:
    # Create fallback surfaces if asset loading fails
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(BLACK)
    
    deck_images = [
        pygame.Surface((100, 300)),
        pygame.Surface((100, 300))
    ]
    for deck in deck_images:
        deck.fill(GRAY)
        
    grip_tape_image = pygame.Surface((100, 300))
    grip_tape_image.fill(WHITE)

# Menu setup
menu_box = pygame.Surface((300, 200), pygame.SRCALPHA)
menu_box.fill((0, 0, 255, 128))  # Semi-transparent blue

# Game state
menu_items = ["Change Deck", "Griptape", "Wheel Color", "Done"]
selected_item = 0
current_deck = 0
wheel_colors = ["Red", "Blue", "Green"]
current_wheel_color = 0
show_grip_tape = False

def draw_shop_items():
    """Draw the shop items on screen"""
    # Draw decks on the wall
    for i, deck in enumerate(deck_images):
        x = 100 + i * 120
        y = 100
        # Highlight selected deck
        if i == current_deck:
            pygame.draw.rect(screen, BLUE, (x-5, y-5, 110, 310), 3)
        screen.blit(deck, (x, y))
    
    # Draw grip tape if selected
    if show_grip_tape:
        screen.blit(grip_tape_image, (350, 100))

def draw_menu():
    """Draw the menu interface"""
    # Draw menu background
    screen.blit(menu_box, (450, 150))
    
    # Draw menu options
    for i, item in enumerate(menu_items):
        color = WHITE if i == selected_item else GRAY
        text = font.render(item, True, color)
        screen.blit(text, (470, 170 + i * 40))
        
    # Draw current wheel color
    if wheel_colors:
        color_text = font.render(f"Current Wheel: {wheel_colors[current_wheel_color]}", 
                               True, WHITE)
        screen.blit(color_text, (470, 350))

def handle_menu_selection():
    """Handle menu item selection"""
    global current_deck, show_grip_tape, current_wheel_color
    
    if menu_items[selected_item] == "Change Deck":
        current_deck = (current_deck + 1) % len(deck_images)
    elif menu_items[selected_item] == "Griptape":
        show_grip_tape = not show_grip_tape
    elif menu_items[selected_item] == "Wheel Color":
        current_wheel_color = (current_wheel_color + 1) % len(wheel_colors)
    elif menu_items[selected_item] == "Done":
        return True
    return False

def main():
    """Main game loop"""
    global selected_item
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        screen.fill(BLACK)
        screen.blit(background, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if handle_menu_selection():
                        running = False
                        
        draw_shop_items()
        draw_menu()
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
