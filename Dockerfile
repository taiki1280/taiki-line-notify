FROM python

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    git \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV WORKDIR /taiki-line-notify/

WORKDIR ${WORKDIR}

COPY Pipfile Pipfile.lock ${WORKDIR}

RUN pip install pipenv --no-cache-dir && \
    pipenv install --system --deploy && \
    pip uninstall -y pipenv virtualenv-clone virtualenv

COPY . $WORKDIR
