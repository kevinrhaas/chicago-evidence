FROM scratch
COPY passwd /etc/passwd
COPY group /etc/group
COPY nsswitch.conf /etc/nsswitch.conf
ENV PATH=/opt/codex/runtimes/codex-primary-runtime/dependencies/node/bin:/usr/bin:/bin
ENV HOME=/tmp/t2794-home
ENV TMPDIR=/tmp
ENV XDG_CACHE_HOME=/tmp/t2794-cache
ENV XDG_CONFIG_HOME=/tmp/t2794-config
ENV NODE_OPTIONS="--v8-pool-size=1 --disable-sigusr1"
ENV UV_THREADPOOL_SIZE=1
ENV OPENBLAS_NUM_THREADS=1
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV NUMEXPR_NUM_THREADS=1
ENV VECLIB_MAXIMUM_THREADS=1
ENV GOMAXPROCS=1
WORKDIR /workspace/shared/T2794-OWNED-CONTAINER-NATIVE-20261023
USER 65532:65532
ENTRYPOINT ["/workspace/shared/w01-python-sum-recovery-20261022/venv311/bin/python", "/workspace/shared/T2794-OWNED-CONTAINER-NATIVE-20261023/run_once.py"]
