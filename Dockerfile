# ==============================================================================
# 神仙道无头协议自动化工具 (SXD Bot) 生产级容器镜像
#
# 特性：
#   - 基础底座：Python 3.11-slim (极简轻量，镜像体积 <150MB)
#   - 多阶段构建：隔离编译依赖与最终运行环境
#   - 容器自愈：内嵌标准 HTTP 存活探针 (/api/health)
#   - 运行模式：默认启动 Web 控制台 + 自愈守护双模引擎
#
# @author Ateng
# @since 2026-10-17
# ==============================================================================

# ------------------------------------------------------------------------------
# 阶段 1: 依赖构建器 (Builder)
# ------------------------------------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /build

# 设置非交互与 Python 编译优化
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装编译必要工具
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libc-dev && \
    rm -rf /var/lib/apt/lists/*

# 复制依赖定义并生成 Wheels 缓存
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt

# ------------------------------------------------------------------------------
# 阶段 2: 生产运行时 (Runner)
# ------------------------------------------------------------------------------
FROM python:3.11-slim AS runner

LABEL maintainer="Ateng" \
      description="神仙道无头协议自动化工具 (SXD Bot)"

WORKDIR /app

# 环境变量：国内时区、编码防御、运行模式
ENV TZ=Asia/Shanghai \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    SXD_MODE=web \
    SXD_HOST=0.0.0.0 \
    SXD_PORT=8000

# 安装轻量运行时工具 (curl 用于健康探针，tzdata 维护时区)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# 从 Builder 复制 Wheels 依赖并快速装载
COPY --from=builder /build/wheels /wheels
COPY --from=builder /build/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels

# 创建持久化存储、日志与配置目录
RUN mkdir -p /app/data /app/config /app/logs

# 复制核心业务代码与资源
COPY main.py /app/main.py
COPY core/ /app/core/
COPY network/ /app/network/
COPY protocol/ /app/protocol/
COPY services/ /app/services/
COPY storage/ /app/storage/
COPY tasks/ /app/tasks/
COPY web/ /app/web/
COPY cli/ /app/cli/
COPY config/config.example.json /app/config/config.example.json
COPY data/protocol_manifest.db /app/data/protocol_manifest.db

# 暴露 Web 控制台默认端口
EXPOSE 8000

# 容器内原生存活性探针 (10秒启动宽限期，30秒定期探测)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -fsS http://127.0.0.1:8000/api/health || exit 1

# 默认启动命令：优先支持 SXD_MODE 环境变量判断 (默认拉起 Web 控制台与自愈挂机)
CMD ["sh", "-c", "if [ \"$SXD_MODE\" = 'daemon' ]; then python main.py --daemon; elif [ \"$SXD_MODE\" = 'once' ]; then python main.py --once; else python main.py web --host $SXD_HOST --port $SXD_PORT; fi"]
