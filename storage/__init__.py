"""神仙道嵌入式 SQLite 存储与状态持久化体系

提供静态协议元数据字典检索、多角色独立私有库、后台专职异步写入流水线、
FIFO 滚动淘汰策略、强类型领域子仓储以及统一存储门面 GameStorage 与 EventBus 切面订阅器。

@author Ateng
@since 2026-10-16
"""

from storage.facade import (
    AuditLogRepository,
    BattleRecordRepository,
    GameStorage,
    InventoryRepository,
    ModuleStateRepository,
    PlayerRepository,
)
from storage.player_db import (
    MAX_FIFO_RECORDS,
    AuditLogRecord,
    BattleRecord,
    InventoryItemRecord,
    ModuleStateRecord,
    PlayerDatabase,
    PlayerProfileRecord,
)
from storage.protocol_db import (
    ActionMeta,
    ConstantMeta,
    ModuleMeta,
    ProtocolDatabase,
    ProtocolRepository,
)
from storage.subscriber import SqliteStorageSubscriber
from storage.worker import (
    StorageTask,
    StorageWorker,
)

__all__ = [
    # 静态协议元数据仓储
    "ModuleMeta",
    "ActionMeta",
    "ConstantMeta",
    "ProtocolDatabase",
    "ProtocolRepository",
    # 角色动态实体模型与私有库
    "PlayerProfileRecord",
    "InventoryItemRecord",
    "ModuleStateRecord",
    "BattleRecord",
    "AuditLogRecord",
    "PlayerDatabase",
    "MAX_FIFO_RECORDS",
    # 异步写入流水线
    "StorageTask",
    "StorageWorker",
    # 领域子仓储与统一门面
    "PlayerRepository",
    "InventoryRepository",
    "ModuleStateRepository",
    "BattleRecordRepository",
    "AuditLogRepository",
    "GameStorage",
    # 事件总线持久化切面
    "SqliteStorageSubscriber",
]
