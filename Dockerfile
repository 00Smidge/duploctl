ARG PY_VERSION=3.12

# Stage 1: Install dependencies and build tools
FROM python:$PY_VERSION AS setup

# Set the working directory in the container
WORKDIR /app

# Copy the source code, pyproject.toml, .git file to the container
COPY . .

# Install build dependencies
RUN <<EOF
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir .[build]
EOF

# Build the package
FROM setup AS builder
RUN python -m build --no-isolation

# Build the binaries
FROM setup AS installer
RUN pyinstaller scripts/installer.spec && ls -al dist

# use scratch for easy exports
FROM scratch AS bin 
COPY --from=installer /app/dist/duploctl /duploctl

# Stage 2: Install the package in a slimmer container
FROM python:$PY_VERSION-slim AS runner

# Set the working directory in the container
WORKDIR /app

# Copy the built package from the previous stage
COPY --from=builder /app/dist ./dist/

# Install the package using pip
RUN pip install --no-cache-dir ./dist/*.whl && \
    rm -rf ./dist

# Set the entrypoint command for the container
ENTRYPOINT ["duploctl"]
