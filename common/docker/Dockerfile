FROM tensorflow/tensorflow:2.9.1-gpu AS base

LABEL maintainer="Elisabetta Iavarone <iavarone@itis.swiss>"

ENV SC_USER_ID 8004
ENV SC_USER_NAME app

RUN set -eux && \
    apt-get update && \
    apt-get install -y gosu && \
    rm -rf /var/lib/apt/lists/* && \
    # verify that the binary works
    gosu nobody true


RUN addgroup --gid ${SC_USER_ID} --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid ${SC_USER_ID} --system --group app


# -------------------------- Build stage -------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    git \
    wget \
    jq \
    python3-minimal \
    python3-pip \
    python3-venv \
    && rm --recursive --force /var/lib/apt/lists/*



# --------------------------Production stage -------------------
FROM base AS production

ENV SC_BUILD_TARGET production

ENV INPUT_FOLDER="/input" \
    OUTPUT_FOLDER="/output"

WORKDIR /home/${SC_USER_NAME}

# Prevent tensorflow from allocating all the GPU memory by default, but it grows as needed
ENV TF_FORCE_GPU_ALLOW_GROWTH=true

RUN pip3 install --upgrade pip
RUN pip3 install scikit-learn

# Verify TensorFlow install
RUN python3 -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
RUN python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

COPY --chown=app:app entrypoint.sh /app/entrypoint.sh


