from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg, LeggedRobotCfgPPO

class GO2RoughCfg( LeggedRobotCfg ):
    class init_state( LeggedRobotCfg.init_state ):
        """描述机器人的初始状态，包括位置和各关节的默认角度"""
        pos = [0.0, 0.0, 0.42] # x,y,z [m]
        # 下面的关节一共有12个（4个髋关节、4个大腿关节、4个小腿关节），我是不是也可以理解为我的动作输出就是一个12维的向量（连续）
        default_joint_angles = { # = target angles [rad] when action = 0.0
            'FL_hip_joint': 0.1,   # [rad]
            'RL_hip_joint': 0.1,   # [rad]
            'FR_hip_joint': -0.1 ,  # [rad]
            'RR_hip_joint': -0.1,   # [rad]

            'FL_thigh_joint': 0.8,     # [rad]
            'RL_thigh_joint': 1.,   # [rad]
            'FR_thigh_joint': 0.8,     # [rad]
            'RR_thigh_joint': 1.,   # [rad]

            'FL_calf_joint': -1.5,   # [rad]
            'RL_calf_joint': -1.5,    # [rad]
            'FR_calf_joint': -1.5,  # [rad]
            'RR_calf_joint': -1.5,    # [rad]
        }

    class control( LeggedRobotCfg.control ):
        """该配置类定义了如何将如神经网络的输出的动作转换为关节的PD控制信号"""
        # PD Drive parameters:
        control_type = 'P'
        stiffness = {'joint': 20.}  # [N*m/rad]
        damping = {'joint': 0.5}     # [N*m*s/rad]
        # action scale: target angle = actionScale * action + defaultAngle
        action_scale = 0.25
        # decimation: Number of control action updates @ sim DT per policy DT
        decimation = 4

    class asset( LeggedRobotCfg.asset ):
        """这个配置类 asset 继承自 LeggedRobotCfg.asset，用于定义与机器人物理模型（URDF文件） 和碰撞处理规则相关的设置。"""
        file = '{LEGGED_GYM_ROOT_DIR}/resources/robots/go2/urdf/go2.urdf'
        name = "go2"
        foot_name = "foot"
        # 以下三个参数是碰撞处理规则（强化学习关键设置）
        penalize_contacts_on = ["thigh", "calf"]    # 在这些部位发生接触时施加奖励惩罚
        terminate_after_contacts_on = ["base"]  # 在这些部位发生接触时终止当前训练回合
        self_collisions = 1 # 1 to disable, 0 to enable...bitwise filter
  
    class rewards( LeggedRobotCfg.rewards ):
        soft_dof_pos_limit = 0.9    # 设置关节位置的软限制边界（当关节接近物理极限时提前给予惩罚，防止硬件损坏）
        base_height_target = 0.25   # 设定机器人躯干（基座）的目标高度（奖励函数会给予机器人保持这个高度的正奖励（或偏离的负奖励））
        class scales( LeggedRobotCfg.rewards.scales ):
            torques = -0.0002   # 关节扭矩消耗的惩罚系数
            dof_pos_limits = -10.0  # 关节超出软限制的惩罚系数

class GO2RoughCfgPPO( LeggedRobotCfgPPO ):
    """描述与PPO算法相关的参数"""
    class algorithm( LeggedRobotCfgPPO.algorithm ):
        entropy_coef = 0.01
    class runner( LeggedRobotCfgPPO.runner ):
        run_name = ''
        experiment_name = 'rough_go2'

  
