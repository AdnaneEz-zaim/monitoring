import dash
import models.Dash as Dashboard

dash.register_page(__name__, order=3)

layout = Dashboard.generate_configuration_layout()
