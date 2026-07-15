from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MotionPalette:
    bg: str
    empty: str
    snake: str
    levels: tuple[str, str, str, str, str]  # 0=empty, 1=Q1, 2=Q2, 3=Q3, 4=Q4
    text: str
    glow_color: str   # Dedicated glow color for eye/head effects


PALETTES: dict[str, dict[str, MotionPalette]] = {
    "boot": {
        "light": MotionPalette(
            bg="#EBF3F9",
            empty="#D9E5F0",
            snake="#5E81AC",
            levels=("#D9E5F0", "#BDD8F0", "#8BBDE0", "#5E9BD4", "#1B5FA8"),
            text="#5E81AC",
            glow_color="#A8C8E8",
        ),
        "dark": MotionPalette(
            bg="#0D1117",
            empty="#2B3542",
            snake="#8FB3D4",
            levels=("#1F2937", "#38BDF8", "#0EA5E9", "#0284C7", "#0369A1"),
            text="#8FB3D4",
            glow_color="#38BDF8",
        ),
    },
    "inference": {
        "light": MotionPalette(
            bg="#F0FAFF",
            empty="#E0F7FA",
            snake="#00D2FF",
            levels=("#E0F7FA", "#BAE6FD", "#7DD3FC", "#38BDF8", "#0369A1"),
            text="#0369A1",
            glow_color="#7DD3FC",
        ),
        "dark": MotionPalette(
            bg="#0D1117",
            empty="#18455A",
            snake="#00F2FE",
            levels=("#0F172A", "#0EA5E9", "#00F2FE", "#38BDF8", "#0369A1"),
            text="#00F2FE",
            glow_color="#00F2FE",
        ),
    },
    "optimization": {
        "light": MotionPalette(
            bg="#FFFDF9",
            empty="#F3DFC9",
            snake="#D08770",
            levels=("#F3DFC9", "#F5E2C8", "#E6C59E", "#D59E74", "#C4774B"),
            text="#D08770",
            glow_color="#F4A261",
        ),
        "dark": MotionPalette(
            bg="#0B0F19",
            empty="#0D0A18",
            snake="#D08770",
            levels=("#0D0A18", "#4B3F2A", "#7A6230", "#B08A3A", "#F0C050"),
            text="#D08770",
            glow_color="#F4A261",
        ),
    },
    "research": {
        "light": MotionPalette(
            bg="#FCFBFE",
            empty="#E8DDF5",
            snake="#B48EAD",
            levels=("#E8DDF5", "#E9D8FA", "#D4B9FA", "#BF9AFA", "#A855F7"),
            text="#A855F7",
            glow_color="#D4B9FA",
        ),
        "dark": MotionPalette(
            bg="#020204",
            empty="#0A0009",
            snake="#B48EAD",
            levels=("#0A0009", "#2D1B4A", "#4A2878", "#6B3FA8", "#A78BFA"),
            text="#B48EAD",
            glow_color="#A78BFA",
        ),
    },
}
