from .entity.ghosts import GhostColor

import pygame


class Paths:
    ASSETS = "assets/"
    GHOSTS = ASSETS + "ghosts/"
    PACMAN = ASSETS + "pacman/"
    SECRET = GHOSTS + "secret/"
    ORANGE = GHOSTS + "orange/"
    CRAZY = GHOSTS + "crazyman/"
    PINK = GHOSTS + "pink/"
    BLUE = GHOSTS + "blue/"
    RED = GHOSTS + "red/"


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
            pygame.image.load(f"assets/pacman/{i}.png").convert_alpha()
            for i in range(5)
        ]

        return pacman_img_copy

    @staticmethod
    def load_life() -> tuple[pygame.Surface, pygame.Surface]:
        alive = pygame.image.load(
                    "assets/icon/heart.png").convert_alpha()

        dead = pygame.image.load(
            "assets/icon/dead_heart.png").convert_alpha()

        return dead, alive

    @staticmethod
    def load_fruit() -> list[pygame.Surface]:
        fruit = [
            pygame.image.load(
                f"assets/fruit/{i+1}.png"
            ).convert_alpha() for i in range(3)
        ]

        return fruit

    @staticmethod
    def load_buttons() -> tuple[pygame.Surface, pygame.Surface]:
        normal = pygame.image.load("assets/button/button.png")
        pressed = pygame.image.load("assets/button/button_pressed.png")

        return normal, pressed
