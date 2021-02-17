try:
	from __init__ import *
except:
	from src import *

application = create_app(testing=False)

if __name__ == '__main__':
	application.run()