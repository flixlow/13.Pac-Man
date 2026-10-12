"""Asset loading helpers for sprites and UI resources."""

from .utils import GhostColor, Paths

import pygame


class AssetLoader:
    """Load all static sprite resources used by the game."""

    @staticmethod
    def load_ghosts() -> dict[GhostColor, list[pygame.Surface]]:
        """Load all ghost sprite sheets.

        Returns:
            Mapping of ghost colors to lists of surfaces.
        """
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
        """Load Pac-Man animation frames.

        Returns:
            List of Pac-Man sprite surfaces.
        """
        pacman_img_copy = [
            pygame.image.load(f"{Paths.PACMAN}{i}.png").convert_alpha()
            for i in range(5)
        ]

        return pacman_img_copy

    @staticmethod
    def load_life() -> tuple[pygame.Surface, pygame.Surface, pygame.Surface]:
        """Load the life-counter sprites.

        Returns:
            Tuple containing ``(dead, alive, reflect)`` surfaces.
        """
        return (
            pygame.image.load(Paths.DEAD).convert_alpha(),
            pygame.image.load(Paths.ALIVE).convert_alpha(),
            pygame.image.load(Paths.REFLECT).convert_alpha()
        )

    @staticmethod
    def load_fruit() -> list[pygame.Surface]:
        """Load all fruit sprites.

        Returns:
            List of fruit images.
        """
        fruit = [
            pygame.image.load(
                f"{Paths.FRUIT}{i+1}.png"
            ).convert_alpha() for i in range(3)
        ]

        return fruit

    @staticmethod
    def load_buttons() -> tuple[pygame.Surface, pygame.Surface]:
        """Load the menu button sprites.

        Returns:
            Tuple containing normal and pressed button surfaces.
        """
        normal = pygame.image.load(Paths.UNPRESSED)
        pressed = pygame.image.load(Paths.PRESSED)

        return normal, pressed

    @staticmethod
    def load_cheat() -> tuple[pygame.Surface]:
        """Load the cheat assets.

        Returns:
            Tuple containing the differents sprite of cheat mode.
        """
        godmode = pygame.image.load(Paths.GODMODE)
        noclip = pygame.image.load(Paths.NOCLIP)
        ultra_vision = pygame.image.load(Paths.ULTRA_VISION)

        return godmode, noclip, ultra_vision
