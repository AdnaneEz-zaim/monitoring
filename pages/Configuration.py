import dash
import models.Dash as Dashboard

dash.register_page(__name__)

layout = Dashboard.generate_configuration_layout()
