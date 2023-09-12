try:
    from bec_plugins.device_server import startup
except ImportError:
    startup = None

if startup is not None:
    startup.run()
    
from device_server import main

if __name__ == "__main__":
    main()
