"""Component for displaying a Bokeh graph."""

from __future__ import annotations
import json
from typing import Any, Dict, List

from reflex.base import Base
from reflex.components.component import Component, NoSSRComponent
from reflex.event import EventHandler
from reflex.utils import console
from reflex.vars.base import LiteralVar, Var

try:
    from bokeh.plotting import figure as Figure
    from bokeh.embed import json_item
    console.log("Bokeh imported!")
except ImportError:
    console.warn("Bokeh is not installed. Please run `pip install bokeh==3.6.0`.")
    Figure = Any
    json_item = None

class Bokeh(NoSSRComponent):
    """Display a Bokeh graph in Reflex."""

    # Bokeh library version
    library = "@bokeh/bokehjs"

    # Tag used in Reflex frontend
    tag = "BokehPlot"

    # Bokeh plot figure data
    data: Var[Dict]  # JSON representation of the Bokeh figure

    # Bokeh layout configurations
    layout: Var[Dict]  # Layout specifications for the Bokeh plot

    # Bokeh chart config, e.g., tools, toolbar, etc.
    config: Var[Dict]  # Configuration options for the Bokeh chart

    # Event handlers for interactions
    on_click: EventHandler  # Fired when the plot is clicked
    on_hover: EventHandler  # Fired when hovering over the plot

    def add_imports(self) -> dict[str, str]:
        """Add imports for the Bokeh component.

        Returns:
            The imports for the Bokeh component.
        """
        return {
            "mergician@v2.0.2": "mergician"  # For merging Bokeh data/layout/templates
        }

    def add_custom_code(self) -> list[str]:
        """Add custom codes for processing the Bokeh points data.

        Returns:
            Custom code snippets for the module level.
        """
        return [
            "const extractPoints = (points) => { /* Your point extraction logic */ }",
            # Add any additional helper functions needed for Bokeh here
        ]

    @classmethod
    def create(cls, *children, **props) -> Component:
        """Create the Bokeh component.

        Args:
            *children: The children of the component.
            **props: The properties of the component.

        Returns:
            The Bokeh component.
        """
        props.setdefault("data", LiteralVar.create({}))  # Default empty figure data
        return super().create(*children, **props)

    def _marshal_bokeh_chart(self, figure: Figure, use_container_width: bool) -> Dict:
        """Marshal (Convert) the Bokeh figure to JSON format for Reflex.

        Args:
            figure: The Bokeh figure to marshal.
            use_container_width: Whether to adjust to container width.

        Returns:
            The marshaled JSON data.
        """
        if json_item is None:
            raise ImportError("Bokeh is not installed. Please run `pip install bokeh`.")

        # Convert Bokeh figure into JSON format using Bokeh's json_item function
        json_data = json_item(figure)
        return {
            "figure": json.dumps(json_data),
            "use_container_width": use_container_width
        }

    def _render(self) -> Component:
        """Render the Bokeh chart in Reflex."""
        tag = super()._render()
        figure = self.data.to(dict)

        # Pass the Bokeh figure to the tag's special props
        tag.special_props.append(Var(_js_expr=f"{{...{str(figure)}}}"))
        return tag
