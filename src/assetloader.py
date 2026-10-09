from .utils import GhostColor

import pygame


class Paths:
    ASSETS = "assets/"
    ICON = ASSETS + "icon/"
    FRUIT = ASSETS + "fruit/"
    BUTTON = ASSETS + "button/"
    GHOSTS = ASSETS + "ghosts/"
    PACMAN = ASSETS + "pacman/"
    RED = GHOSTS + "red/"
    BLUE = GHOSTS + "blue/"
    PINK = GHOSTS + "pink/"
    ORANGE = GHOSTS + "orange/"
    SECRET = GHOSTS + "secret/"
    CRAZY = GHOSTS + "crazyman/"
    ALIVE = ICON + "heart.png"
    DEAD = ICON + "dead_heart.png"
    REFLECT = ICON + "reflect.png"
    UNPRESSED = BUTTON + "button.png"
    PRESSED = BUTTON + "button_pressed.png"


class AssetLoader:
    @staticmethod
    def load_ghosts() -> dict[GhostColor, list[pygame.Surface]]:
        ghosts_img = {
            GhostColor.RED: [pygame.image.load(
                f"{Paths.RED}{i+1}.png").convert_alpha()
                for i in range(8)],
            GhostColor.BLUE: [pygame.image.load(
                f"{Paths.BLUE}{i+1}.png").convert_alpha()
                for i in range(8)],
            GhostColor.ORANGE: [pygame.image.load(
                f"{Paths.ORANGE}{i+1}.png").convert_alpha()
                for i in range(8)],
            GhostColor.PINK: [pygame.image.load(
                f"{Paths.PINK}{i+1}.png").convert_alpha()
                for i in range(8)],
            GhostColor.SECRET: [pygame.image.load(
                f"{Paths.SECRET}{i+1}.png").convert_alpha()
                for i in range(8)],
            GhostColor.CRAZY: [
                pygame.image.load(
                    f"assets/ghosts/crazyman/{i+1}.png").convert_alpha()
                for i in range(4)]
        }

        return ghosts_img

    @staticmethod
    def load_pacman() -> list[pygame.Surface]:
        pacman_img_copy = [
            pygame.image.load(f"{Paths.PACMAN}{i}.png").convert_alpha()
            for i in range(5)
        ]

        return pacman_img_copy

    @staticmethod
    def load_life() -> tuple[pygame.Surface, pygame.Surface, pygame.Surface]:
        alive = pygame.image.load(Paths.ALIVE).convert_alpha()

        dead = pygame.image.load(Paths.DEAD).convert_alpha()
        reflect = pygame.image.load(Paths.REFLECT).convert_alpha()

        return dead, alive, reflect

    @staticmethod
    def load_fruit() -> list[pygame.Surface]:
        fruit = [
            pygame.image.load(
                f"{Paths.FRUIT}{i+1}.png"
            ).convert_alpha() for i in range(3)
        ]

        return fruit

    @staticmethod
    def load_buttons() -> tuple[pygame.Surface, pygame.Surface]:
        normal = pygame.image.load(Paths.UNPRESSED)
        pressed = pygame.image.load(Paths.PRESSED)

        return normal, pressed
