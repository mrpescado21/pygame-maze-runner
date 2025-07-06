import sys
import time
import asyncio
import hashlib
import pygame

from mazegenerator import maze_generate, TileType


# Init pygame
screen_width: int = 384
screen_height: int = 216
screen_width_ratio: float = float(screen_width) / float(screen_height)
screen_height_ratio: float = float(screen_height) / float(screen_width)
screen: pygame.Surface = pygame.Surface((screen_width, screen_height))
screen.fill((0, 0, 0))

pygame.draw.circle(screen, (255, 255, 255), (screen_width // 2, screen_height // 2), 64)
    
screen_scaled_width: int
screen_scaled_height: int
screen_scaled: pygame.Surface
screen_scaled_rect: pygame.Rect
display_width: int = screen_width * 4
display_height: int = screen_height * 4
display_fullscreen: bool = False
display_windowed_width: int = display_width
display_windowed_height: int = display_height
pygame.init()
display: pygame.Surface


def setup_display():
    global display_width
    global display_height
    global display
    global screen_scaled
    global screen_scaled_width
    global screen_scaled_height
    global screen_scaled_rect

    if display_fullscreen:
        display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        display_width, display_height = pygame.display.get_window_size()
    else:
        display = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
    pygame.display.set_caption("Maze Runner")
    display.fill((0, 0, 0))
    
    if float(display_height) / float(display_width) >= screen_height_ratio:
        screen_scaled_width = display_width
        screen_scaled_height = int(screen_scaled_width * screen_height_ratio)
    else:
        screen_scaled_height = display_height
        screen_scaled_width = int(screen_scaled_height * screen_width_ratio)
    screen_scaled = pygame.Surface((screen_scaled_width, screen_scaled_height))
    screen_scaled_rect = screen_scaled.get_rect()
    screen_scaled_rect.center = display.get_rect().center


async def main():
    # We're going to update the display size based on pygame events below
    global display_width
    global display_height
    global display_fullscreen
    global display_windowed_width
    global display_windowed_height

    # Setup the pygame display and grab the clock
    setup_display()
    clock = pygame.time.Clock()
    
    # To deal with fluctuations in frame rate, we need to
    # keep getting the time delta between frames
    time_last: float = time.time()
    time_delta: float
    # Setup FPS calculation
    fps_calc_frames: int = 120
    fps_frames: int = 0
    fps_last_time: float = time_last
    fps: float = 0

    running = True
    while running:
        # Get the delta time
        time_current: float = time.time()
        time_delta = time_current - time_last
        time_last = time_current
        # Calculate FPS
        fps_frames += 1
        if fps_frames > fps_calc_frames:
            fps = float(fps_frames) / (time_current - fps_last_time)
            fps_frames = 0
            fps_last_time = time_current
            pygame.display.set_caption(f"Maze Runner: {fps:.1f}")
        
        # Handle pygame events
        for event in pygame.event.get():
            # Check for closing the window
            if event.type == pygame.QUIT:
                running = False
            # Check for display resize
            elif event.type == pygame.VIDEORESIZE:
                display_width, display_height = event.size
                setup_display()
            # Check for key presses
            elif event.type == pygame.KEYDOWN:
                # F - Toggle fullscreen or windowed
                if event.key == pygame.K_f:
                    display_fullscreen = not display_fullscreen
                    if display_fullscreen:
                        display_windowed_width = display_width
                        display_windowed_height = display_height
                    else:
                        display_width = display_windowed_width
                        display_height = display_windowed_height
                    setup_display()

        # Scale the screen and draw it on the display
        pygame.transform.scale(screen, (screen_scaled_width, screen_scaled_height), screen_scaled)
        display.blit(screen_scaled, screen_scaled_rect)
        # Flip to display what we have drawn
        pygame.display.flip()
        # Yield control to asyncio event loop
        await asyncio.sleep(0)
        # Cap at 60 fps
        clock.tick(60)


    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())