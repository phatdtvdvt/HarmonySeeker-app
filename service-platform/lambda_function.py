from mangum import Mangum
from main import app

# Create Lambda handler from the app
handler = Mangum(app)
