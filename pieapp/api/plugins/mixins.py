from __future__ import annotations

from PySide6.QtCore import Signal

from pieapp.api.models.media import MediaFile
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin
from pieapp.api.registries.menus.mixins import MenuAccessorMixin
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin
from pieapp.api.registries.toolbars.mixins import ToolBarAccessorMixin
from pieapp.api.registries.toolbuttons.mixins import ToolButtonAccessorMixin


class MediaPluginMixin:
    # Emit on snapshot created
    sig_on_snapshot_created = Signal(MediaFile)

    # Emit on snapshot deleted
    sig_on_snapshot_deleted = Signal(MediaFile)

    # Emit on snapshot modified
    sig_on_snapshot_modified = Signal(MediaFile)

    # Emit on global snapshot restored
    sig_on_snapshot_restored = Signal()

    # Global snapshots

    # Emit on global snapshot created
    sig_on_global_snapshot_created = Signal(MediaFile)

    # Emit on global snapshot deleted
    sig_on_global_snapshot_deleted = Signal(MediaFile, int)

    # Emit on global snapshot modified
    sig_on_global_snapshot_modified = Signal(MediaFile)

    # Emit on global snapshot restored
    sig_on_global_snapshot_restored = Signal()


class CoreAccessorsMixin(
    ConfigAccessorMixin,
    ThemeAccessorMixin
):
    pass


class LayoutAccessorsMixins(
    MenuAccessorMixin,
    ToolBarAccessorMixin,
    ToolButtonAccessorMixin
):
    pass
