#!/bin/bash
# ============================================================
# TurtleBot3 仿真启动脚本
# 在 ROS2 Jazzy + Gazebo 环境下运行 TurtleBot3 仿真
# ============================================================

set -e

# ---------- 配置 ----------
# 可选模型: burger, waffle, waffle_pi
TURTLEBOT3_MODEL="${TURTLEBOT3_MODEL:-burger}"
MODE="${1:-gazebo}"   # gazebo / fake / teleop

# ---------- 颜色输出 ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ---------- 检查模型 ----------
valid_models=("burger" "waffle" "waffle_pi")
valid=0
for m in "${valid_models[@]}"; do
    [ "$TURTLEBOT3_MODEL" = "$m" ] && valid=1
done
if [ $valid -eq 0 ]; then
    error "无效的模型: $TURTLEBOT3_MODEL (可选: burger, waffle, waffle_pi)"
    exit 1
fi

# ---------- Source ROS2 ----------
if [ -f /opt/ros/jazzy/setup.bash ]; then
    source /opt/ros/jazzy/setup.bash
elif [ -f /opt/ros/humble/setup.bash ]; then
    source /opt/ros/humble/setup.bash
else
    error "找不到 ROS2 setup.bash，请检查 ROS2 安装"
    exit 1
fi

# Source 工作空间（如果存在）
WS_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$WS_DIR/install/setup.bash" ]; then
    source "$WS_DIR/install/setup.bash"
    info "已加载工作空间: $WS_DIR"
fi

export TURTLEBOT3_MODEL
info "TURTLEBOT3_MODEL = $TURTLEBOT3_MODEL"

# ---------- 模式选择 ----------
case "$MODE" in
    # ---------------------------------------
    # 模式 1: Gazebo 仿真（完整物理仿真）
    # ---------------------------------------
    gazebo)
        info "启动 TurtleBot3 $TURTLEBOT3_MODEL Gazebo 仿真..."
        ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
        ;;

    # ---------------------------------------
    # 模式 2: Fake Node（无需 Gazebo，纯 TF/里程计）
    # ---------------------------------------
    fake)
        info "启动 TurtleBot3 $TURTLEBOT3_MODEL Fake Node..."
        ros2 launch turtlebot3_fake_node turtlebot3_fake_node.launch.py
        ;;

    # ---------------------------------------
    # 模式 3: 键盘遥控
    # ---------------------------------------
    teleop)
        info "启动 TurtleBot3 键盘遥控..."
        info "按如下方式控制:"
        echo "----------------------------"
        echo "  u    i    o"
        echo "  j    k    l"
        echo "  m    ,    ."
        echo "  q/z: 加速/减速"
        echo "  space: 急停"
        echo "----------------------------"
        sleep 1
        ros2 run teleop_twist_keyboard teleop_twist_keyboard
        ;;

    # ---------------------------------------
    # 模式 4: 一键启动 Gazebo + 遥控
    # ---------------------------------------
    full)
        info "启动 TurtleBot3 $TURTLEBOT3_MODEL 仿真 + 键盘遥控..."
        # 后台启动 Gazebo 仿真
        ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py &
        SIM_PID=$!
        sleep 5
        # 前台启动键盘遥控
        ros2 run teleop_twist_keyboard teleop_twist_keyboard
        # 用户退出 teleop 后一并关闭仿真
        kill $SIM_PID 2>/dev/null
        ;;

    *)
        echo "用法: $0 [gazebo|fake|teleop|full]"
        echo ""
        echo "  参数:"
        echo "    gazebo   - 启动 Gazebo 完整仿真（默认）"
        echo "    fake     - 启动 Fake Node（无需 Gazebo）"
        echo "    teleop   - 启动键盘遥控（需先运行仿真）"
        echo "    full     - 启动 Gazebo + 键盘遥控"
        echo ""
        echo "  环境变量:"
        echo "    TURTLEBOT3_MODEL - 模型名称 (burger / waffle / waffle_pi)"
        echo ""
        echo "  示例:"
        echo "    $0 gazebo                          # 使用 burger 模型"
        echo "    TURTLEBOT3_MODEL=waffle $0 gazebo  # 使用 waffle 模型"
        echo "    TURTLEBOT3_MODEL=waffle_pi $0 full # waffle_pi + 遥控"
        exit 1
        ;;
esac
