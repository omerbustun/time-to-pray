from PyQt6.QtGui import QPainter, QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt
from ..api.fetch_times import get_monthly_prayer_times, get_remaining_time_for_next_prayer
import os

ICON_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "icon.png")

def generate_icon_with_text(text):
    """
    Generates a QIcon with the specified text.
    """
    # Create a QPixmap (canvas) of the desired size
    pixmap = QPixmap(64, 64)  # You can adjust this size as needed
    pixmap.fill(Qt.GlobalColor.transparent)  # Fill with a transparent color

    # Create a QPainter to draw on the QPixmap
    painter = QPainter(pixmap)
    painter.setFont(QFont("Arial", 28))  # Set font and size
    painter.setPen(Qt.GlobalColor.white)  # Set text color
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, text)  # Draw centered text

    painter.end()  # End the QPainter session

    return QIcon(pixmap)

def update_tray_icon(tray):
    """
    Updates the tray icon with the remaining time for the next prayer.
    """
    today_prayer_times = get_monthly_prayer_times()
    next_prayer, remaining_time = get_remaining_time_for_next_prayer(today_prayer_times)

    if remaining_time:
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        # For the tooltip
        tooltip_time_text = f"{hours}:{minutes:02d}"

        # For the tray icon
        if hours == 0:
            tray_time_text = f"{minutes}"
        else:
            tray_time_text = f"{hours}:{minutes:02d}"
        
        # Generate the icon with the desired text for the tray
        icon = generate_icon_with_text(tray_time_text)

        # Set the generated icon as the tray icon
        tray.setIcon(icon)

        # Set the tooltip for the tray icon
        tray.setToolTip(f"Next prayer is {next_prayer} in {tooltip_time_text}")
    else:
        # Handle the case where remaining_time is None, e.g., set the default icon
        tray.setIcon(QIcon(ICON_PATH))
        pass

