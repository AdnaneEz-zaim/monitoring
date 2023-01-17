import dash
import models.Dash as Dashboard

dash.register_page(__name__, order=2)

layout = Dashboard.generate_monitoring_layout()

