import os
import warnings
from app.controller import MainWindowController

# Suppress joblib/loky warnings
warnings.filterwarnings("ignore", category=UserWarning, module="joblib.externals.loky")

# Set environment variable for loky
os.environ['LOKY_MAX_CPU_COUNT'] = '4'  # Set to a reasonable number of cores

def main():
    try:
        controller = MainWindowController()
        controller.run()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
