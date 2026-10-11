from .utils import GhostColor, Paths

import pygame


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
                pygame.image.load(f"{Paths.CRAZY}{i+1}.png").convert_alpha()
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
        return (
            pygame.image.load(Paths.DEAD).convert_alpha(),
            pygame.image.load(Paths.ALIVE).convert_alpha(),
            pygame.image.load(Paths.REFLECT).convert_alpha()
        )

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
