#!/bin/bash
# Setup script for Raspberry Pi Drowsiness Detection System

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required system dependencies
echo "Installing system dependencies..."
sudo apt-get install -y build-essential cmake pkg-config
sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install -y libxvidcore-dev libx264-dev
sudo apt-get install -y libfontconfig1-dev libcairo2-dev
sudo apt-get install -y libgdk-pixbuf2.0-dev libpango1.0-dev
sudo apt-get install -y libgtk2.0-dev libgtk-3-dev
sudo apt-get install -y libatlas-base-dev gfortran
sudo apt-get install -y python3-dev python3-pip
sudo apt-get install -y python3-numpy python3-scipy

# Create virtual environment
echo "Setting up Python virtual environment..."
python3 -m pip install virtualenv
python3 -m virtualenv -p python3 venv
source venv/bin/activate

# Install Python packages
echo "Installing Python dependencies..."
pip install -r ../requirements.txt

# Create logs directory
echo "Creating logs directory..."
mkdir -p ../logs

# Download facial landmark predictor
echo "Downloading facial landmark predictor..."
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bzip2 -d shape_predictor_68_face_landmarks.dat.bz2
mv shape_predictor_68_face_landmarks.dat ../models/

# Set up automatic startup (optional)
echo "Setting up autostart (optional)..."
if [ "$1" = "--enable-autostart" ]; then
    mkdir -p ~/.config/autostart
    cat > ~/.config/autostart/drowsiness_detection.desktop << EOL
[Desktop Entry]
Type=Application
Name=Drowsiness Detection
Comment=Start Drowsiness Detection System on boot
Exec=/bin/bash -c 'cd $(pwd)/.. && source venv/bin/activate && python main.py'
Hidden=false
X-GNOME-Autostart-enabled=true
EOL
    echo "Autostart enabled. The application will start on boot."
fi

echo "Setup complete! You can now run the drowsiness detection system by:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the main script: python main.py"