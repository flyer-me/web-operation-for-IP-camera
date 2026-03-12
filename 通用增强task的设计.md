存档，代码目的是为RPA任务进行流程的控制，包括日志、数据库存储、检查点记录和断点恢复。以下是示例，未进行良好设计和测试，不要直接使用。

```python

# ---------------------- 进度缓冲器 ----------------------
class ProgressBuffer:
    def __init__(self, progress: TaskProgress, update_interval_steps: int = 10, update_interval_seconds: float = 1.0):
        self.progress = progress
        self.update_interval_steps = update_interval_steps  # 每N步更新一次数据库
        self.update_interval_seconds = update_interval_seconds  # 每T秒更新一次数据库
        self.last_update_step = 0
        self.last_update_time = time.time()
        self._cached_data = {}

    def update(self, **kwargs) -> None:
        """缓存进度数据，满足条件时才写入数据库"""
        self._cached_data.update(kwargs)
        current_step = kwargs.get('step_current', self.last_update_step)
        current_time = time.time()
        if (current_step - self.last_update_step >= self.update_interval_steps or
            current_time - self.last_update_time >= self.update_interval_seconds):
            self._flush()

    def _flush(self) -> None:
        """写入数据库"""
        if self._cached_data:
            self.progress.update(**self._cached_data)
            self.last_update_step = self._cached_data.get('step_current', self.last_update_step)
            self.last_update_time = time.time()
            self._cached_data = {}

    def close(self) -> None:
        """关闭时强制写入剩余数据"""
        self._flush()

# ======================
# 日志过滤器(给日志添加 task_id 上下文)
# ======================
class TaskIdFilter(logging.Filter):
    def __init__(self, task_id: str = "unknown"):
        self.task_id = task_id

    def filter(self, record: logging.LogRecord) -> bool:
        record.task_id = self.task_id
        return True

# ======================
# Peewee 数据模型
# ======================
class TaskProgressModel(Model):
    """任务进度表(支持状态追踪、异常记录)"""
    task_id = CharField(primary_key=True, max_length=100, verbose_name="任务唯一标识")
    task_name = CharField(max_length=200, default="", verbose_name="任务名称")
    cursor = IntegerField(default=0, verbose_name="断点游标(行号/页数/字节数)")
    extra = TextField(default="{}", verbose_name="上下文数据(JSON)")
    status = CharField(
        max_length=20, 
        default="pending", 
        verbose_name="任务状态(pending/running/failed/finished)"
    )
    error_info = TextField(default="", verbose_name="异常信息(失败时记录)")
    create_time = DateTimeField(default=datetime.now, verbose_name="创建时间")
    update_time = DateTimeField(default=datetime.now, verbose_name="更新时间")

    class Meta:
        database = get_db()
        table_name = "task_progress"
        indexes = (
            (("status", "update_time"), False),  # 复合索引: 按状态+时间快速查询
        )

# ======================
# 通用任务进度管理器
# ======================
class TaskProgressManager:
    def __init__(self, task_id: str, task_name: str = "", db_path: str = "task_progress.db"):
        self.task_id = task_id
        self.task_name = task_name
        self.db = get_db(db_path)
        self._init_task()
        # 给日志添加 task_id 过滤器
        self.log_filter = TaskIdFilter(task_id)
        for handler in logger.handlers:
            handler.addFilter(self.log_filter)

    def _init_task(self):
        """初始化任务: 不存在则创建，失败则重置为可重试状态"""
        try:
            with self.db.atomic():  # 事务保证原子性
                task, created = TaskProgressModel.get_or_create(
                    task_id=self.task_id,
                    defaults={
                        "task_name": self.task_name,
                        "cursor": 0,
                        "extra": "{}",
                        "status": "pending"
                    }
                )
                if not created:
                    # 若任务上次失败，重置为 pending 允许重试，保留 cursor 以便续传
                    if task.status == "failed":
                        task.status = "pending"
                        task.error_info = ""
                        task.save()
                        logger.info(f"任务上次失败，已重置为待执行状态，保留断点 cursor={task.cursor}")
        except IntegrityError:
            pass  # 并发场景下的重复创建，忽略

    @contextmanager
    def session(self):
        """数据库会话上下文管理器(自动处理连接/事务)"""
        with self.db.connection_context():
            yield

    def get_breakpoint(self) -> Tuple[int, Dict[str, Any]]:
        """
        获取断点信息
        :return: (cursor, extra_dict)
        """
        with self.session():
            task = TaskProgressModel.get_by_id(self.task_id)
            cursor = task.cursor
            try:
                extra = json.loads(task.extra)
            except json.JSONDecodeError:
                extra = {}
                logger.warning(f" extra 字段 JSON 解析失败，已重置为空字典")
            logger.info(f"获取断点: cursor={cursor}, extra={extra}")
            return cursor, extra

    def update_progress(
        self, 
        step: int = 1, 
        extra: Optional[Dict[str, Any]] = None, 
        cursor_override: Optional[int] = None
    ):
        """
        更新进度
        :param step: 进度步长(默认+1)
        :param extra: 上下文数据(覆盖更新)
        :param cursor_override: 强制覆盖 cursor(可选，用于非连续进度场景)
        """
        extra = extra or {}
        with self.session():
            task = TaskProgressModel.get_by_id(self.task_id)
            # 更新 cursor
            if cursor_override is not None:
                task.cursor = cursor_override
            else:
                task.cursor += step
            # 更新 extra
            task.extra = json.dumps(extra, ensure_ascii=False)
            task.status = "running"
            task.update_time = datetime.now()
            task.save()
            logger.debug(f"进度更新: cursor={task.cursor}, step={step}, extra={extra}")

    def mark_failed(self, error_msg: str = "", exc_info: Optional[Tuple] = None):
        """
        标记任务失败，记录异常信息
        :param error_msg: 自定义错误信息
        :param exc_info: 异常元组(sys.exc_info())
        """
        error_trace = ""
        if exc_info:
            error_trace = "".join(traceback.format_exception(*exc_info))
        full_error = f"{error_msg}\n{error_trace}".strip()
        
        with self.session():
            task = TaskProgressModel.get_by_id(self.task_id)
            task.status = "failed"
            task.error_info = full_error
            task.update_time = datetime.now()
            task.save()
        logger.error(f"任务失败: {error_msg}", exc_info=exc_info)

    def mark_finished(self):
        """标记任务完成"""
        with self.session():
            task = TaskProgressModel.get_by_id(self.task_id)
            task.status = "finished"
            task.update_time = datetime.now()
            task.save()
        logger.info(f"任务完成！总进度 cursor={task.cursor}")

    def close(self):
        """清理资源(移除日志过滤器)"""
        for handler in logger.handlers:
            handler.removeFilter(self.log_filter)

    def __enter__(self) -> "TaskProgressManager":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.mark_failed(exc_info=(exc_type, exc_val, exc_tb))
        self.close()
        return False  # 不抑制异常，继续向上抛出

# ======================
# 装饰器(自动异常处理、资源管理)
# ======================
def with_task_progress(
    task_id: str, 
    task_name: str = ""
):
    """
    任务进度装饰器(增强版)
    :param task_id: 任务唯一ID
    :param task_name: 任务名称(可选)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            with TaskProgressManager(task_id, task_name) as tp:
                # 获取断点
                start_cursor, extra = tp.get_breakpoint()

                try:
                    # 执行业务函数
                    result = func(start_cursor, extra, tp, *args, **kwargs)
                    # 成功则标记完成
                    tp.mark_finished()
                    return result
                except Exception as e:
                    tp.mark_failed(exc_info=True)
                    raise
        return wrapper
    return decorator

# ======================
# 6. 业务代码示例(演示完整流程: 断点续传、异常处理、重试)
# ======================
# 示例1: 模拟处理未知行数的文件(带异常、断点续传)
@with_task_progress(
    task_id="process_large_file_v2",
    task_name="处理2026年3月数据文件")
def process_large_file(
    start_cursor: int, 
    extra: Dict[str, Any], 
    tp: TaskProgressManager
):
    """
    业务函数签名固定: (start_cursor, extra, tp, *args, **kwargs)
    """
    # 从 extra 恢复上下文(无则初始化)
    file_path = extra.get("file_path", "large_data.txt")
    encoding = extra.get("encoding", "utf-8")
    
    # 模拟生成大文件(实际场景替换为真实文件读取)
    import os
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding=encoding) as f:
            for i in range(100):
                f.write(f"这是第 {i} 行数据，内容随机: {datetime.now().isoformat()}\n")
    
    # 读取文件
    with open(file_path, "r", encoding=encoding) as f:
        lines = f.readlines()
    
    # 从断点开始处理
    for line_idx in range(start_cursor, len(lines)):
        line = lines[line_idx].strip()
        
        # ========== 核心业务逻辑(模拟可能的异常) ==========
        if line_idx == 30:  # 第一次运行到第30行故意抛异常
            raise ValueError(f"模拟处理失败: 第 {line_idx} 行数据格式错误")
        
        print(f"处理行 {line_idx}: {line[:30]}")
        
        # ========== 更新进度 + 保存上下文 ==========
        tp.update_progress(
            step=1,
            extra={
                "file_path": file_path,
                "encoding": encoding,
                "last_processed_line": line_idx,
                "last_line_content": line[:20]
            }
        )

# 示例2: 模拟爬虫(带分页、上下文恢复)
@with_task_progress(
    task_id="crawl_news_v2",
    task_name="爬取新闻网站数据")
def crawl_news(
    start_cursor: int, 
    extra: Dict[str, Any], 
    tp: TaskProgressManager
):
    base_url = extra.get("base_url", "https://example.com/news?page=")
    max_pages = extra.get("max_pages", 20)
    
    for page in range(start_cursor, max_pages):
        current_url = f"{base_url}{page}"
        
        # ========== 核心爬虫逻辑 ==========
        print(f"爬取页面: {current_url}")
        
        # ========== 更新进度 ==========
        tp.update_progress(
            step=1,
            extra={
                "base_url": base_url,
                "max_pages": max_pages,
                "current_url": current_url,
                "crawl_time": datetime.now().isoformat()
            }
        )

```
