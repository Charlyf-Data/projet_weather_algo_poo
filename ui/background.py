import base64
import streamlit as st
from pathlib import Path


class BackgroundManager:

    def __init__(self, image_path: str):
        """Initialise le fond avec le chemin de l’image."""
        self.image_path = Path(image_path)
        self.encoded_image = None

    def _encode_image(self):
        """Encode l’image en base64 (usage interne)."""
        if not self.image_path.exists():
            raise FileNotFoundError(f"Image not found: {self.image_path}")

        with open(self.image_path, "rb") as f:
            self.encoded_image = base64.b64encode(f.read()).decode("utf-8")

    def apply(self):
        """Applique le fond à l’application Streamlit."""
        if self.encoded_image is None:
            self._encode_image()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{self.encoded_image}");
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
