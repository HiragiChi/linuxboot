USE FIST;

CREATE TABLE FIST.kernel_snapshot (
	user_id varchar(50) NOT NULL COMMENT '客户端标识符',
	tar_snapshot varchar(100) NULL COMMENT '用于快速检测的快照路径',
	files_snapshot varchar(100) NULL COMMENT '用于具体检测的快照路径',
	update_date DATE NULL COMMENT '更新日期',
	update_time TIME NULL COMMENT '更新时间',
	kernel_version varchar(30) NULL COMMENT 'Linux内核版本',
	remark varchar(100) NULL COMMENT '注释'
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COLLATE=utf8_general_ci
COMMENT='Store standard snapshot of kernel files.';

