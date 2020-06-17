# BUILD IMAGE --------------------------------------------------------
FROM alpine:3.11 AS python-build

# Get build tools and required header files
RUN apk add --no-cache \
        python3 python3-dev \
        py3-pip py3-virtualenv \
        git gcc musl-dev

RUN mkdir /app
WORKDIR /app
ADD . .

ENV VIRTUAL_ENV=/app/venv
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install python dependencies
RUN pip3 install -r requirements.txt

# ACTUAL IMAGE -------------------------------------------------------
FROM alpine:3.11

RUN apk add --no-cache python3

RUN mkdir /app
COPY --from=python-build /app/. /app/

ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

LABEL maintainer="jakub@status.im"
LABEL source="https://github.com/status-im/auto-sticker-pinner"
LABEL description="Service for pinning newly added Status Sticker Packs"

ENTRYPOINT ["/app/main.py"]
# By default just show help if called without arguments
CMD ["--help"]
