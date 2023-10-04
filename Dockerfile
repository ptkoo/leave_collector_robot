FROM balenalib/rpi-debian:bullseye-build
LABEL io.balena.device-type="raspberry-pi"

# Install required dependencies (if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
		less \
		kmod \
		nano \
		net-tools \
		ifupdown \
		iputils-ping \
		i2c-tools \
		usbutils \
	&& rm -rf /var/lib/apt/lists/*

# RUN [ ! -d /.balena/messages ] && mkdir -p /.balena/messages; echo 'Here are a few details about this Docker image (For more information please visit https://www.balena.io/docs/reference/base-images/base-images/): \nArchitecture: ARM v6 \nOS: Debian Bullseye \nVariant: build variant \nDefault variable(s): UDEV=off \nExtra features: \n- Easy way to install packages with `install_packages <package-name>` command \n- Run anywhere with cross-build feature  (for ARM only) \n- Keep the container idling with `balena-idle` command \n- Show base image details with `balena-info` command' > /.balena/messages/image-info

# Set the working directory inside the container
WORKDIR /app

# Copy the Python scripts and other necessary files into the container
COPY src/ /app/src/
# COPY data/ /app/data/
# COPY logs/ /app/logs/
COPY Dockerfile /app/

# Set the entry point to run main.py using python
CMD ["python3", "src/main.py"]
