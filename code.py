import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (128, 128, 128)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)

class SignUpEveryLikeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Number Increaser")
        self.clock = pygame.time.Clock()

        # Game state
        self.number = 0
        self.increment_rate = 1.0  # Starting rate per second
        self.last_increment_time = pygame.time.get_ticks()
        self.is_signed_up = False
        self.total_likes = 0
        self.total_signups = 0

        # UI elements
        self.signup_button = pygame.Rect(SCREEN_WIDTH//2 - 120, 350, 240, 50)
        self.like_button = pygame.Rect(SCREEN_WIDTH//2 - 80, 450, 160, 60)

        # Fonts
        self.font_title = pygame.font.Font(None, 56)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

        # Animation variables
        self.like_animation = 0
        self.signup_animation = 0
        self.floating_texts = []
        self.particles = []

        # Account names (randomly generated)
        self.current_account_name = ""
        self.account_names = []

    def generate_account_name(self):
        """Generate a random account name"""
        adjectives = ["Cool", "Super", "Amazing", "Epic", "Awesome", "Stellar", "Fantastic", "Incredible", "Mighty", "Ultimate"]
        nouns = ["User", "Player", "Gamer", "Hero", "Champion", "Master", "Legend", "Pro", "Star", "Ace", "Bread"]
        number = random.randint(100, 9999)
        return f"{random.choice(adjectives)}{random.choice(nouns)}{number}"

    def sign_up(self):
        """Handle sign up action"""
        if not self.is_signed_up:
            self.is_signed_up = True
            self.total_signups += 1
            self.current_account_name = self.generate_account_name()
            self.account_names.append(self.current_account_name)
            self.signup_animation = 30

            self.add_floating_text(f"Welcome {self.current_account_name}!", 
                                 SCREEN_WIDTH//2, 320, GREEN)
            self.create_signup_particles(SCREEN_WIDTH//2, 350)

    def give_like(self):
        """Handle like action - requires being signed up"""
        if self.is_signed_up:
            self.total_likes += 1
            self.increment_rate += 0.2  # Each like increases rate by 0.2
            self.like_animation = 25

            # Sign out immediately after liking!
            self.is_signed_up = False

            # Add floating text
            self.add_floating_text(f"+0.2/sec boost!", SCREEN_WIDTH//2, 420, BLUE)
            self.add_floating_text("Account logged out!", SCREEN_WIDTH//2, 480, ORANGE)

            # Create particles
            self.create_like_particles(SCREEN_WIDTH//2, 450)

    def add_floating_text(self, text, x, y, color):
        """Add floating text effect"""
        self.floating_texts.append({
            'text': text,
            'x': x,
            'y': y,
            'color': color,
            'life': 80,  # frames to live
            'start_y': y
        })

    def create_signup_particles(self, x, y):
        """Create particles for sign up"""
        for _ in range(15):
            self.particles.append({
                'x': x + random.randint(-40, 40),
                'y': y + random.randint(-20, 20),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-3, -1),
                'life': 50,
                'color': random.choice([GREEN, GOLD, BLUE]),
                'size': random.randint(2, 5)
            })

    def create_like_particles(self, x, y):
        """Create heart particles for likes"""
        for _ in range(12):
            self.particles.append({
                'x': x + random.randint(-25, 25),
                'y': y + random.randint(-15, 15),
                'vx': random.uniform(-1.5, 1.5),
                'vy': random.uniform(-2.5, -0.5),
                'life': 40,
                'color': RED,
                'size': random.randint(2, 4),
                'is_heart': True
            })

    def draw_heart(self, x, y, size):
        """Draw a small heart"""
        # Simple heart using circles and triangle
        pygame.draw.circle(self.screen, RED, (int(x-size//3), int(y-size//3)), size//2)
        pygame.draw.circle(self.screen, RED, (int(x+size//3), int(y-size//3)), size//2)
        points = [(int(x), int(y+size//2)), 
                 (int(x-size//2), int(y)), 
                 (int(x+size//2), int(y))]
        pygame.draw.polygon(self.screen, RED, points)

    def update_animations(self):
        """Update all animations"""
        # Update button animations
        if self.like_animation > 0:
            self.like_animation -= 1
        if self.signup_animation > 0:
            self.signup_animation -= 1

        # Update floating texts
        for text in self.floating_texts[:]:
            text['y'] -= 1.2  # Float upward
            text['life'] -= 1
            if text['life'] <= 0:
                self.floating_texts.remove(text)

        # Update particles
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.08  # Gravity
            particle['life'] -= 1

            if particle['life'] <= 0:
                self.particles.remove(particle)

    def draw_particles(self):
        """Draw all particles"""
        for particle in self.particles:
            if particle.get('is_heart', False):
                self.draw_heart(particle['x'], particle['y'], particle['size'])
            else:
                pygame.draw.circle(self.screen, particle['color'], 
                                 (int(particle['x']), int(particle['y'])), 
                                 particle['size'])

    def draw_floating_texts(self):
        """Draw floating text effects"""
        for text in self.floating_texts:
            alpha_factor = text['life'] / 80

            rendered_text = self.font_small.render(text['text'], True, text['color'])
            text_rect = rendered_text.get_rect(center=(text['x'], text['y']))
            self.screen.blit(rendered_text, text_rect)

    def handle_click(self, pos):
        """Handle mouse clicks"""
        if not self.is_signed_up and self.signup_button.collidepoint(pos):
            self.sign_up()
        elif self.is_signed_up and self.like_button.collidepoint(pos):
            self.give_like()

    def update(self):
        """Update game state"""
        current_time = pygame.time.get_ticks()

        # Increment number based on rate (every second)
        if current_time - self.last_increment_time >= 1000:
            self.number += self.increment_rate
            self.last_increment_time = current_time

        # Update animations
        self.update_animations()

    def draw_stats_panel(self):
        """Draw the statistics panel"""
        panel_rect = pygame.Rect(50, 550, SCREEN_WIDTH-100, 120)
        pygame.draw.rect(self.screen, LIGHT_GRAY, panel_rect)
        pygame.draw.rect(self.screen, BLACK, panel_rect, 2)

        # Stats title
        stats_title = self.font_medium.render("STATISTICS", True, BLACK)
        self.screen.blit(stats_title, (60, 560))

        # Stats content
        stats = [
            f"Total Likes: {self.total_likes}",
            f"Total Sign-ups: {self.total_signups}",
            f"Current Rate: +{self.increment_rate:.1f}/sec",
            f"Accounts Created: {len(self.account_names)}"
        ]

        for i, stat in enumerate(stats):
            x = 60 + (i % 2) * 300
            y = 590 + (i // 2) * 25
            stat_text = self.font_small.render(stat, True, BLACK)
            self.screen.blit(stat_text, (x, y))

        # Current account status
        if self.is_signed_up:
            account_text = self.font_small.render(f"Logged in as: {self.current_account_name}", 
                                                True, GREEN)
            self.screen.blit(account_text, (60, 640))
        else:
            account_text = self.font_small.render("Not logged in", True, RED)
            self.screen.blit(account_text, (60, 640))

    def draw(self):
        """Draw everything"""
        self.screen.fill(WHITE)

        # Title
        title_text = self.font_title.render("SIGN UP TO LIKE", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title_text, title_rect)

        subtitle_text = self.font_small.render("(Every Single Time!)", True, DARK_GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, 80))
        self.screen.blit(subtitle_text, subtitle_rect)

        # Current number (big and prominent)
        number_color = GREEN if self.increment_rate > 2 else (BLUE if self.increment_rate > 1.5 else BLACK)
        number_text = self.font_large.render(f"Number: {int(self.number)}", True, number_color)
        number_rect = number_text.get_rect(center=(SCREEN_WIDTH//2, 140))
        self.screen.blit(number_text, number_rect)

        # Rate display
        rate_text = self.font_medium.render(f"Growing at +{self.increment_rate:.1f} per second", 
                                          True, DARK_GRAY)
        rate_rect = rate_text.get_rect(center=(SCREEN_WIDTH//2, 180))
        self.screen.blit(rate_text, rate_rect)

        # Progress indicator
        progress_text = self.font_small.render("Like and subscribe pls", True, BLACK)
        progress_rect = progress_text.get_rect(center=(SCREEN_WIDTH//2, 220))
        self.screen.blit(progress_text, progress_rect)

        # Main interaction area
        if not self.is_signed_up:
            # Sign up section
            instruction_text = self.font_medium.render("Create an account to like!", True, BLACK)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, 280))
            self.screen.blit(instruction_text, instruction_rect)

            # Sign up button with animation
            button_size_offset = self.signup_animation * 2
            signup_button_animated = pygame.Rect(
                self.signup_button.x - button_size_offset//2,
                self.signup_button.y - button_size_offset//4,
                self.signup_button.width + button_size_offset,
                self.signup_button.height + button_size_offset//2
            )

            button_color = BLUE
            if signup_button_animated.collidepoint(pygame.mouse.get_pos()):
                button_color = (50, 100, 150)

            pygame.draw.rect(self.screen, button_color, signup_button_animated, border_radius=8)
            pygame.draw.rect(self.screen, BLACK, signup_button_animated, 2, border_radius=8)

            signup_text = self.font_medium.render("CREATE ACCOUNT", True, WHITE)
            signup_rect = signup_text.get_rect(center=signup_button_animated.center)
            self.screen.blit(signup_text, signup_rect)

            # Like button (disabled)
            pygame.draw.rect(self.screen, LIGHT_GRAY, self.like_button, border_radius=8)
            pygame.draw.rect(self.screen, DARK_GRAY, self.like_button, 2, border_radius=8)

            disabled_text = self.font_medium.render("LIKE", True, DARK_GRAY)
            disabled_rect = disabled_text.get_rect(center=self.like_button.center)
            self.screen.blit(disabled_text, disabled_rect)

            step_text = self.font_small.render("like plssssss", True, DARK_GRAY)
            step_rect = step_text.get_rect(center=(SCREEN_WIDTH//2, 520))
            self.screen.blit(step_text, step_rect)

        else:
            # Signed up - show like button
            instruction_text = self.font_medium.render(f"Welcome, {self.current_account_name}!", True, GREEN)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, 280))
            self.screen.blit(instruction_text, instruction_rect)

            step_text = self.font_medium.render("like plssssss", True, BLACK)
            step_rect = step_text.get_rect(center=(SCREEN_WIDTH//2, 320))
            self.screen.blit(step_text, step_rect)

            # Sign up button (disabled)
            pygame.draw.rect(self.screen, LIGHT_GRAY, self.signup_button, border_radius=8)
            pygame.draw.rect(self.screen, DARK_GRAY, self.signup_button, 2, border_radius=8)
            disabled_signup_text = self.font_medium.render("SIGNED UP", True, DARK_GRAY)
            disabled_signup_rect = disabled_signup_text.get_rect(center=self.signup_button.center)
            self.screen.blit(disabled_signup_text, disabled_signup_rect)

            # Like button (active) with animation
            button_size_offset = self.like_animation * 3
            like_button_animated = pygame.Rect(
                self.like_button.x - button_size_offset//2,
                self.like_button.y - button_size_offset//4,
                self.like_button.width + button_size_offset,
                self.like_button.height + button_size_offset//2
            )

            button_color = RED
            if like_button_animated.collidepoint(pygame.mouse.get_pos()):
                button_color = (180, 20, 40)

            pygame.draw.rect(self.screen, button_color, like_button_animated, border_radius=8)
            pygame.draw.rect(self.screen, BLACK, like_button_animated, 2, border_radius=8)

            like_text = self.font_medium.render("LIKE (+0.2)", True, WHITE)
            like_rect = like_text.get_rect(center=like_button_animated.center)
            self.screen.blit(like_text, like_rect)

            warning_text = self.font_small.render("Warning: You'll be logged out after liking!", 
                                                True, ORANGE)
            warning_rect = warning_text.get_rect(center=(SCREEN_WIDTH//2, 520))
            self.screen.blit(warning_text, warning_rect)

        # Draw particles and floating text
        self.draw_particles()
        self.draw_floating_texts()

        # Draw stats panel
        self.draw_stats_panel()

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.handle_click(event.pos)

            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()

# Run the game
if __name__ == "__main__":
    game = SignUpEveryLikeGame()
    game.run()
