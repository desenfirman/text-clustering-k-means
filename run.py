# Run a test server.
from app import app
print("Hello")
app.run(host='127.0.0.1', port=8080, debug=True)

# end of file
